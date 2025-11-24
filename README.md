# kolo_fortuny_sieci_komputerowe

Zespół:
Kamil Suwiczak
Marcin Kaczor

Gra a'la koło fortuny

Gracz łączy się do serwera. Ma do wyboru opcję: stwórz własny pokój i dołącz za pomocą kodu.
Podczas dołączania do pokoju gracz musi wpisać nick, jeśli jest zajęty to musi wybrać inny.
Jeśli wybierze stwórz własny pokój to generowany jest kod, aby inni gracze mogli dołączyć, jeśli dołącz za pomocą kodu to musi wpisać kod gry.
Osoba która stwarza pokój ma przycisk start, aby rozpocząć grę oraz ustawia ile rund gry się odbędzie.
Jeśli osoba która stworzyła pokój go opuści to "zarządcą" pokoju jest osoba która dołączyła najwcześniej.
Po rozpoczęciu gry kolejni gracze nie mogą już dołączyć.

Serwer z danego zbioru losuje hasło, następnie zamienia hasło w _ np. rower -> _ _ _ _ _ co kilka sekund losowo odkrywa daną literkę tworząc np. r _ w _ _. 
Zadaniem graczy jest wpisywanie haseł do momentu zgadnięcia hasła. Po stronie klienta będzie zaimplementowane zapamiętywanie wpisanych wcześniej haseł (tak aby gracz wiedział co wpisał). 
Serwer oczekuje na wpisywanie słów od graczy.
W przypadku, gdy dwóch graczy odgadnie hasło wygrywa ten, który będzie pierwszy.

Za każde odgadnięte hasło określony gracz dostaje punkt.
Na końcu gry pokazuje się ranking, kto ile punktów zdobył i na którym jest miejscu.
Po skończeniu gry pokazują się opcję: wróć do pokoju, wyjdź z pokoju.
