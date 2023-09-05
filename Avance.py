"""
Nombre: Juan Francisco Andrade Lara
Curso: Gr1
Fecha: 31/07/2023
"""
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import threading
import datetime
import time

# Definición de la clase SesiónEstudio
class SesiónEstudio:
    def __init__(self, fecha, tiempo_estudio, avance_material):
        self.fecha = fecha
        self.tiempo_estudio = tiempo_estudio
        self.avance_material = avance_material

# Definición de la clase SeguimientoEstudio
class SeguimientoEstudio:
    def __init__(self):
        self.sesiones = []
        self.tiempo_inicial = None
        self.tiempo_transcurrido = 0
        self.temporizador_activo = False

    def agregar_sesion_estudio(self, sesion):
        self.sesiones.append(sesion)

    def calcular_tiempo_total_estudio(self):
        return np.sum([sesion.tiempo_estudio for sesion in self.sesiones])

    def generar_grafico_tiempo_estudio(self):
        fechas = [sesion.fecha for sesion in self.sesiones]
        tiempos_estudio = [sesion.tiempo_estudio for sesion in self.sesiones]
        tiempos_minutos = [tiempo * 60 for tiempo in tiempos_estudio]  # Convertir a minutos

        plt.plot(fechas, tiempos_minutos, marker='o', linestyle='-')  # Gráfico de dispersión con líneas rectas
        plt.xlabel('Fechas')
        plt.ylabel('Tiempo de Estudio (minutos)')
        plt.title('Tiempo de Estudio por Sesión')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Definición de la clase TemporizadorPomodoro
