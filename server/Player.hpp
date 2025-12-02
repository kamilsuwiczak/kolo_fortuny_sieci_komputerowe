#include <stdio.h>
#include <unistd.h>
#include <iostream>

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

    int addPoint(){
        points++;
    }
    
};