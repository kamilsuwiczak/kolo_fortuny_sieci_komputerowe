#include <stdio.h>
#include <unistd.h>
#include <algorithm>
#include <chrono>
#include <random>
#include <iostream>
#include "Player.hpp"


class Room{
private:
    int roomNumber;
    std::vector <Player> playersList; 
    std::string password;
    std::string hashedPassword;
    std::vector <int> unreavealedLetterIndices;
    std::string gameState;
    std::string roundState;
    int currentRound;
    int maxRound;
    
public:
    Room(int roomNumber);

    int getRoomNumber(){
        return roomNumber;
    }
    std::string getPassword(){
        return password;
    }
    std::string getHashedPassword(){
        return hashedPassword;
    }

    void generatePassword(){
    
    }
    void generateHashedPassword(){

    }
    void generateUnreavealedLetterIndices(){

    }
    void revealLetter(){
        
    }
    void startNewRound(){

    }
    void startGame(){

    }
    void broadcast(){

    }

    bool addPlayer(Player *player){

    }
    bool removePlayer(int sockDes){

    }


};