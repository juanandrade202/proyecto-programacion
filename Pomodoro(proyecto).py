"""
Nombre: Juan Francisco Andrade Lara
Curso: Gr1
Fecha: 31/07/2023
"""
import time
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock

class PomodoroApp(App):
    def build(self):
        self.title = "Pomodoro Timer"
        self.layout = BoxLayout(orientation="vertical")

        self.lbl_timer = Label(text="00:00", font_size=48)
        self.layout.add_widget(self.lbl_timer)

        self.btn_start_pomodoro = Button(text="Iniciar Pomodoro", on_press=self.start_pomodoro)
        self.btn_stop_pomodoro = Button(text="Detener Pomodoro", on_press=self.stop_pomodoro, disabled=True)
        self.layout.add_widget(self.btn_start_pomodoro)
        self.layout.add_widget(self.btn_stop_pomodoro)

        self.btn_start_break = Button(text="Iniciar Descanso Corto", on_press=self.start_break)
        self.btn_stop_break = Button(text="Detener Descanso", on_press=self.stop_break, disabled=True)
        self.layout.add_widget(self.btn_start_break)
        self.layout.add_widget(self.btn_stop_break)

        self.btn_start_long_break = Button(text="Iniciar Descanso Largo", on_press=self.start_long_break)
        self.btn_stop_long_break = Button(text="Detener Descanso Largo", on_press=self.stop_long_break, disabled=True)
        self.layout.add_widget(self.btn_start_long_break)
        self.layout.add_widget(self.btn_stop_long_break)

        # Variables de estado
        self.pomodoro_running = False
        self.break_running = False
        self.long_break_running = False
        self.timer_running = False
        self.timer_start_time = None
        self.timer_duration = None
        self.timer_data = []

        return self.layout

    def start_pomodoro(self, instance):
        if not self.pomodoro_running:
            self.pomodoro_running = True
            self.timer_duration = 25 * 60  # 25 minutos
            self.start_timer()
            self.btn_start_pomodoro.disabled = True
            self.btn_stop_pomodoro.disabled = False

    def stop_pomodoro(self, instance):
        self.stop_timer()
        self.pomodoro_running = False
        self.btn_start_pomodoro.disabled = False
        self.btn_stop_pomodoro.disabled = True
        self.show_notification("Pomodoro Completado", "¡Es hora de un descanso corto!")

    def start_break(self, instance):
        if not self.break_running:
            self.break_running = True
            self.timer_duration = 5 * 60  # 5 minutos
            self.start_timer()
            self.btn_start_break.disabled = True
            self.btn_stop_break.disabled = False

    def stop_break(self, instance):
        self.stop_timer()
        self.break_running = False
        self.btn_start_break.disabled = False
        self.btn_stop_break.disabled = True
        self.show_notification("Descanso Corto Completado", "¡Es hora de trabajar de nuevo!")

    def start_long_break(self, instance):
        if not self.long_break_running:
            self.long_break_running = True
            self.timer_duration = 15 * 60  # 15 minutos
            self.start_timer()
            self.btn_start_long_break.disabled = True
            self.btn_stop_long_break.disabled = False

    def stop_long_break(self, instance):
        self.stop_timer()
        self.long_break_running = False
        self.btn_start_long_break.disabled = False
        self.btn_stop_long_break.disabled = True
        self.show_notification("Descanso Largo Completado", "¡Es hora de trabajar de nuevo!")

    def start_timer(self, instance=None):
        if not self.timer_running:
            self.timer_running = True
            if self.timer_duration is None:  # Agregamos esta línea para inicializar el tiempo si es None
                self.timer_duration = 0
        self.timer_start_time = time.time()
        Clock.schedule_interval(self.update_timer_label, 1)

    def stop_timer(self, dt=None):
        if self.timer_running:
            self.timer_running = False
            Clock.unschedule(self.update_timer_label)
            if dt is not None:  # Check if this is called by schedule_once
                self.timer_data.append(self.timer_duration)  # Cambiamos el registro de tiempo a segundos
                if self.timer_duration > 0:  # Solo si el tiempo es mayor a cero
                    if self.timer_duration == 25 * 60:  # Check if it's Pomodoro time
                        self.plot_timer_data()

    def update_timer_label(self, dt):
        if self.timer_running:
            elapsed_time = self.timer_duration - (time.time() - self.timer_start_time)
            minutes = int(elapsed_time / 60)
            seconds = int(elapsed_time % 60)
            self.lbl_timer.text = f"{minutes:02}:{seconds:02}"

    def show_notification(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def plot_timer_data(self):
        plt.clf()
        plt.plot(range(1, len(self.timer_data) + 1), self.timer_data)
        plt.xlabel('Cronómetro')
        plt.ylabel('Tiempo (segundos)')
        plt.title('Tiempo del Cronómetro')
        plt.tight_layout()
        plt.savefig('timer_plot.png')
        plt.close()
        popup = Popup(title='Gráfico del Cronómetro', size_hint=(None, None), size=(400, 400))
        image = Image(source='timer_plot.png')
        popup.content = image
        popup.open()

if __name__ == '__main__':
    PomodoroApp().run()
