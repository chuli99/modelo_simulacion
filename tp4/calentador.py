import matplotlib.pyplot as plt
import numpy as np
class Calentador:

    def __init__(self, temperatura, masa, tiempo, voltaje):
        self.temperatura=temperatura
        self.masa=masa
        self.set_tiempo(tiempo)
        self.cte=4.18
        self.voltaje=voltaje

    def get_temperatura(self):
        return self.temperatura
    
    def set_temperatura(self, temperatura):
        self.temperatura=temperatura
    
    def get_masa(self):
        return self.masa
    
    def set_masa(self, masa):
        self.masa=masa

    def get_tiempo(self):
        return self.tiempo
    
    def set_tiempo(self, tiempo):
        if tiempo>=0:
            self.tiempo=tiempo
        else:
            print("El tiempo debe ser positivo y en segundos")
    
    def get_voltaje(self):
        return self.voltaje
    
    def set_voltaje(self, voltaje):
        self.voltaje=voltaje

    def calculo_restistencia(self):
        delta_t=100-self.temperatura
        q=self.cte*self.masa*delta_t
        p=q/self.tiempo
        i=p/self.voltaje
        r=self.voltaje/i
        return r
    
    def calculo_delta_temp(self):
        delta_t=100-self.temperatura
        q=self.cte*self.masa*delta_t
        p=q/self.tiempo
        i=p/self.voltaje

        nuevo_delta=p/((self.masa/1000)*self.cte*1000)
        return nuevo_delta
    
    def graficar(self, nuevo_delta):
        x = self.tiempo
        y = [nuevo_delta * i for i in range(1, x+1)]
        coefficients = np.polyfit(range(1, x+1), y, 1)
        slope = coefficients[0]
        intercept = coefficients[1]
        y_line = [slope * i + intercept for i in range(1, x+1)]
        # Mostramos la gráfica
        plt.plot(range(1, x+1), y_line, 'b-') 
        plt.show()


#Defino variables
temperatura = 30
masa = 1000
tiempo = 300
voltaje = 220
calentador=Calentador(temperatura,masa,tiempo,voltaje)