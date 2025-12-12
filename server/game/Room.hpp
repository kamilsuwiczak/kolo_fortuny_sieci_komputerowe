#include <stdio.h>
#include <unistd.h>
#include <algorithm>
#include <chrono>
#include <random>
#include <iostream>
#include "Player.hpp"
#include <condition_variable>
#include <thread>
#pragma once

enum GameState {
    WAITING,
    IN_PROGRESS,
    FINISHED
};

class Room{
private:
    // Zarządzanie pokojem
    int m_room_number;
    std::vector<Player*> m_players_list; 
    Player* m_host;                      
    std::mutex m_mutex;         
    static const int MAX_PLAYERS = 6;
    const std::vector<std::string>& m_password_source;   
    
    // Logika gry
    std::thread m_game_thread;           
    std::string m_password;                     
    std::string m_hashed_password;             
    std::vector<int> m_unrevealed_indices; 
    bool m_round_over;  
    std::condition_variable m_guess_cv; // Do powiadamiania o zgadnięciu
    
    // Stan gry i rund
    GameState m_game_state; 
    int m_current_round;
    int m_max_round;
    
    
    void broadcast(const std::string& message); // Wysyłanie wiadomości do wszystkich
    void gameLoop(); 
    void sendStateToAll(); // Wysyła m_hashed_password
    void finishGame();
    public:
    
    
    Room(int roomNumber, Player* host, const std::vector<std::string>& passwordSource); 
    
    ~Room();
    // Gettery
    int getRoomNumber() const { return m_room_number; }
    const std::string& getPassword() const { return m_password; }
    const std::string& getHashedPassword() const { return m_hashed_password; }
    GameState getGameState() const { return m_game_state; }
    std::vector<int> getUnrevealedLetterIndices() const { return m_unrevealed_indices; }
    std::thread& getGameThread() { return m_game_thread; }
    GameState& getGameStateRef() { return m_game_state; }
    bool& getRoundOverRef() { return m_round_over; }
    int getPlayersCount() const { return m_players_list.size(); }
    
    // metody rundy i gry
    void generatePassword(const std::vector <std::string>& WORDS);
    void generateHashedPassword();
    void generateUnrevealedLetterIndices();
    bool revealRandomLetter();
    void startNewRound();
    void startGame(int maxRounds); 

    //  zarządzanie graczami
    bool validateNick(const std::string& nick);
    bool addPlayer(Player* player); 
    Player* removePlayer(int sockDes);
    void processGuess(Player* player, const std::string& guess); 
};