class TemporizadorPomodoro:
    def __init__(self):
        self.tiempo_transcurrido = 0
        self.tiempo_pomodoro = 1500  # 1500 segundos = 25 minutos (duración de una sesión de estudio)
        self.tiempo_descanso = 300  # 300 segundos = 5 minutos (duración de un descanso)
        self.temporizador_activo = False
        self.cuenta_descansos = 0
        self.pomodoros_completados = 0

    def temporizador_pomodoro(self, lbl_temporizador):  # Agregar lbl_temporizador como argumento
        while self.temporizador_activo:
            time.sleep(1)
            self.tiempo_transcurrido += 1
            tiempo_restante = max(self.tiempo_pomodoro - self.tiempo_transcurrido, 0)
            tiempo_formateado = self.formatear_tiempo(tiempo_restante)
            lbl_temporizador.config(text=f"Tiempo: {tiempo_formateado}")
            if tiempo_restante <= 0:
                self.detener_pomodoro()
                messagebox.showinfo("Pomodoro completado", "¡Se acabó el tiempo!")
                self.cuenta_descansos += 1
                if self.cuenta_descansos == 4:
                    btn_descanso_largo.config(state=tk.NORMAL)
                self.pomodoros_completados += 1
                if self.pomodoros_completados == 2:
                    btn_descanso_largo.config(state=tk.NORMAL)
                reiniciar_botones()

    def temporizador_descanso(self):
        while self.temporizador_activo:
            time.sleep(1)
            self.tiempo_transcurrido += 1
            tiempo_restante = max(self.tiempo_descanso - self.tiempo_transcurrido, 0)
            tiempo_formateado = self.formatear_tiempo(tiempo_restante)
            lbl_temporizador.config(text=f"Tiempo: {tiempo_formateado}")
            if tiempo_restante <= 0:
                self.detener_descanso()
                messagebox.showinfo("Descanso completado", "¡Descanso terminado! Inicia otra sesión Pomodoro.")

    def iniciar_pomodoro(self):
        if not self.temporizador_activo:
            self.tiempo_transcurrido = 0
            self.temporizador_activo = True
            threading.Thread(target=self.temporizador_pomodoro, args=(lbl_temporizador,)).start()

    def detener_pomodoro(self):
        self.temporizador_activo = False
        # Habilitar los botones correspondientes cuando se detiene el Pomodoro
        btn_iniciar_pomodoro.config(state=tk.NORMAL)
        btn_detener_pomodoro.config(state=tk.DISABLED)
        btn_iniciar_descanso.config(state=tk.NORMAL)
        btn_detener_descanso.config(state=tk.DISABLED)
        btn_iniciar_sesion_estudio.config(state=tk.NORMAL)
        btn_detener_sesion_estudio.config(state=tk.DISABLED)
        btn_reiniciar_temporizador_sesion_estudio.config(state=tk.DISABLED)

    def iniciar_descanso(self):
        if not self.temporizador_activo:
            self.tiempo_transcurrido = 0
            self.temporizador_activo = True
            threading.Thread(target=self.temporizador_descanso).start()

    def detener_descanso(self):
        self.temporizador_activo = False
        if self.cuenta_descansos >= 4:
            btn_descanso_largo.config(state=tk.NORMAL)

    def formatear_tiempo(self, segundos):
        minutos = int(segundos // 60)
        segundos = int(segundos % 60)
        return f"{minutos:02}:{segundos:02}"

# Función para reiniciar los botones
def reiniciar_botones():
    btn_iniciar_pomodoro.config(state=tk.NORMAL)
    btn_detener_pomodoro.config(state=tk.DISABLED)
    btn_iniciar_descanso.config(state=tk.NORMAL)
    btn_detener_descanso.config(state=tk.DISABLED)
    btn_iniciar_sesion_estudio.config(state=tk.NORMAL)
    btn_detener_sesion_estudio.config(state=tk.DISABLED)
    btn_reiniciar_temporizador_sesion_estudio.config(state=tk.DISABLED)

# Definición de la clase TemporizadorSesionEstudio
class TemporizadorSesionEstudio:
    def __init__(self):
        self.tiempo_transcurrido = 0
        self.temporizador_activo = False

    def contar_tiempo(self):
        if self.temporizador_activo:
            self.tiempo_transcurrido += 1
            tiempo_formateado = self.formatear_tiempo(self.tiempo_transcurrido)
            lbl_temporizador.config(text=f"Tiempo: {tiempo_formateado}")
            root.after(1000, self.contar_tiempo)

    def iniciar_temporizador(self):
        if not self.temporizador_activo:
            self.tiempo_transcurrido = 0
            self.temporizador_activo = True
            self.contar_tiempo()

    def detener_temporizador(self):
        self.temporizador_activo = False
        self.tiempo_transcurrido = 0

    def formatear_tiempo(self, segundos):
        minutos = int(segundos // 60)
        segundos = int(segundos % 60)
        return f"{minutos:02}:{segundos:02}"

# Función para iniciar el Pomodoro
def iniciar_pomodoro():
    temporizador_pomodoro.iniciar_pomodoro()
    btn_iniciar_pomodoro.config(state=tk.DISABLED)
    btn_detener_pomodoro.config(state=tk.NORMAL)

# Función para detener el Pomodoro
def detener_pomodoro():
    temporizador_pomodoro.detener_pomodoro()

# Función para iniciar el Descanso
def iniciar_descanso():
    temporizador_pomodoro.iniciar_descanso()
    btn_iniciar_descanso.config(state=tk.DISABLED)
    btn_detener_descanso.config(state=tk.NORMAL)

# Función para detener el Descanso
def detener_descanso():
    temporizador_pomodoro.detener_descanso()

# Función para iniciar la Sesión de Estudio
def iniciar_sesion_estudio():
    seguimiento.tiempo_inicial = time.time()
    seguimiento.temporizador_activo = True
    btn_iniciar_sesion_estudio.config(state=tk.DISABLED)
    btn_detener_sesion_estudio.config(state=tk.NORMAL)
    btn_reiniciar_temporizador_sesion_estudio.config(state=tk.DISABLED)
    temporizador_sesion_estudio.iniciar_temporizador()

# Función para detener la Sesión de Estudio
def detener_sesion_estudio():
    seguimiento.temporizador_activo = False
    tiempo_transcurrido_sesion = int(time.time() - seguimiento.tiempo_inicial)
    tiempo_formateado = temporizador_sesion_estudio.formatear_tiempo(tiempo_transcurrido_sesion)
    temporizador_sesion_estudio.detener_temporizador()
    lbl_temporizador.config(text=f"Tiempo: {tiempo_formateado}")
    seguimiento.agregar_sesion_estudio(SesiónEstudio(str(datetime.datetime.now()), tiempo_transcurrido_sesion / 3600, 0))
    seguimiento.generar_grafico_tiempo_estudio()
    btn_iniciar_sesion_estudio.config(state=tk.NORMAL)
    btn_detener_sesion_estudio.config(state=tk.DISABLED)
    btn_reiniciar_temporizador_sesion_estudio.config(state=tk.NORMAL)

# Función para reiniciar el temporizador de la Sesión de Estudio
def reiniciar_temporizador_sesion_estudio():
    temporizador_sesion_estudio.detener_temporizador()
    lbl_temporizador.config(text="Tiempo: 00:00")
    btn_iniciar_sesion_estudio.config(state=tk.NORMAL)
    btn_detener_sesion_estudio.config(state=tk.DISABLED)
    btn_reiniciar_temporizador_sesion_estudio.config(state=tk.DISABLED)

# Función para tomar un descanso largo
def tomar_descanso_largo():
    btn_descanso_largo.config(state=tk.DISABLED)
    temporizador_pomodoro.cuenta_descansos = 0
    temporizador_descanso_largo.tiempo_transcurrido = 0
    temporizador_descanso_largo.temporizador_activo = False
    temporizador_descanso_largo.contar_tiempo()
    messagebox.showinfo("Descanso Largo", "¡Tomar descanso de 15 minutos!")
    btn_descanso_largo.config(state=tk.NORMAL)

# Crear instancia del seguimiento de estudio
seguimiento = SeguimientoEstudio()

# Crear instancia del temporizador Pomodoro
temporizador_pomodoro = TemporizadorPomodoro()

# Crear instancia del temporizador contador de sesión de estudio
temporizador_sesion_estudio = TemporizadorSesionEstudio()

# Crear interfaz gráfica
root = tk.Tk()
root.title("Temporizador de Estudio")

lbl_temporizador = tk.Label(root, text="Tiempo: 00:00")
lbl_temporizador.pack()

# Botones para el temporizador Pomodoro
btn_iniciar_pomodoro = tk.Button(root, text="Iniciar Pomodoro", command=iniciar_pomodoro)
btn_iniciar_pomodoro.pack()

btn_detener_pomodoro = tk.Button(root, text="Detener Pomodoro", command=detener_pomodoro, state=tk.DISABLED)
btn_detener_pomodoro.pack()

# Botones para el temporizador de descanso
btn_iniciar_descanso = tk.Button(root, text="Iniciar Descanso", command=iniciar_descanso)
btn_iniciar_descanso.pack()

btn_detener_descanso = tk.Button(root, text="Detener Descanso", command=detener_descanso, state=tk.DISABLED)
btn_detener_descanso.pack()

# Botones para el temporizador de sesión de estudio
btn_iniciar_sesion_estudio = tk.Button(root, text="Iniciar Sesión de Estudio", command=iniciar_sesion_estudio)
btn_iniciar_sesion_estudio.pack()

btn_detener_sesion_estudio = tk.Button(root, text="Detener Sesión de Estudio", command=detener_sesion_estudio, state=tk.DISABLED)
btn_detener_sesion_estudio.pack()

btn_reiniciar_temporizador_sesion_estudio = tk.Button(root, text="Reiniciar Temporizador", command=reiniciar_temporizador_sesion_estudio, state=tk.DISABLED)
btn_reiniciar_temporizador_sesion_estudio.pack()

# Botón para tomar descanso largo
btn_descanso_largo = tk.Button(root, text="Tomar Descanso Largo (15 min)", command=tomar_descanso_largo, state=tk.DISABLED)
btn_descanso_largo.pack()

root.mainloop()
