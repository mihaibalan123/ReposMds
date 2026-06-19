import json
import os

DATA_FILE = "todos.json"


def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save_todos(todos):
    with open(DATA_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def next_id(todos):
    return max((t["id"] for t in todos), default=0) + 1


def cmd_add(todos, args):
    text = " ".join(args)
    if not text:
        print("Specifică textul sarcinii.")
        return
    todo = {"id": next_id(todos), "text": text, "done": False}
    todos.append(todo)
    save_todos(todos)
    print(f"Adăugat: {todo['text']} (id: {todo['id']})")


def cmd_list(todos, _args):
    if not todos:
        print("Lista de sarcini este goală.")
        return
    for t in todos:
        status = "\u2713" if t["done"] else "\u25CB"
        print(f"  [{status}] {t['id']}. {t['text']}")


def cmd_done(todos, args):
    if not args:
        print("Folosire: done <id>")
        return
    try:
        tid = int(args[0])
    except ValueError:
        print("ID-ul trebuie să fie un număr.")
        return
    for t in todos:
        if t["id"] == tid:
            t["done"] = True
            save_todos(todos)
            print(f"Marcat ca rezolvat: {t['text']}")
            return
    print(f"Sarcina cu id {tid} nu a fost găsită.")


def cmd_delete(todos, args):
    if not args:
        print("Folosire: delete <id>")
        return
    try:
        tid = int(args[0])
    except ValueError:
        print("ID-ul trebuie să fie un număr.")
        return
    for i, t in enumerate(todos):
        if t["id"] == tid:
            removed = todos.pop(i)
            save_todos(todos)
            print(f"Șters: {removed['text']}")
            return
    print(f"Sarcina cu id {tid} nu a fost găsită.")


COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "done": cmd_done,
    "delete": cmd_delete,
}


def main():
    print("Aplica\u021Bie TODO")
    print("Comenzi: add <text>, list, done <id>, delete <id>, exit")
    todos = load_todos()
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd == "exit":
            break
        handler = COMMANDS.get(cmd)
        if handler:
            handler(todos, args)
        else:
            print(f"Comand\u0103 necunoscut\u0103: {cmd}")
    print("La revedere!")


if __name__ == "__main__":
    main()
