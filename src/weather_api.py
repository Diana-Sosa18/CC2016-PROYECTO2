import requests

def get_weather(city):
    url = "http://wttr.in/" + city + "?format=3";
    answer = requests.get(url);
    if(answer.status_code == 200):
        print(answer.text);
    else:
        print("La ciudad no fue encontrada.");

city = str.lower(input("Ingrese la ciudad: "));
get_weather(city);