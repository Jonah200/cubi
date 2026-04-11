import time

import paho.mqtt.client as mqtt
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from cubi_touch.cubi_util import generate_scramble

class StartScreen(Screen):
    scramble = StringProperty("")

    def on_pre_enter(self):
        self.scramble = generate_scramble()

    def go_to_inspection(self):
        self.manager.get_screen("inspection").start_timer()
        self.manager.current = "inspection"

class InspectionScreen(Screen):
    time_left = NumericProperty(15)
    show_button = BooleanProperty(False)

    def start_timer(self):
        self.time_left = 15
        self.show_button = False
        Clock.schedule_interval(self.countdown, 1)

    def countdown(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            self.show_button = True
            return False
        
    def start_solve(self):
        self.manager.current = "solve"

class SolveScreen(Screen):
    time_text = StringProperty("Tap to Start")
    running = False
    start_time = 0

    def on_touch_down(self, touch):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            Clock.schedule_interval(self.update_time, 0.01)
        else:
            self.running = False
            Clock.unschedule(self.update_time)
            elapsed = time.time() - self.start_time
            self.show_result(elapsed)
        return True
    
    def update_time(self, dt):
        elapsed = time.time() - self.start_time
        self.time_text = f"{elapsed:.2f}"

    def show_result(self, elapsed):
        scramble = self.manager.get_screen("start").scramble
        content = Label(
            text=f"{scramble}\n\nTime: {elapsed:.2f}",
            halign="center",
            valign="middle",
        )
        content.bind(size=lambda lbl, _: setattr(lbl, 'text_size', lbl.size))

        popup = Popup(
            title="Result",
            content=content,
            size_hint=(0.8,0.5)
        )
        
        content.bind(on_touch_down=lambda *x: self.reset_app(popup))
        popup.open()

    def reset_app(self, popup):
        popup.dismiss()
        self.time_text = "Tap to Start"
        self.manager.current = "start"

class CubiApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(InspectionScreen(name="inspection"))
        sm.add_widget(SolveScreen(name="solve"))
        return sm

if __name__ == "__main__":
    CubiApp().run()
