#include <stdio.h>
#include <unistd.h>
#include <algorithm>
#include <chrono>
#include <random>
#include <iostream>
#include "Room.hpp"

Room::Room(int roomNumber, Player* host, const std::vector<std::string>& passwordSource):
m_room_number(roomNumber),m_host(host),m_password_source(passwordSource),m_current_round(0), m_max_round(3){
    m_players_list.push_back(host);
    m_game_state = WAITING;
}

Room::~Room() {

    {
        std::lock_guard<std::mutex> lock(m_mutex);
        m_game_state = FINISHED; 
        m_round_over = true;
    }
    m_guess_cv.notify_all();

    if (m_game_thread.joinable()) {
        m_game_thread.join(); 
    }
    
}

void Room::generatePassword(const std::vector <std::string>& WORDS){
    std::random_device rd;               
    std::mt19937 gen(rd());
    
    std::uniform_int_distribution<> dist(0, WORDS.size() - 1 );

    m_password = WORDS[dist(gen)];
}   

void Room::generateHashedPassword(){
    m_hashed_password = "";
    for (size_t i = 0; i<m_password.length();i++){
        m_hashed_password += "_";
    }
}

void Room::generateUnrevealedLetterIndices(){
    for (size_t i = 0;i<m_password.length();i++){
        m_unrevealed_indices.push_back(i);
    }
}

bool Room::revealRandomLetter() {
    if (m_unrevealed_indices.empty()) return false;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, m_unrevealed_indices.size() - 1);

    int idx = dist(gen);
    int letterPos = m_unrevealed_indices[idx];

    m_hashed_password[letterPos] = m_password[letterPos];

    m_unrevealed_indices.erase(m_unrevealed_indices.begin() + idx);
    return true; 
}

void Room::startNewRound(){
    std::lock_guard<std::mutex> lock(m_mutex);
    m_current_round++;
    m_round_over = false;
    m_unrevealed_indices.clear();
    generatePassword(m_password_source);
    generateHashedPassword();
    generateUnrevealedLetterIndices();
    broadcast("NEW_ROUND:" + std::to_string(m_current_round));
    broadcast("HASHPASS:" + m_hashed_password);
}


void Room::processGuess(Player* player, const std::string& guess) {
    std::lock_guard<std::mutex> lock(m_mutex);
    if (m_game_state != IN_PROGRESS || m_round_over) {
        return; 
    }

    if (guess == m_password) {
        m_round_over = true;
        player->addPoint();
        broadcast("CORRECT:" + player->getNick() + ";GUESS:" + guess);
        m_guess_cv.notify_all(); 
    } else {
        broadcast("INCORRECT:" + player->getNick() + ";GUESS:" + guess);
    }
}

void Room::startGame(int maxRound){
    if (m_game_state == IN_PROGRESS) {
        return; 
    }
    for (auto& player : m_players_list) {
        player->resetPoints();
    }
    m_current_round = 0;
    m_max_round = maxRound;
    m_game_state = IN_PROGRESS;
    m_game_thread = std::thread(&Room::gameLoop, this);
    m_game_thread.detach();

}

void Room::broadcast(const std::string& message) {
    for (auto& player : m_players_list) {
        player->sendMessage(message);
    }
}

void Room::sendLeaderboard() {
    std::lock_guard<std::mutex> lock(m_mutex);
    std::string leaderboard = "LEADERBOARD:";
    for (const auto& player : m_players_list) {
        leaderboard += player->getNick() + "," + std::to_string(player->getPoints()) + ";";
    }
    if (!leaderboard.empty()) {
        leaderboard.pop_back(); 
    }
    broadcast(leaderboard);
}

void Room::gameLoop() {
    while (true) {
        
        {
            std::lock_guard<std::mutex> lock(m_mutex);
            if (m_current_round >= m_max_round || m_game_state != IN_PROGRESS) {
                break; 
            }
        }

        startNewRound();
        sendLeaderboard();
        std::unique_lock<std::mutex> lock(m_mutex); 
        while (m_game_state == IN_PROGRESS) { 
            if (m_unrevealed_indices.size() <= m_password.length() * 0.5 || m_round_over) {
                break; 
            }
            
            bool notified = m_guess_cv.wait_for(lock, std::chrono::seconds(5), [this] {
                return m_round_over || m_game_state != IN_PROGRESS;
            });
            
            if (!notified && m_game_state == IN_PROGRESS) {
                if (revealRandomLetter()) {
                    std::cout << "Revealed a letter: " << m_hashed_password << std::endl;
                    broadcast("HASHPASS:" + m_hashed_password);
                }
            } 
        }

        if (m_game_state == IN_PROGRESS && !m_round_over) {
            broadcast("TIMEOUT: Ostatnia szansa! 10 sekund...");
            m_guess_cv.wait_for(lock, std::chrono::seconds(10), [this] {
                return m_round_over || m_game_state != IN_PROGRESS;
            });
        }

        if (m_game_state == IN_PROGRESS) {
            if (m_round_over) {
                broadcast("INFO: Hasło odgadnięte! Przerwa 5s.");
            } else {
                broadcast("ROUND_OVER:" + m_password);
            }
            
            lock.unlock();
            std::this_thread::sleep_for(std::chrono::seconds(5));
            lock.lock();
        }
    }

    if (m_game_state != FINISHED) { 
        finishGame();
        sendLeaderboard();
    }
}

void Room::finishGame() {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_game_state = FINISHED;
    broadcast("GAME_OVER");
}

bool Room::validateNick(const std::string& nick) {
    for (const auto& player : m_players_list) {
        if (player->getNick() == nick) {
            return false; 
        }
    }
    return true;
}

bool Room::addPlayer(Player* player) {

    std::lock_guard<std::mutex> lock(m_mutex);
    
    if (m_players_list.size() >= MAX_PLAYERS) {
        player->sendMessage("ERROR_FULL_ROOM: Pokój jest pełny.");
        return false; 
    }

    if(m_game_state != WAITING) {
        player->sendMessage("ERROR_GAME_STARTED: Gra już się rozpoczęła. Nie można dołączyć do pokoju.");
        return false; 
    }
    if (!validateNick(player->getNick())) {
        player->sendMessage("ERROR_NICK_TAKEN: Nick jest już zajęty w tym pokoju.");
        return false; 
    }

    if (!player) return false;
    broadcast("PLAYER_JOINED:" + player->getNick());
    m_players_list.push_back(player);
    return true;
}

Player* Room::removePlayer(int sockDes) {
    std::lock_guard<std::mutex> lock(m_mutex);
    Player* removed_player = nullptr;
    auto it = std::remove_if(m_players_list.begin(), m_players_list.end(), 
        [&](Player* p){
            if (p->getSockDes() == sockDes) {
                removed_player = p; 
                return true; 
            }
            return false;
        });
        
    if (removed_player) {
        m_players_list.erase(it, m_players_list.end());
        broadcast("PLAYER_LEFT:" + removed_player->getNick());
        if (removed_player == m_host) {
            if (!m_players_list.empty()) {
                m_host = m_players_list.front(); 
                broadcast("HOST_CHANGE:" + m_host->getNick());
            } else {
                m_host = nullptr; 
            }
        }
    }
    
    return removed_player; 
}





