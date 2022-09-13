"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger
from programy.extensions.base import Extension
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from .weather_util import weatherutils


class WeatherExtension(Extension):

    def get_geo_locator(self):
        return Nominatim(user_agent="weather")


    # WEATHER [OBSERVATION|FORECAST] LOCATION * WHEN *

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):

        try:
            splits = data.split()
            if len(splits) != 5:
                YLogger.debug(client_context, "Weather - Not enough paramters passed, [%d] expected 5", len(splits))
                return None

            obvtype = splits[0]
            if obvtype not in ['OBSERVATION', 'FORECAST']:
                YLogger.debug(client_context, "Weather - Type not understood [%s]", obvtype)
                return None

            if splits[1] == 'LOCATION':
                postcode = splits[2]
            else:
                YLogger.debug(client_context, "Weather - LOCATION missing")
                return None

            if splits[3] == 'WHEN' or splits[3] == "DAY":
                when = splits[4]
            else:
                YLogger.debug(client_context, "Weather - WHEN missing")
                return None

            if obvtype == 'OBSERVATION':
                result = self.current_observation(client_context, postcode)

            elif obvtype == 'FORECAST':
                result =  self.five_day_forecast(client_context, postcode, when)

            return result

        except Exception as error:
            YLogger.exception(client_context, "Failed to execute weather extension", error)

        return "ERR"

    def current_observation(self, context, postcode):
        YLogger.debug(context, "Getting weather observation for [%s]", postcode)

        weather = weatherutils(postcode)
        weather_result = weather.get_weather_now()

        result = "DESCRIPTION {} TEMPRATURE {} WIND {} PRESSURE {} HUMIDITY {}".format(
            weather_result["description"], 
            weather_result["temperature"],
            weather_result["wind_speed"],
            weather_result["pressure"],
            weather_result["humidity"]
        )

        return result

    def five_day_forecast(self, context, postcode, when, fromdate=None):
        YLogger.debug(context, "Getting 5 day forecast for [%s] at time [%s]", postcode, when)

        weather = weatherutils(postcode)

        try:
            time = datetime.now() + timedelta(days=int(when))
            weather_result = weather.get_weather_when(str(time.date()))

            result = "DESCRIPTION {} TEMPRATURE {} WIND {} PRESSURE {} HUMIDITY {}".format(
                weather_result["description"], 
                weather_result["temperature"],
                weather_result["wind_speed"],
                weather_result["pressure"],
                weather_result["humidity"]
            )

            return result
        except Exception as error:
            YLogger.exception(client_context, "Failed to execute weather extension", error)
            return "ERR"

        return "ERR"