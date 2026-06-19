import requests

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=44.4323&longitude=26.1063&current_weather=true"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['current_weather']['temperature']
        print(f"Temperatura curentă în București este: {temp}°C")
    else:
        print("Eroare la obținerea datelor de la API.")

if __name__ == "__main__":
    get_weather()