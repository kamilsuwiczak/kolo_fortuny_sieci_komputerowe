#include "src/Server.hpp"
#include <iostream>
#include <stdexcept>

int main(int argc, char* argv[]) {
    int port = 8080;
    if (argc > 1) {
        try {
            port = std::stoi(argv[1]);
        } catch (...) {
            std::cerr << "Nieprawidłowy port. Używam domyślnego: 8080" << std::endl;
        }
    }

    try {
        Server server(port);
        server.run();

    } catch (const std::exception& e) {
        std::cerr << "BŁĄD KRYTYCZNY: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}