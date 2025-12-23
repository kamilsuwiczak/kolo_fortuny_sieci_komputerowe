wiadomosci wysylane do serwera i z serwera powinny zaczynac sie wielkimi literami a po nich wiadomosc


**Wiadomosci wysylane przez serwer:**

* NEW_ROUND:3 - numer rundy
* CORRECT:Kamil;GUESS:odganięte_haslo - poprawne zgadniecie gracza Kamil hasla odgadniete_haslo
* INCORRECT:Kamil;GUESS:nieodgadniete_haslo - niepoprawne zgadniecie gracza Kamil hasla nieodgadniete_haslo
* TIMEOUT: Ostatnia szansa. Oczekiwanie 10s... - czas do zakończenia rundy
* INFO: Przejście do następnej rundy za 3s. - info o przejsciu do następnej rundy
* GAME_OVER - koniec gry
* ERROR_FULL_ROOM: Pokój jest pełny.
* ERROR_GAME_STARTED: Gra już się rozpoczęła. Nie można dołączyć do pokoju.
* ERROR_NICK_TAKEN: Nick jest już zajęty w tym pokoju.
* ERROR_WRONG_ROOM_CODE
* PLAYER_LEFT:Marcin - gracz o nicku Marcin wyszedł z gry
* HOST_CHANGE:Martyna - gracz o nicku Martyna jest nowym hostem

* PLAYERS:Player1,Player2,Player3 - lista graczy
* ROOM_CODE:ZAQ1 - kod pokoju dla hosta
* HASHPASS:_1_1__ - zakodowane haslo
* 


**Wiadomosci wysylane przez clienta:**
* GUESS slowo - zgadywane slowo
* START_GAME - wiadomosc wysylana w chwili startu gry
* LEAVE_GAME - wiadomosc wysylana w chwili gdy ktos chce opuscic pokoj
* JOIN_ROOM nr_pokoju nick_gracza - prośba o dołączenie do pokoju
* CREATE_ROOM nick - prośba o utworzenie pokoju
