#Shelsy A. Chanis / 8-916-978
#Mario Carter / 8-915-1458

import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()

    def search_location(self):
        search_template = "http://api.openweathermap.org/data/2.5/find?q={}&type=like&APPID=c2c87d898f065cd7b4d1a64e5706ad60"
        search_url = search_template.format(self.search_input.text)
        content = Button(text="Thank you so much for using me, now you can choose a city so you can know the weather."
                              "\nAnd yes I kinda do what weather apps do. Don't judge me.")
        popup = Popup(title='HELLO THERE! THIS A POP UP.', content=content, auto_dismiss=False, size_hint=(None, None), size=(700, 200))
        content.bind(on_press=popup.dismiss)
        popup.open()
        request = UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        cities = [(d['name'], d['sys']['country']) for d in data['list']]
        #crashes when try to search non-exist city or a blank :l
        self.search_results.item_strings = cities
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()

    def args_converter(self, index, data_item):
        city, country = data_item
        return {'location': (city, country)}

class LocationButton(ListItemButton):
    location = ListProperty()

class WeatherRoot(BoxLayout):
    current_weather = ObjectProperty()
    def show_current_weather(self, location = None):
        self.clear_widgets()

        if self.current_weather is None:
            self.current_weather = CurrentWeather()

        if location is not None:
            self.current_weather.location = location

        self.current_weather.update_weather()
        self.add_widget(self.current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())

class CurrentWeather(BoxLayout):
    location= ListProperty(['Panama City', 'PA'])
    conditions= ObjectProperty()
    temp= NumericProperty()
    temp_min= NumericProperty()
    temp_max= NumericProperty()
    conditions_box = ObjectProperty()
    conditions_desc = StringProperty()
    wind = NumericProperty()
    conditions_image = StringProperty()

    def update_weather(self):
        content = Button(text="Working on that........weather.\nWell, that's it. It was lovely to help you!")
        popup = Popup(title='HELLO THERE! THIS ANOTHER POP UP.', content=content, auto_dismiss=False, size_hint=(None, None), size=(700, 200))
        content.bind(on_press=popup.dismiss)
        popup.open()
        weather_template = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=c2c87d898f065cd7b4d1a64e5706ad60"
        weather_url = weather_template.format(*self.location)
        request = UrlRequest(weather_url, self.weather_retrieved)

    def weather_retrieved(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.conditions_desc = data['weather'][0]['description']
        self.temp = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']
        self.wind= data['wind']['speed']
        self.conditions_image = "http://openweathermap.org/img/w/{}.png".format(data['weather'][0]['icon'])

class WeatherApp(App):
    pass

if __name__ == '__main__':
    WeatherApp().run()
