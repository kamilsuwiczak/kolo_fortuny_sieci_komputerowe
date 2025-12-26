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
    
    const std::vector<std::string> m_password_source = {"CAT", "DUCK", "HORSE", "SERVER"};

    void setup_listening_socket(int port);

    void handle_new_connection(int listen_fd);

    bool handle_client_data(size_t i);
    
    void process_command(Player* player, const std::string& command_line);

    bool validate_nick(const std::string& nick);

public:
    Server(int port = DEFAULT_PORT);
    ~Server();
    void run(); 
    
    void cleanup_player(Player* player);
};