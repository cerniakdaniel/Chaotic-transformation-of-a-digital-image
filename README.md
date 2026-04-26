# 🔷Image Scrambling Visualizer — Multi-Stage Transformation



### Interaktywna wizualizacja chaotycznych przekształceń obrazu zbudowana w Pythonie (PyQt6 + NumPy)



### 📖Opis projektu



Aplikacja pozwala krok po kroku obserwować działanie dwóch algorytmów geometrycznych:

\- **Etap 1** — **Naiwny scrambling** — permutacja wierszy i kolumn obrazu

\- **Etap 2** — **Permutacja Fisher-Yates** — losowe przemieszanie wszystkich pikseli

\- **Etap 3** — **Permutacja + substytucja** — zmiana pozycji i wartości pikseli



### 🚀Uruchomienie



Projekt wymaga Pythona oraz kilku bibliotek:



1\. Zainstaluj zależności:

`pip install PyQt6 numpy pillow`

2\. Uruchom aplikację:

`python main.py`

3\. Gotowe✅



### 🎮Jak używać



&#x20;         Akcja           |              Opis               

\-------|-----

&#x20;    Wczytaj obraz       | Przeciągnij plik lub kliknij pole

&#x20;    Scramble        | Przekształca obraz

&#x20;  Unscramble (dobry klucz)   | Odtwarza obraz

&#x20;   Unscramble (zły klucz)      | Pokazuje efekt błędu

&#x20;        Zapis            | Zapisuje obrazy do folderu

&#x20;       Klucz         | Seed sterujący algorytmem




### 📂Struktura projektu



project/
├── main.py
├── stage1.py
├── stage2.py
├── stage3.py
├── metrics.py
└── uwb.png



### 🛠Technologie



\- **PyQt6** — interfejs graficzny

\- **NumPy** — operacje na obrazach

\- **Pillow** — wczytywanie i zapis obrazów



### 📊Metryki



Aplikacja analizuje:

\- korelację pikseli

\- entropię Shannon’a

\- średnią różnicę bezwzględną (MAD)



### ⚠️ Uwagi



Projekt ma charakter edukacyjny.

Nie jest to bezpieczny system szyfrowania — pokazuje jedynie:

\- działanie permutacji i substytucji

\- wpływ klucza na wynik

\- różnicę między „chaosem” a bezpieczeństwem



### 👨‍🎓 Autor



Daniel Czerniak

Informatyka — II rok

Filia UWB w Wilnie

##### 

