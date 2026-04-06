import paho.mqtt.client as mqtt
from kivy.app import App
from kivy.properties import StringProperty
from cubi_touch.cubi_util import generate_scramble

class CubiApp(App):
    display_text = StringProperty("Hello")

    def change_text(self):
        self.display_text = generate_scramble()

if __name__ == "__main__":
    CubiApp().run()
