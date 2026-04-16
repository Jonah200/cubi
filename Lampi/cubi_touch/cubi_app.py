import time

from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from cubi_touch.cubi_util import generate_scramble
from cubi_service import CubiService

class StartScreen(Screen):
    scramble = StringProperty("")

    def on_pre_enter(self):
        self.scramble = generate_scramble()

    def rescramble(self):
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

        result_label = Label(
            text=f"{scramble}\n\nTime: {elapsed:.2f}",
            halign="center",
            valign="middle",
        )
        result_label.bind(size=lambda lbl, _: setattr(lbl, 'text_size', lbl.size))

        save_btn = Button(text="Save", size_hint_y=0.3)
        discard_btn = Button(text="Discard", size_hint_y=0.3)

        btn_row = BoxLayout(orientation="horizontal", size_hint_y=0.3, spacing=10)
        btn_row.add_widget(save_btn)
        btn_row.add_widget(discard_btn)

        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(result_label)
        content.add_widget(btn_row)

        popup = Popup(title="Result", content=content, size_hint=(0.8, 0.6), auto_dismiss=False)

        save_btn.bind(on_press=lambda *_: self._on_save(popup, scramble, elapsed))
        discard_btn.bind(on_press=lambda *_: self._on_discard(popup))

        popup.open()

    def _on_save(self, popup, scramble, elapsed):
        App.get_running_app().service.publish_solve(scramble, elapsed)
        popup.dismiss()
        self.time_text = "Tap to Start"
        self.manager.current = "start"

    def _on_discard(self, popup):
        popup.dismiss()
        self.time_text = "Tap to Start"
        self.manager.current = "start"

class CubiApp(App):
    def build(self):
        self.service = CubiService()
        self._association_popup = None

        self.service.on_association_required = self._on_association_required
        self.service.on_associated = self._on_associated

        sm = ScreenManager()
        sm.add_widget(StartScreen(name="start"))
        sm.add_widget(InspectionScreen(name="inspection"))
        sm.add_widget(SolveScreen(name="solve"))
        return sm

    # --- Association callbacks (may arrive from MQTT thread) ---

    def _on_association_required(self, code):
        # Schedule on main thread; capture code in default arg
        Clock.schedule_once(lambda dt, c=code: self._show_association_popup(c))

    def _on_associated(self, username):
        Clock.schedule_once(lambda dt, u=username: self._dismiss_association_popup(u))

    def _show_association_popup(self, code):
        if self._association_popup is not None:
            return  # already showing

        short_code = code[:6]
        content = BoxLayout(orientation="vertical", padding=20, spacing=15)
        content.add_widget(Label(
            text="Associate this device\nwith your Cubi account:",
            halign="center",
            font_size=18,
        ))
        content.add_widget(Label(
            text=short_code,
            font_size=48,
            bold=True,
            halign="center",
        ))
        content.add_widget(Label(
            text="Enter this code on the web dashboard.",
            halign="center",
            font_size=14,
        ))

        self._association_popup = Popup(
            title="Device Not Associated",
            content=content,
            size_hint=(0.85, 0.55),
            auto_dismiss=False,
        )
        self._association_popup.open()

    def _dismiss_association_popup(self, username):
        if self._association_popup is None:
            return
        self._association_popup.dismiss()
        self._association_popup = None

    def on_stop(self):
        self.service.stop()

if __name__ == "__main__":
    CubiApp().run()
