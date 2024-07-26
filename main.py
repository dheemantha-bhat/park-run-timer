from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import API_KEY, CRED_PATH



class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_event = None
        self.timer_seconds = 0
        self.result = [0]
        self.lap_count = 0

    def build(self):

        main_layout = FloatLayout()

        button_layout = BoxLayout(
            orientation="vertical", size_hint=(1, 0.4), pos_hint={"top": 1}
        )

        button1 = Button(text="Start Race", background_color=(1, 0, 0, 1))
        button1.bind(on_press=self.start_timer)
        button2 = Button(text="Lap", background_color=(0, 1, 0, 1))
        button2.bind(on_press=self.lap_timer)
        button2.bind(on_press=self.store_list)
        button3 = Button(text="End Race", background_color=(0, 0, 1, 1))
        button3.bind(on_press=self.stop_timer)

        button_layout.add_widget(button1)
        button_layout.add_widget(button2)
        button_layout.add_widget(button3)

        self.timer = Label(
            text="Timer: 0 seconds", size_hint=(1, 0.2), pos_hint={"center_y": 0.5}
        )
        self.display = Label(
            text="Results", size_hint=(1, 0.2), pos_hint={"center_y": 0.25}
        )

        main_layout.add_widget(button_layout)
        main_layout.add_widget(self.timer)
        main_layout.add_widget(self.display)

        return main_layout

    def start_timer(self, instance):
        if self.timer_event is None:
            self.timer_seconds = 0
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.timer_seconds += 1
        self.timer.text = f"Timer: {self.timer_seconds} seconds"

    def stop_timer(self, instance):
        self.timer_event = Clock.unschedule(self.timer_event)
        self.timer.text = f"Timer: {self.timer_seconds} seconds"

    def lap_timer(self, instance):
        if self.timer_event is not None:
            self.result.append(self.timer_seconds)
            self.lap_count += 1
            lap_info = [
                f"Lap: {self.lap_count - i} | Timer: {self.result[-(i+1)]} seconds"
                for i in range(2)
            ]
            self.display.text = " \n ".join(lap_info)

    def store_list(self, instance):

        my_list = [self.lap_count + 1, self.timer_seconds]

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            CRED_PATH, scope
        )
        client = gspread.authorize(creds)

        sheet = client.open_by_key(
            API_KEY
        ).sheet1

        sheet.append_row(my_list)


if __name__ == "__main__":
    MainApp().run()
