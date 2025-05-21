import requests

def get_weather(city):
    url = "http://wttr.in/" + city + "?format=3";
    answer = requests.get(url);
    if(answer.status_code == 200):
        return answer.text
    else:
        return "Ciudad no encontrada."