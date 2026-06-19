# Specificații Aplicație TODO (Command Line REPL)

Aplicația trebuie să fie scrisă în Python și să funcționeze ca un REPL (Read-Eval-Print Loop) în linia de comandă.

## Funcționalități necesare:
1. Adăugare sarcină: utilizatorul scrie o comandă pentru a adăuga un TODO (ex: `add Cumpără pâine`).
2. Listare sarcini: comandă pentru a vedea toate sarcinile (ex: `list`).
3. Marcare ca rezolvat: comandă pentru a bifa un TODO ca finalizat (ex: `done 1`).
4. Ștergere sarcină: comandă pentru a șterge un TODO (ex: `delete 1`).
5. Ieșire: comanda `exit`.

Datele trebuie să fie salvate într-un fișier local `todos.json` pentru ca sarcinile să nu se piardă la închiderea aplicației.
