#pragma once
#include <stdio.h>
#include <unistd.h>
#include <iostream>
#include <sys/socket.h>

class Player{
private:
    std::string nick;
    int sockDes;
    int points;

public:

   Player(int sockDes, const std::string& nick)
    : sockDes(sockDes), nick(nick), points(0) {}


    std::string getNick(){
        return nick;
    }

    int getSockDes(){
        return sockDes;
    }

    int getPoints(){
        return points;
    }

    void addPoint(){
        points++;
    }

    virtual int sendMessage(const std::string& message){
        std::string final_message = message + '\n';
        return send(getSockDes(), final_message.c_str(), final_message.length(), 0);
    }
    
    virtual ~Player() {}
};