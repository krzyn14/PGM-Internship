## Instrukcja jak uruchomić program do obliczenia xG diff dla każdego stanu meczu dla obu zespołów

### Wymagania

- Python 3.10 lub nowszy
- biblioteki wymienione w `requirements.txt`

### 1. Utworzenie środowiska wirtualnego

```bash
python3 -m venv .venv
```

Aktywacja na macOS/Linux:

```bash
source .venv/bin/activate
```

Aktywacja na Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Instalacja zależności

```bash
python -m pip install -r requirements.txt
```

### 3. Import danych do SQLite

Plik z danymi meczowymi powinien znajdować się w katalogu:

```text
exercise_1/data
```

Następnie należy uruchomić:

```bash
python exercise_1/import_csv.py
```

Skrypt utworzy bazę SQLite i zaimportuje dane do tabeli `events_raw`.

Ten krok może być pominięty z racji tego, że baza została zaimportowana do repozytorium.

### 4. Obliczenie xG difference

Aby obliczyć różnicę xG dla każdego stanu meczu, należy uruchomić:

```bash
python exercise_1/calculate_xg.py
```

Skrypt:

- pobiera unikalne strzały z bazy SQLite;
- ustala wynik przed każdym strzałem;
- przypisuje strzał do stanu `drawing`, `winning` lub `losing`;
- oblicza `xG for`, `xG against` oraz `xG difference`;
- wyświetla tabelę wynikową w terminalu;
- zapisuje wykres w formacie PNG.

### Wynik działania

W terminalu zostanie wyświetlona tabela:

```text
Expected Goals Difference by Game State
```

Wygenerowany wykres zostanie zapisany w katalogu:

```text
exercise_1/reports/xg_difference_by_game_state.png
```
