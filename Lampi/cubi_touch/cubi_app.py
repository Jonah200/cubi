import time
from typing import Dict, List

from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from cubi_touch.cubi_util import generate_scramble, generate_scramble_vis
from cubi_service import CubiService
from cubi_common import *

class ColoredBox(Widget):
    def __init__(self, r, g, b, a=1, **kwargs):
        super(ColoredBox, self).__init__(**kwargs)
        with self.canvas:
            Color(r, g ,b, a)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        # Update rectangle when widget moves/resizes
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Face(Widget):
    def __init__(self, arr, **kwargs):
        super(Face, self).__init__(**kwargs)
        self.layout = GridLayout(cols=3,rows=3,spacing=[1])
        for row in arr:
            for color in row:
                self.layout.add_widget(ColoredBox(*COLOR_MAP[color]))
        self.add_widget(self.layout)
        self.bind(pos=self.update_layout, size=self.update_layout)

    def update_layout(self, *args):
        self.layout.pos = self.pos
        self.layout.size = self.size

class VisScreen(Screen):
    scramble_arrs: Dict[str, List[List[str]]] = {}

    def compute_scramble(self):
        self.scramble_arrs = generate_scramble_vis(App.get_running_app().scramble)

    def on_enter(self):
        scramble = App.get_running_app().scramble
        if scramble == "":
            App.get_running_app().scramble = generate_scramble()
        self.layout_grid()

    def go_to_inspection(self):
        self.manager.get_screen("inspection").start_timer()
        self.manager.current = "inspection"

    def rescramble(self):
        App.get_running_app().scramble = generate_scramble()
        self.layout_grid()

    def layout_grid(self):
        self.compute_scramble()
        self.ids.vis_grid.clear_widgets()
        self.ids.vis_grid.add_widget(Widget())
        self.ids.vis_grid.add_widget(Face(self.scramble_arrs['top']))
        self.ids.vis_grid.add_widget(Widget())
        self.ids.vis_grid.add_widget(Widget())
        self.ids.vis_grid.add_widget(Face(self.scramble_arrs['left']))
        self.ids.vis_grid.add_widget(Face(self.scramble_arrs['front']))
        self.ids.vis_grid.add_widget(Face(self.scramble_arrs['right']))
        self.ids.vis_grid.add_widget(Face(self.scramble_arrs['back']))
        self.ids.vis_grid.add_widget(Widget())
        self.ids.vis_grid.add_widget(Face(self.scramble_arrs['bottom']))
        self.ids.vis_grid.add_widget(Widget())
        self.ids.vis_grid.add_widget(Widget())

class InspectionScreen(Screen):
    time_left = NumericProperty(15)
    ready_set_go = StringProperty("")

    def start_timer(self):
        self.time_left = 15
        Clock.schedule_interval(self.countdown, 1)

    def countdown(self, dt):
        self.time_left -= 1
        if self.time_left == 2:
            self.ready_set_go = "READY\n"
        if self.time_left == 1:
            self.ready_set_go += "SET\n"
        if self.time_left <= 0:
            self.start_solve()
        
    def on_touch_down(self, touch):
        self.start_solve()

    def start_solve(self):
        Clock.unschedule(self.countdown)
        self.manager.current = "solve"
        self.time_left = 15
        self.ready_set_go = ""

class SolveScreen(Screen):
    time_text = StringProperty("0.0")
    running = False
    start_time = 0

    def on_enter(self):
        self.running = True
        self.start_time = time.time()
        Clock.schedule_interval(self.update_time, 0.01)

    def on_touch_down(self, touch):
        self.running = False
        Clock.unschedule(self.update_time)
        elapsed = time.time() - self.start_time
        self.show_result(elapsed)
        return True
    
    def update_time(self, dt):
        elapsed = time.time() - self.start_time
        self.time_text = f"{elapsed:.2f}"

    def show_result(self, elapsed):
        scramble = App.get_running_app().scramble

        result_label = Label(
            text=f"{scramble}\n\nTime: {elapsed:.2f}",
            halign="center",
            valign="middle",
        )
        result_label.bind(size=lambda lbl, _: setattr(lbl, 'text_size', lbl.size))

        save_btn = Button(text="Save", size_hint_y=1)
        discard_btn = Button(text="Discard", size_hint_y=1)

        btn_row = BoxLayout(orientation="horizontal", size_hint_y=0.3, spacing=10)
        btn_row.add_widget(save_btn)
        btn_row.add_widget(discard_btn)

        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(result_label)
        content.add_widget(btn_row)

        popup = Popup(title="Result", content=content, size_hint=(0.9, 0.8), auto_dismiss=False)

        save_btn.bind(on_press=lambda *_: self._on_save(popup, scramble, elapsed))
        discard_btn.bind(on_press=lambda *_: self._on_discard(popup))

        popup.open()

    def _on_save(self, popup, scramble, elapsed):
        App.get_running_app().service.publish_solve(scramble, elapsed)
        popup.dismiss()
        self.manager.current = "visualization"

    def _on_discard(self, popup):
        popup.dismiss()
        self.manager.current = "visualization"

    def on_leave(self):
        self.time_text = "0.0"

class CubiApp(App):
    scramble = StringProperty("")

    def build(self):
        self.service = CubiService()
        self._association_popup = None

        self.service.on_association_required = self._on_association_required
        self.service.on_associated = self._on_associated
        self.service.start()

        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(VisScreen(name="visualization"))
        sm.add_widget(InspectionScreen(name="inspection"))
        sm.add_widget(SolveScreen(name="solve"))
        return sm

    # --- Association callbacks (may arrive from MQTT thread) ---

    def _on_association_required(self, code):
        # Schedule on main thread; capture code in default arg
        #Clock.schedule_once(lambda dt, c=code: self._show_association_popup(c))
        pass

    def _on_associated(self, username):
        #Clock.schedule_once(lambda dt, u=username: self._dismiss_association_popup(u))
        pass

    def _show_association_popup(self, code):
        if self._association_popup is not None:
            return  # already showing

        short_code = code[:6]
        content = Label(
                text=f"Associate this device with you Cubi account\n{short_code}\nEnter this code on the web dashboard",
                font_size=18,
                halign="center"
        )

        content.bind(size=lambda lbl, _: setattr(lbl, 'text_size', lbl.size))

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
