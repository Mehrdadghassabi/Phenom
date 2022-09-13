from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim


class weatherutils:
    def __init__(self, city):
        self.city = city

    def get_geo_location(self):
        app = Nominatim(user_agent="weather")
        latitude = app.geocode(self.city).latitude
        longitude = app.geocode(self.city).longitude
        return (latitude, longitude)

    def get_weather_now(self):
        latlong = self.get_geo_location()
        url = "https://darksky.net/forecast/{},{}/us12/en".format(latlong[0], latlong[1])
        resp = requests.get(url)

        soup = BeautifulSoup(resp.text, "lxml")

        humidity = soup.find('span', class_='num swip humidity__value').text
        wind_speed = soup.find('span', class_='num swip wind__speed__value').text
        pressure = soup.find('span', class_='num swip pressure__value').text
        temperature = soup.find('span', class_='summary swap').text.split()[0]
        description = " ".join(soup.find('span', class_='summary swap').text.split()[1:])

        result = {
            'humidity' : humidity,
            'wind_speed' : wind_speed,
            'pressure' : pressure,
            'temperature' : temperature,
            'description' : description
        }

        return result

    def get_weather_when(self, when):
        latlong = self.get_geo_location()
        url = "https://darksky.net/details/{},{}/{}/us12/en".format(latlong[0], latlong[1], when)
        resp = requests.get(url)

        soup = BeautifulSoup(resp.text, "lxml")

        humidity = soup.find('div', class_='humidity').find('span', class_='val swap').text.split()[0]
        wind_speed = soup.find('div', class_='wind').find('span', class_="val swap").text.split()[0]
        pressure = soup.find('div', class_='pressure').find('span', class_="val swap").text.split()[0]
        temperature = soup.find('div', class_='temperature').find('span', class_="val swap").text.strip()
        description = soup.find('div', class_='dayDetails center').find('p', id='summary').text.replace("\xa0", "")

        result = {
            'humidity' : humidity,
            'wind_speed' : wind_speed,
            'pressure' : pressure,
            'temperature' : temperature,
            'description' : description
        }

        return result
