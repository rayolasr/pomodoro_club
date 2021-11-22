import configparser
import datetime
import tkinter as tk
from tkinter import ttk

from pydub import AudioSegment
from pydub.playback import play


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.segundos = 0
        self.counter_active = False

        # Leo el fichero de configuración
        print('leyendo el fichero de configuración')
        config = configparser.ConfigParser()
        config.sections()
        config.read('config.ini')
        self.productionTime = int(config['POMODORO_DEFAULT']['productionTime'])
        self.distractionTime = int(config['POMODORO_DEFAULT']['distractionTime'])
        print('fichero de configuración leído')

        # Configuro la ventana
        self.geometry('600x400')
        self.title('Pomodoro Club')
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Configuro el contador de tiempo visual
        self.guitimer = tk.Label(text=f'0:00:00')
        self.guitimer.config(font=("Arial", 50))
        self.guitimer.grid(row=0, column=0, sticky='NSWE')

        # Configuro el botón de inicio y parada de la cuenta atrás
        self.boton1 = ttk.Button(self, text='Start Counter', command=lambda: self.start_countdown())
        self.boton1.grid(row=1, column=0, sticky='NSWE')

    # Métodos para iniciar, mantener y detener el contador
    def start_countdown(self):
        print('Starting countdown')
        self.boton1.config(text='Stop counter', command=lambda: self.stop_counter())
        self.guitimer.update_idletasks()  # Force update the label
        self.boton1.update_idletasks()  # Force update the boton
        self.counter_active = True
        self.countdown(self.productionTime)  # Inicia una cuenta atrás para el tiempoe de producción

    def countdown(self, segundos):
        self.guitimer['text'] = str(datetime.timedelta(seconds=segundos))
        if self.counter_active:
            if segundos > 0:
                self.after(1000, self.countdown, segundos - 1)
            else:
                print('Countdown finished')
                self.boton1.config(text='Start counter', command=lambda: self.start_countdown())
                self.guitimer.update_idletasks()  # Force update the label
                self.boton1.update_idletasks()  # Force update the boton
                play(AudioSegment.from_wav("assets/sounds/notification.wav"))
                self.start_countup()  # Cuando la cuenta atrás termina, inicia una cuenta para el tiempo de distracción
        else:
            self.guitimer['text'] = f'0:00:00'

    def start_countup(self):
        print('Starting countup')
        self.boton1.config(text='Stop counter', command=lambda: self.stop_counter())
        self.guitimer.update_idletasks()  # Force update the label
        self.boton1.update_idletasks()  # Force update the boton
        self.counter_active = True
        self.countup(self.distractionTime, 0)

    def countup(self, duracion, segundos):
        self.guitimer['text'] = str(datetime.timedelta(seconds=segundos))
        if self.counter_active:
            if segundos < duracion:
                self.after(1000, self.countup, duracion, segundos + 1)
            else:
                print('Countup finished')
                self.boton1.config(text='Start counter', command=lambda: self.start_countdown())
                self.guitimer.update_idletasks()  # Force update the label
                self.boton1.update_idletasks()  # Force update the boton
                play(AudioSegment.from_wav("assets/sounds/notification.wav"))
        else:
            self.guitimer['text'] = f'0:00:00'

    def stop_counter(self):
        print('Stopping countdown')
        self.counter_active = False
        self.boton1.config(text='Start counter', command=lambda: self.start_countdown())


window = Gui()
window.mainloop()
