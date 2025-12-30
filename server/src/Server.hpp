#pragma once

#include <iostream>
#include <map>
#include <vector>
#include <poll.h>      
#include <netinet/in.h> 
#include <string>
#include <sys/socket.h>

class Player; 
class Room; 

#define BUFFER_SIZE 1024
#define DEFAULT_PORT 8080

class Server {
private:
    int m_listen_fd; 
    std::vector<pollfd> m_fds; 

    std::map<int, Player*> m_fd_to_player; 
    
    std::map<Player*, Room*> m_player_to_room; 
    
    std::map<int, Room*> m_active_rooms; 
    
    const std::vector<std::string> m_password_source = {"CAT", "DUCK", "HORSE", "SERVER", "COMPUTER", "KEYBOARD", "MOUSE", "MONITOR", "PRINTER", "LAPTOP", "DOG", "BIRD", "FISH", "ELEPHANT", "TIGER", "LION", "BEAR", "WOLF", "FOX", "SNAKE", "CROCODILE", "GIRAFFE", "ZEBRA", "KANGAROO", "PENGUIN", "DOLPHIN", "SHARK", "WHALE", "OCTOPUS", "CRAB", "LOBSTER"};

    void setup_listening_socket(int port);

    void handle_new_connection(int listen_fd);

    bool handle_client_data(size_t i);
    
    void process_command(Player* player, const std::string& command_line);

    void remove_player_from_room(Player* player);

    bool validate_nick(const std::string& nick);

    void handle_join_room(Player* player, std::istringstream& iss);
    void handle_create_room(Player* player, std::istringstream& iss);
    void handle_start_game(Player* player, std::istringstream& iss);
    void handle_guess(Player* player, std::istringstream& iss);
    void handle_leave_game(Player* player);

public:
    Server(int port = DEFAULT_PORT);
    ~Server();
    void run(); 
    
    void cleanup_player(Player* player);
};