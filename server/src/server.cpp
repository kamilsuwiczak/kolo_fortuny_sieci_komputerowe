#include "Server.hpp"
#include <iostream>
#include <cstdlib>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <cstring>
#include <algorithm>
#include <sstream>
#include "../game/Player.hpp"
#include "../game/Room.hpp"


Server::Server(int port) : m_listen_fd(-1) {
    std::cout << "Inicjalizacja serwera..." << std::endl;
    setup_listening_socket(port);
}

Server::~Server() {
    std::cout << "Zamykanie serwera..." << std::endl;
    
    if (m_listen_fd != -1) {
        close(m_listen_fd);
    }
    
    for (auto const& [fd, player] : m_fd_to_player) {
        close(fd);
        delete player;
    }
    m_fd_to_player.clear();
    
    for (auto const& [id, room] : m_active_rooms) {
        delete room; 
    }
    m_active_rooms.clear();

    m_player_to_room.clear(); 
    std::cout << "Zasoby serwera zwolnione." << std::endl;
}

void Server::setup_listening_socket(int port) {
    m_listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (m_listen_fd == -1) {
        throw std::runtime_error("Blad: Nie udalo sie utworzyc gniazda.");
    }

    int opt = 1;
    if (setsockopt(m_listen_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        std::cerr << "Ostrzeżenie: setsockopt(SO_REUSEADDR) nie powiodlo sie." << std::endl;
    };

    sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = INADDR_ANY; 
    memset(&(server_addr.sin_zero), 0, sizeof(server_addr.sin_zero));

    if (bind(m_listen_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        close(m_listen_fd);
        throw std::runtime_error("Blad bind: Port " + std::to_string(port) + " jest zajety.");
    }

    if (listen(m_listen_fd, MAX_CONNECTIONS) < 0) {
        close(m_listen_fd);
        throw std::runtime_error("Blad listen.");
    }

    pollfd listen_fd_entry = { m_listen_fd, POLLIN, 0 };
    m_fds.push_back(listen_fd_entry);
    
    std::cout << "Serwer nasłuchuje na porcie " << port << std::endl;
}


void Server::handle_new_connection(int listen_fd) {
    sockaddr_storage client_addr; 
    socklen_t addr_size = sizeof(client_addr);
    int client_fd = accept(listen_fd, (struct sockaddr*)&client_addr, &addr_size);

    if (client_fd < 0) {
        std::cerr << "Blad accept: " << strerror(errno) << std::endl;
        return;
    }

    pollfd new_fd_entry = { client_fd, POLLIN, 0 };
    m_fds.push_back(new_fd_entry);
    
    Player* new_player = new Player(client_fd, "TEMP_NICK");
    m_fd_to_player[client_fd] = new_player;

    new_player->sendMessage("WELCOME");
    std::cout << "Nowe połączenie zaakceptowane. FD: " << client_fd << std::endl;
}

void Server::handle_client_data(size_t i) {
    int client_fd = m_fds[i].fd;
    char buffer[BUFFER_SIZE];
    
    ssize_t bytes_read = recv(client_fd, buffer, BUFFER_SIZE - 1, 0);

    if (bytes_read <= 0) {
        std::cout << "Klient rozłączony. FD: " << client_fd << std::endl;
        cleanup_player(m_fd_to_player[client_fd]); 
        close(client_fd);
        m_fds.erase(m_fds.begin() + i); 
        
    } else {
        buffer[bytes_read] = '\0'; 
        std::cout << "Odebrano od FD " << client_fd << ": " << buffer << std::endl;
        process_command(m_fd_to_player[client_fd], buffer);
    }
}
 
//Reszta metod in progress

