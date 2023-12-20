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

        # Leer el fichero de configuración
        print('leyendo el fichero de configuración')
        config = configparser.ConfigParser()
        config.sections()
        config.read('config.ini')
        self.produccion = int(config['POMODORO_DEFAULT']['productionTime'])
        self.distraccion = int(config['POMODORO_DEFAULT']['distractionTime'])
        print('fichero de configuración leído')

        # Configurar la ventana
        self.geometry('600x400')
        self.title('Pomodoro Club')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)
        self.columnconfigure(3, weight=1)

        # Configurar el contador de tiempo visual
        self.guitimer = tk.Label(text=f'0:00:00')
        self.guitimer.config(font=("Arial", 50))
        self.guitimer.grid(row=1, column=0, sticky='NSWE', columnspan=4)

        # Configurar el botón de inicio y parada de la cuenta atrás
        self.boton1 = ttk.Button(self, text='Start Counter', command=lambda: self.start_countdown())
        self.boton1.grid(row=2, column=0, sticky='NSWE', columnspan=4)

        # Configurar las cajas para los tiempos del pomodoro
        self.produccion = tk.StringVar(value='25')
        self.etiqueta_produccion = tk.Label(text='Minutos de producción')
        self.etiqueta_produccion.grid(row=0, column=0)
        self.etiqueta_produccion.config(font=("Arial", 8))
        self.entrada_produccion = ttk.Entry(self, width=2, textvariable=self.produccion)
        self.entrada_produccion.grid(row=0, column=1,)

        self.distraccion = tk.StringVar(value='5')
        self.etiqueta_distraccion = tk.Label(text='Minutos de distracción')
        self.etiqueta_distraccion.grid(row=0, column=2)
        self.etiqueta_distraccion.config(font=("Arial", 8))
        self.entrada_distraccion = ttk.Entry(self, width=2, textvariable=self.distraccion)
        self.entrada_distraccion.grid(row=0, column=3)

    # Iniciar, mantener y detener el contador
    def start_countdown(self):
        print('Starting countdown')
        self.boton1.config(text='Stop counter', command=lambda: self.stop_counter())
        self.guitimer.update_idletasks()  # Force update the label
        self.boton1.update_idletasks()  # Force update the boton
        self.counter_active = True
        self.entrada_produccion.config(state='disabled')
        self.entrada_distraccion.config(state='disabled')
        self.countdown(int(self.produccion.get())*60)  # Inicia una cuenta atrás para el tiempoe de producción

    def countdown(self, segundos):
        self.guitimer['text'] = str(datetime.timedelta(seconds=segundos))
        if self.counter_active:
            if segundos > 0:
                self.after(1000, self.countdown, segundos-1)
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
        self.countup(int(self.distraccion.get())*60, 0)

    def countup(self, duracion, segundos):
        self.guitimer['text'] = str(datetime.timedelta(seconds=segundos))
        if self.counter_active:
            if segundos < duracion:
                self.after(1000, self.countup, duracion, segundos+1)
            else:
                print('Countup finished')
                self.boton1.config(text='Start counter', command=lambda: self.start_countdown())
                self.guitimer.update_idletasks()  # Force update the label
                self.boton1.update_idletasks()  # Force update the boton
                self.entrada_distraccion.config(state='enabled')
                self.entrada_produccion.config(state='enabled')
                play(AudioSegment.from_wav("assets/sounds/notification.wav"))
        else:
            self.guitimer['text'] = f'0:00:00'

    def stop_counter(self):
        print('Stopping countdown')
        self.counter_active = False
        self.entrada_distraccion.config(state='enabled')
        self.entrada_produccion.config(state='enabled')
        self.boton1.config(text='Start counter', command=lambda: self.start_countdown())


window = Gui()
window.mainloop()
