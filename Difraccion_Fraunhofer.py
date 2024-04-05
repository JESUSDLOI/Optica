
# ---------------------------------------------------------
# Nombre del Programa - Difracion_Fraunhofer.py
# Copyright (C) 2024 Jesús de la Oliva Iglesias
# Este programa es software propietario.
# ---------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import j1
from scipy.signal import argrelextrema

#Insturcciones para el usuario


class ExpNorm(Normalize):
    def __init__(self, vmin=None, vmax=None, clip=False, gamma=1.0):
        Normalize.__init__(self, vmin, vmax, clip)
        self.gamma = gamma

    def __call__(self, value, clip=None):
        y = ((value - self.vmin) / (self.vmax - self.vmin)) ** self.gamma
        return np.ma.masked_array(y)
    
    
def Fresnel(a, lam, R):
    F = a**2 / (lam * R)
    return F


#Instrucciones para el usuario

print("---------------------------------------------------------\n")
print("Programa para visualizar la difracción de Fraunhöfer de una abertura circular o rectangular\n")
print("---------------------------------------------------------\n")


#Pedir al usuario el tipo de abertura

abertura = input("\nIntroduce el tipo de abertura circular(0) o rectangular(1): ")


#Elegir el tipo de abertura

if abertura == "0":
    print("\nHas elegido una abertura circular, introduce los datos")
    
    #Pedir datos al usuario
    lado = float(input("\nIntroduce el diámtro de la abertura en milímtros: "))
    a = lado/2 * 10**-3
    longitud = float(input("\nIntroduce la longitud de onda en nanómetros: "))
    lam = longitud * 10**-9
    R = float(input("\nIntroduce la distancia de la rendija al plano de observación en metros: "))
    F= Fresnel(a, lam, R)
    
    print("\nEl número de fresnel es: ", F)
    if F <= 1*10**-3:
        print("\nLa aproximación de Fresnel es válida")
        
        #Tamaño de la pantalla
        l = 0.4
        l = float(input("\nIntroduce el lado del tamaño de la pantalla en metros(se recomienda ser inferior a 1 y mayor a 0.1): "))
        
        #Definir el rango de la pantalla para el plot
        x = np.linspace(-l, l, 5000)
        y = np.linspace(-l, l, 5000)
        X, Y = np.meshgrid(x, y)
        
        #Número de onda
        k = 2 * np.pi / lam
        
        #Argumento de la función de difracción
        Z = k * a * np.sqrt(X**2 + Y**2)/R
        
        #Función para calcular la difrracción Fraunhöfer de una abertura circular de diámetro a	
        def aber_circular(Z):
            return (2*j1(Z) / Z)**2
        
        #Valores de la intensidad de difracción de Fraunhöfer en pantalla
        valores = aber_circular(Z)
    else:
        print("\nLa aproximación de Fresnel no es adecuada para este caso de Frauhofer")
        exit()
    
elif abertura == "1":
    print("Has elegido una abertura rectangular, introduce los datos\n")
    
    #Pedir datos al usuario
    lado1 = float(input("\nIntroduce el lado del eje x de la abertura en milímetros: "))
    a = lado1/2 * 10**-3
    lado2 = float(input("\nIntroduce el lado del eje y de la abertura en milímetros: "))
    b = lado2/2 * 10**-3
    longitud = float(input("\nIntroduce la longitud de onda en nanómetros: "))
    lam = longitud * 10**-9
    R = float(input("\nIntroduce la distancia de la rendija al plano de observación en metros: "))
    diagonal = np.sqrt(a**2 + b**2)
    F= Fresnel(diagonal, lam, R)
    
    print("\nEl número de fresnel es: ", F)
    
    if F <= 1*10**-3:
        print("La aproximación de Fresnel es válida\n")
        
        #Tamaño de la pantalla
        l = float(input("\nIntroduce el lado del tamaño de la pantalla en metros (se recomienda ser inferior a 1 y mayor a 0.1): "))
        
        #Definir el rango de la pantalla para el plot
        x = np.linspace(-l, l, 2000)
        y = np.linspace(-l, l, 2000)
        X, Y = np.meshgrid(x, y)
        
        #Número de onda
        k = 2 * np.pi / lam
        
        #Argumento de la función de difracción
        alfa = -X/R
        beta = -Y/R
        arg1 = k*a*alfa
        arg2 = k*b*beta
        
        #Función senoC
        def sinc(arg):
            return np.where(arg == 0, 1.0, np.sin(arg) / arg)
        
        #Función para calcular la difracción Fraunhöfer de una abertura rectangular de lado a
        def aber_rectangular(arg):
            return sinc(arg)**2
        
        valores = aber_rectangular(arg1) * aber_rectangular(arg2)
        
        
    else:
        print("La aproximación de Fresnel no es adecuada para este caso de Frauhofer\n")
        exit()


