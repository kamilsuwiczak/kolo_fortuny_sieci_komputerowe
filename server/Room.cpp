#include <stdio.h>
#include <unistd.h>
#include <algorithm>
#include <chrono>
#include <random>
#include <iostream>
#include "Room.hpp"
#include <thread>

Room::Room(int roomNumber, Player* host):
m_room_number(roomNumber),m_host(host),m_current_round(0), m_max_round(3){}

Room::~Room() {}


bool Room::validateNick(const std::string& nick) {
    std::lock_guard<std::mutex> lock(m_mutex);
    for (int i = 0; i < m_players_list.size(); i++) {
        if (m_players_list[i]->getNick() == nick) {
            return false; 
        }
    }
    return true;
}

bool Room::addPlayer(Player* player) {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_players_list.push_back(player);
    broadcast("NEW PLAYER " + player->getNick());
    std::cout << "Player added: " << player->getNick() << std::endl;
    return true;
    
}

bool Room::removePlayer(int sockDes) {
    std::lock_guard<std::mutex> lock(m_mutex);
    auto it = std::remove_if(m_players_list.begin(), m_players_list.end(),
                             [sockDes](Player* player) {
                                 return player->getSockDes() == sockDes;
                             });
    if (it != m_players_list.end()) {
        m_players_list.erase(it, m_players_list.end());
        return true;
    }
    return false;
}

void Room::generatePassword(){
    static std::vector <std::string> WORDS = {"cat", "duck", "horse"};
    std::random_device rd;               
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, WORDS.size() - 1 );

    m_password = WORDS[dist(gen)];
    std::cout<<"Generated password: " << m_password <<std::endl;
}   

void Room::generateHashedPassword(){
    m_hashed_password = "";
    for (int i = 0; i<m_password.length();i++){
        m_hashed_password += "_";
    }
    std::cout<<"Generated hashed password: " << m_hashed_password <<std::endl;
}

void Room::generateUnrevealedLetterIndices(){
    for (int i =0;i<getPassword().length();i++){
        m_unrevealed_indices.push_back(i);
    }
    std::cout<<"Generated unrevealed letter indices: ";
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
    std::cout<<"Revealed letter at position: " << letterPos <<std::endl;
    return true; 
}

void Room::startNewRound(){
    std::lock_guard<std::mutex> lock(m_mutex);
    m_current_round++;
    m_round_over = false;
    m_unrevealed_indices.clear();
    generatePassword();
    generateHashedPassword();
    generateUnrevealedLetterIndices();
    broadcast("NEW ROUND " + std::to_string(m_current_round));
    sendStateToAll();
    std::cout<<"Started new round: " << m_current_round <<std::endl;
}

void Room::startGame(int maxRound){
    m_max_round = maxRound;
    m_game_state = IN_PROGRESS;
   m_game_thread = std::thread(&Room::gameLoop, this);
}

void Room::broadcast(const std::string& message) {
    for (auto& player : m_players_list) {
        player->sendMessage(message);
    }
}

void Room::sendStateToAll() {

    broadcast("HASHPASS " + m_hashed_password);
}

void Room::gameLoop() {
    while (true) {
        {
            std::lock_guard<std::mutex> lock(m_mutex);
            if (m_current_round >= m_max_round) {
                break; 
            }
        }

        startNewRound();

        std::unique_lock<std::mutex> lock(m_mutex);
        while (m_game_state == IN_PROGRESS ) {
            if (m_unrevealed_indices.size() <= m_password.length() * 0.5 || m_round_over) {
                     break; 
            }

           bool timed_out = m_guess_cv.wait_for(lock, std::chrono::seconds(10)) == std::cv_status::timeout;
            
            if (timed_out && m_game_state == IN_PROGRESS) {
                if (revealRandomLetter()) {
                sendStateToAll();
                }
            }
            
        }
        if (m_game_state == IN_PROGRESS) {
            
            bool was_guessed;
            {
                 std::lock_guard<std::mutex> lock(m_mutex);
                 was_guessed = m_round_over;
            }
            
            if (!was_guessed) {
                broadcast("TIMEOUT: Ostatnia szansa. Oczekiwanie 10s...");
                std::this_thread::sleep_for(std::chrono::seconds(10)); 
            } else {
                broadcast("INFO: Przejście do następnej rundy za 3s.");
                std::this_thread::sleep_for(std::chrono::seconds(3)); 
            }
        }
    }

    if (m_game_state != FINISHED) { 
        finishGame();
    }
}

void Room::finishGame() {
    std::lock_guard<std::mutex> lock(m_mutex);
    m_game_state = FINISHED;
    broadcast("GAME OVER " + m_password);
}





