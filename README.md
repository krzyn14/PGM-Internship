# PGM - **Odpowiedzi na pytania do stażu**

 **1.** Rozwiązanie do zadania pierwszego zostało przygotowane w folderze
        _PGM/exercise_1_, gdzie znajduje się kod do utworzenia bazy danych SQLite
        i wgraniu danych meczowych ze Statsbomb (*import_csv.py*), a także
        kod, który wylicza xG diff dla każdego stanu meczu dla obu drużyn i
        przedstawia wynik w postaci tabeli wraz z liczbą oddanych strzałów i
        xg_for/xg_against, a także grafiki (*calculate_xg.py*). 
        Dodatkowo w pliku _guide.md_ znajduje się instrukcja jak wykonać program.

**xG Difference in each Game State:**

 | team_name                   | game_state | shots_for | shots_against | xg_for | xg_against | xg_difference |
|-----------------------------|------------|----------:|--------------:|-------:|-----------:|--------------:|
| Polonia Bytom               | drawing    | 17        | 10            | 0.923  | 0.609      | 0.314         |
| Polonia Bytom               | winning    | 1         | 2             | 0.066  | 0.017      | 0.050         |
| Polonia Bytom               | losing     | 2         | 2             | 0.079  | 0.117      | -0.038        |
| Pogoń Grodzisk Mazowiecki   | drawing    | 10        | 17            | 0.609  | 0.923      | -0.314        |
| Pogoń Grodzisk Mazowiecki   | winning    | 2         | 2             | 0.117  | 0.079      | 0.038         |
| Pogoń Grodzisk Mazowiecki   | losing     | 2         | 1             | 0.017  | 0.066      | -0.050        |

**W postaci grafiki:**
<img width="2400" height="1000" alt="image" src="https://github.com/user-attachments/assets/af8bce97-022a-4c19-aaed-fd2e3b609832" />

 **2.** Rozwiązanie zadania drugiego ma formę opisową. Odpowiedź zawarta jest w folderze _PGM/exercise_2_ w pliku _analiza_wahadlowego.md_, gdzie skrupulatnie opisałem metodologię jaką obrałbym przygotowując analizę dla sztabu pierwszej drużyny Pogoni.
