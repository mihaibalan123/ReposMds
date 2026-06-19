import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
todo_list = []

def add_task(task_desc):
    todo_list.append(task_desc)
    return f"SUCCES: Am adăugat '{task_desc}' în lista."

def list_tasks():
    return "Task-urile tale sunt: " + ", ".join(todo_list) if todo_list else "Nu ai niciun task."

tools = [{"type": "function", "function": {"name": "add_task", "description": "Adaugă un task", "parameters": {"type": "object", "properties": {"task_desc": {"type": "string"}}, "required": ["task_desc"]}}}, {"type": "function", "function": {"name": "list_tasks", "description": "Afișează task-urile", "parameters": {"type": "object", "properties": {}}}}]

def proceseaza_comanda(prompt):
    messages = [{"role": "system", "content": "Ești un asistent de management al task-urilor. Răspunde pe scurt în română."}, {"role": "user", "content": prompt}]
    msg = client.chat.completions.create(model="mistral", messages=messages, tools=tools).choices[0].message
    if msg.tool_calls:
        messages.append(msg)
        for t in msg.tool_calls:
            n = t.function.name
            a = json.loads(t.function.arguments)
            r = add_task(a.get("task_desc", "")) if n == "add_task" else list_tasks()
            messages.append({"role": "tool", "tool_call_id": t.id, "content": r})
        print("🤖 Agent:", client.chat.completions.create(model="mistral", messages=messages, tools=tools).choices[0].message.content)
    else:
        print("🤖 Agent:", msg.content)

print("--- AI Task Manager pornit (scrie 'exit' pentru ieșire) ---")
while True:
    u = input("\nTu: ")
    if u.lower() == 'exit': break
    proceseaza_comanda(u)
