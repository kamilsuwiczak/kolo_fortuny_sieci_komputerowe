TARGET = game_server
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -pthread -I.
BUILD_DIR = build

SRCS = main.cpp \
       src/server.cpp \
       game/Room.cpp \
       

OBJS = $(SRCS:%.cpp=$(BUILD_DIR)/%.o)

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

	@echo " Sukces! Plik binarny: ./$(TARGET)"

$(BUILD_DIR)/%.o: %.cpp
	@mkdir -p $(dir $@)  
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR) $(TARGET)
	@echo "Folder $(BUILD_DIR) i plik $(TARGET) zostały usunięte."

rebuild: clean all

.PHONY: all clean rebuild