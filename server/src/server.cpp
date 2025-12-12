#include <iostream>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/un.h>
#include <netinet/in.h>
#include <map>
#include "../game/Player.hpp"
#include "../game/Room.hpp"
#include <random>

#define MAX_CONNECTIONS 10

std::map<int, Player*> fd_to_player;
std::map<Player*, Room*> player_to_room;


int setup_socket(){
    int server_fd = socket(AF_INET6, SOCK_STREAM, 0);
    if (server_fd == -1) {
        std::cerr << "Failed to create socket" << std::endl;
        exit(EXIT_FAILURE);
    }

    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
    std::cerr << "setsockopt(SO_REUSEADDR) failed" << std::endl;
    }   

    int disable_v6_only = 0;
    if (setsockopt(server_fd, IPPROTO_IPV6, IPV6_V6ONLY, &disable_v6_only, sizeof(disable_v6_only))) {
    std::cerr << "setsockopt(IPV6_V6ONLY) failed" << std::endl;
    }

    sockaddr_in6 server_addr6;
    server_addr6.sin6_family = AF_INET6;
    server_addr6.sin6_addr = in6addr_any;
    server_addr6.sin6_port = htons(8080);

    if (bind(server_fd, (struct sockaddr*)&server_addr6, sizeof(server_addr6)) < 0) {
        std::cerr << "Bind failed" << std::endl;
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    if (listen(server_fd, MAX_CONNECTIONS) < 0) {
        std::cerr << "Listen failed" << std::endl;
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    return server_fd;
    
}


int main(int agc, char *argv[]){

    



    return 0;
}