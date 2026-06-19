import json
import requests
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def get_weather(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"Temperatura exactă preluată de la senzor este {data['current_weather']['temperature']}°C."
    return "Eroare la obținerea vremii."

tools = [{"type": "function", "function": {"name": "get_weather", "description": "Obține vremea curentă pentru o latitudine și longitudine.", "parameters": {"type": "object", "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}}, "required": ["latitude", "longitude"]}}}]

prompt_utilizator = "Cât este temperatura acum în București? (coordonate: lat 44.43, lon 26.10)"

print("\n--- 1. RULARE FĂRĂ TOOL CALLS ---")
print("Agentul simplu zice:", client.chat.completions.create(model="mistral", messages=[{"role": "user", "content": prompt_utilizator}]).choices[0].message.content)

print("\n--- 2. RULARE CU TOOL CALLS ---")
messages = [{"role": "system", "content": "You are a helpful assistant. Use tools when needed."}, {"role": "user", "content": prompt_utilizator}]
msg = client.chat.completions.create(model="mistral", messages=messages, tools=tools).choices[0].message

if msg.tool_calls:
    messages.append(msg)
    for tool_call in msg.tool_calls:
        args = json.loads(tool_call.function.arguments)
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": get_weather(args["latitude"], args["longitude"])})
    print("Agentul cu Tools zice:", client.chat.completions.create(model="mistral", messages=messages, tools=tools).choices[0].message.content)
else:
    print("Agent:", msg.content)