else:
    print("No has introducido un tipo de abertura válido, vuelve a intentarlo\n")
    
    exit()


#Recomendación 
print("\nSi se visualiza mal la figura, se recomienda cambiar el tamaño de la pantalla al ejecutar el programa")

# Diccionario de colores orientativos para la longitud de onda en el espectro visible
colores = {
    (400*10**-9, 500*10**-9): 'Blues',
    (500*10**-9, 580*10**-9): 'Greens',
    (580*10**-9, 630*10**-9): 'YlOrBr',
    (630*10**-9, 700*10**-9): 'Oranges',
    (700*10**-9, float('inf')): 'Reds'
}

# Encontrar el color correspondiente a la longitud de onda
for wavelength_range, color in colores.items():
    if lam >= wavelength_range[0] and lam < wavelength_range[1]:
        color = color
        break
else:
    color = 'Purples'

# Creación de la figura
fig = plt.figure(figsize=(18, 12))  # Ajusta el tamaño de la figura si es necesario

#Parametros para el plot
z_min = 0.0008 # Valor mínimo de visualización eje z
z_max = 0.02 # Valor máximo de visualización del eje z
step = 0.0002 # Paso entre los niveles del eje z

#Variación de la intensidad de los colores
imax = 0.02
imin = 0.0005

# Aplicar LogNorm a los colores
norm = ExpNorm(vmin=imin, vmax=imax)

if abertura == "0":
    # Creación del primer subplot 3D
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, valores, cmap=color, norm=norm)
    ax1.set_title('Abertura circular de {:.2e}mm: Longitud de onda de {:.2e}m'.format(lado1, lado2, lam))
    ax1.set_xlabel('X m')
    ax1.set_ylabel('Y m')
    ax1.set_zlabel('Intensidad en la pantalla')

    # Creación del primer subplot 2D
    ax4 = fig.add_subplot(122)
    ax4.contourf(X, Y, valores, cmap=color, levels=np.arange(z_min, z_max, step), norm=norm)  # Ajusta los niveles según la sección del eje z que quieras mostrar
    ax4.set_title('Abertura circular de {:.2e}mm: Longitud de onda de {:.2e}m'.format(lado1, lado2, lam))
    ax4.set_xlabel('X m')
    ax4.set_ylabel('Y m')
    
elif abertura == "1":
    # Creación del primer subplot 3D
    ax2 = fig.add_subplot(121, projection='3d')
    ax2.plot_surface(X, Y, valores, cmap=color, norm=norm)
    ax2.set_title('Abertura rectangular de {:.2e}mm x {:.2e}mm: Longitud de onda de {:.2e}m'.format(lado1, lado2, lam))
    ax2.set_xlabel('X m')
    ax2.set_ylabel('Y m')
    ax2.set_zlabel('Intensidad en la pantalla')

    # Creación del primer subplot 2D
    ax5 = fig.add_subplot(122)
    ax5.contourf(X, Y, valores, cmap=color, levels=np.arange(z_min, z_max, step), norm=norm)  # Ajusta los niveles según la sección del eje z que quieras mostrar
    ax5.set_title('Abertura rectangular de {:.2e}mm x {:.2e}mm: Longitud de onda de {:.2e}m'.format(lado1, lado2, lam))
    ax5.set_xlabel('X m')
    ax5.set_ylabel('Y m')


# Mostrar el gráfico1
plt.show()


