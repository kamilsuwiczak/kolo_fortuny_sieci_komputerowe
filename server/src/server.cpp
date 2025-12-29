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

    if (listen(m_listen_fd, SOMAXCONN) < 0) {
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
    
    Player* new_player = new Player(client_fd);
    m_fd_to_player[client_fd] = new_player;

    new_player->sendMessage("WELCOME");
    std::cout << "Nowe połączenie zaakceptowane. FD: " << client_fd << std::endl;
}

bool Server::handle_client_data(size_t i) {
    int client_fd = m_fds[i].fd;
    char buffer[BUFFER_SIZE];
    
    ssize_t bytes_read = recv(client_fd, buffer, BUFFER_SIZE - 1, 0);

    if (bytes_read <= 0) {
        std::cout << "Klient rozłączony. FD: " << client_fd << std::endl;
        cleanup_player(m_fd_to_player[client_fd]); 
        close(client_fd);
        m_fds.erase(m_fds.begin() + i); 
        return true;

        
    } else {
        buffer[bytes_read] = '\0'; 
        std::cout << "Odebrano od FD " << client_fd << ": " << buffer << std::endl;
        process_command(m_fd_to_player[client_fd], buffer);
        return false;
    }
}

bool Server::validate_nick(const std::string& nick) {
    if (nick.empty()) {
        return false;
    }
    if (nick.length() < 3 || nick.length() > 20) {
        return false;
    }
    for (char c : nick) {
        if (std::isspace(c)) {
            return false;
        }
    }
    return true;
}

void Server::remove_player_from_room(Player* player) {
    if (m_player_to_room.count(player)) {
        Room* room = m_player_to_room[player];
        
        room->removePlayer(player->getSockDes());
        m_player_to_room.erase(player);

        if (room->getPlayersList().empty()) {
            int r_id = room->getRoomNumber();
            m_active_rooms.erase(r_id);
            delete room; 
            std::cout << "Pokój " << r_id << " usunięty (pusty)." << std::endl;
        }
    }
}

void Server::cleanup_player(Player* player) {
    remove_player_from_room(player);
    
    m_fd_to_player.erase(player->getSockDes());
    delete player;
}

void Server::handle_join_room(Player* player, std::istringstream& iss) {
    std::string room_id_str, nick;
    iss >> room_id_str >> nick;

    if (m_player_to_room.count(player)) {
        player->sendMessage("ERROR: Już jesteś w pokoju.");
        return;
    }

    if (room_id_str.empty()) {
        player->sendMessage("ERROR_INVALID_ROOM_ID: Nieprawidłowy identyfikator pokoju.");
        return;
    }

    if (!validate_nick(nick)) {
        player->sendMessage("ERROR_INVALID_NICK: Nieprawidłowy nick.");
        return;
    }

    int r_id;
    try {
        r_id = std::stoi(room_id_str);
    } catch (const std::exception& e) {
        player->sendMessage("ERROR_INVALID_ROOM_ID: Nieprawidłowy identyfikator pokoju.");
        return;
    }

    auto it = m_active_rooms.find(r_id);
    if (it == m_active_rooms.end()) {
        player->sendMessage("ERROR_ROOM_NOT_FOUND: Pokój " + room_id_str + " nie istnieje.");
        return;
    }

    Room* room = it->second;
    player->setNick(nick);
    
    if (room->addPlayer(player)) {
        m_player_to_room[player] = room;
        
    }
}

void Server::handle_create_room(Player* player, std::istringstream& iss) {
    if (m_player_to_room.count(player)) {
        player->sendMessage("ERROR: Już jesteś w pokoju.");
        return;
    }

    std::string nick;
    iss >> nick;
    if (!validate_nick(nick)) {
        player->sendMessage("ERROR_INVALID_NICK: Nieprawidłowy nick.");
        return;
    }
    player->setNick(nick);

    static int next_room_number = 1;

    Room* new_room = new Room(next_room_number, player, m_password_source);

    m_active_rooms[next_room_number] = new_room;
    m_player_to_room[player] = new_room;
    player->sendMessage("ROOM_CREATED:" + std::to_string(next_room_number));
    next_room_number = (next_room_number % 9999) + 1;

}

void Server::handle_start_game(Player* player, std::istringstream& iss) {
    if (!m_player_to_room.count(player)) {
        player->sendMessage("ERROR: Nie jesteś w pokoju.");
        return;
    }

    Room* room = m_player_to_room[player];
    if (room->getPlayersList().empty() || room->getPlayersList().front() != player) {
        player->sendMessage("ERROR_NOT_HOST: Tylko gospodarz może rozpocząć grę.");
        return;
    }

    std::string max_rounds_str;
    iss >> max_rounds_str;
    int max_rounds = 3;
    try {
        max_rounds = std::stoi(max_rounds_str);
        if (max_rounds <= 0 || max_rounds > 20) {
            throw std::out_of_range("Invalid range");
        }
    } catch (const std::exception& e) {
        player->sendMessage("ERROR_INVALID_ROUNDS: Nieprawidłowa liczba rund.");
        return;
    }

    room->startGame(max_rounds);
}

void Server::handle_guess(Player* player, std::istringstream& iss) {
    if (!m_player_to_room.count(player)) {
        player->sendMessage("ERROR: Nie jesteś w pokoju.");
        return;
    }

    Room* room = m_player_to_room[player];
    std::string guess;
    iss >> guess;

    room->processGuess(player, guess);
}

void Server::handle_leave_game(Player* player) {
    remove_player_from_room(player);
    player->sendMessage("LEFT_ROOM");

}

void Server::process_command(Player* player, const std::string& command_line) {
    std::istringstream iss(command_line);
    std::string cmd;
    iss >> cmd;

    if (cmd == "JOIN_ROOM") {
        handle_join_room(player, iss);
    } else if (cmd == "CREATE_ROOM") {
        handle_create_room(player, iss);
    } else if (cmd == "START_GAME") {
        handle_start_game(player, iss);
    }
    else if (cmd == "GUESS") {
        handle_guess(player, iss);
    } 
    else if (cmd == "LEAVE_ROOM") {
        handle_leave_game(player);
    }
    else {
        player->sendMessage("ERROR_UNKNOWN_COMMAND: Niepoprawna wiadomość.");
    }
}

void Server::run() {

    while (true) {

        int poll_count = poll(m_fds.data(), m_fds.size(), -1);

        if (poll_count < 0) {
            if (errno == EINTR) continue;
            std::cerr << "Błąd poll(): " << strerror(errno) << std::endl;
            break;
        }

        for (size_t i = 0; i < m_fds.size(); ++i) {
            
            if (m_fds[i].revents & POLLIN) {
                
                if (m_fds[i].fd == m_listen_fd) {
                    handle_new_connection(m_listen_fd);
                } 

                else {
                    bool removed = handle_client_data(i);
                    if (removed) {
                        --i; 
                    }
                }
            }
            
            else if (m_fds[i].revents & (POLLERR | POLLHUP)) {
                std::cout << "Błąd lub rozłączenie na FD: " << m_fds[i].fd << std::endl;
                cleanup_player(m_fd_to_player[m_fds[i].fd]);
                close(m_fds[i].fd);
                m_fds.erase(m_fds.begin() + i);
                --i;
            }
        }
    }
}

