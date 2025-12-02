#include <stdio.h>
#include <unistd.h>
#include <algorithm>
#include <chrono>
#include <random>
#include <iostream>
#include "Room.hpp"


static std::vector <std::string> WORDS = {"cat", "duck", "horse"};

Room::Room(int roomNumber):
roomNumber(roomNumber),currentRound(0), maxRound(3){}

