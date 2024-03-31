

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import j1
from scipy.signal import argrelextrema


class ExpNorm(Normalize):
    def __init__(self, vmin=None, vmax=None, clip=False, gamma=1.0):
        Normalize.__init__(self, vmin, vmax, clip)
        self.gamma = gamma

    def __call__(self, value, clip=None):
        y = ((value - self.vmin) / (self.vmax - self.vmin)) ** self.gamma
        return np.ma.masked_array(y)

#Calcular el número de Fresnell

lam1 = 400*10**(-9)
lam2 = 550*10**(-9)
lam3 = 650*10**(-9)
a = 0.01*10**(-3)
R = 3

'''#Pedir datos al usuario
lado = float(input("Introduce el lado de la abertura en metros: "))
lam = float(input("Introduce la longitud de onda en metros: "))
R = float(input("Introduce la distancia de la rendija al plano de observación: "))
'''

def sinc(arg):
    if arg == 0:
        return 1.0
    else:
        return np.sin(arg) / arg


def Fresnel(a, lam, R):
    F = a**2 / (lam * R)
    return F


'''
#########################################

def aber_rectangular(arg):
    return sinc(arg)**2

#a = lado/2

distancia = 1
alfa = x/distancia

arg = k*a*alfa

##############################################
'''





def aber_circular(Z):
    return (2*j1(Z) / Z)**2


x1 = np.linspace(-0.40, 0.40, 2000)
x2 = np.linspace(-0.40, 0.40, 2000)
x3 = np.linspace(-0.55, 0.55, 2000) 
y1 = np.linspace(-0.40, 0.40, 2000)
y2 = np.linspace(-0.45, 0.45, 2000)
y3 = np.linspace(-0.55, 0.55, 2000)   
x, y = np.meshgrid(x3, y3)



k1 = 2 * np.pi / lam1
k2 = 2 * np.pi / lam2
k3 = 2 * np.pi / lam3

Z1 = k1 * a/2 * np.sqrt(x**2 + y**2)/R
Z2 = k2 * a/2 * np.sqrt(x**2 + y**2)/R
Z3 = k3 * a/2 * np.sqrt(x**2 + y**2)/R


# Cálculo de los valores de la función para Z1, Z2, Z3
values1 = aber_circular(Z1)
values2 = aber_circular(Z2)
values3 = aber_circular(Z3)


def segundo_max(R, k, x):
    x= 8.46*R/(k*a/2)
    return x
    
max_400 = segundo_max(R, k1, x)
max_550 = segundo_max(R, k2, x)
max_650 = segundo_max(R, k3, x)


z_min = 0.0008 # Valor mínimo del eje z
z_max = 0.02 # Valor máximo del eje z
step = 0.0002 # Paso entre los niveles del eje z

imax = 0.02
imin = 0.0005

# Aplicar LogNorm a los colores
norm = ExpNorm(vmin=imin, vmax=imax)



# Creación de la figura
fig = plt.figure(figsize=(18, 12))  # Ajusta el tamaño de la figura si es necesario

# Creación del primer subplot 3D
ax1 = fig.add_subplot(231, projection='3d')
ax1.plot_surface(x, y, values1, cmap='Blues', norm=norm)
ax1.set_title('Abertura circular 0.01mm: Longitud de onda de 400 nm')
ax1.set_xlabel('X m')
ax1.set_ylabel('Y m')
ax1.set_zlabel('Intensidad en la pantalla')

# Creación del primer subplot 2D
ax4 = fig.add_subplot(234)
ax4.contourf(x3, y3, values1, cmap='Blues', levels=np.arange(z_min, z_max, step), norm=norm)  # Ajusta los niveles según la sección del eje z que quieras mostrar
ax4.set_title('Abertura circular 0.01mm: Longitud de onda de 400 nm')
ax4.set_xlabel('X m')
ax4.set_ylabel('Y m')
ax4.plot(max_400, 0, 'bo', label=f'Segundo máximo del patrón 400nm: x={max_400:.2f}m')

# Creación del segundo subplot 3D
ax2 = fig.add_subplot(232, projection='3d')
ax2.plot_surface(x, y, values2, cmap='Greens', norm=norm)
ax2.set_title('Abertura circular 0.01mm: Longitud de onda de 550 nm')
ax2.set_xlabel('X m')
ax2.set_ylabel('Y m')
ax2.set_zlabel('Intensidad en la pantalla')

# Creación del segundo subplot 2D
ax5 = fig.add_subplot(235)
ax5.contourf(x3, y3, values2, cmap='Greens', levels=np.arange(z_min, z_max, step), norm=norm)  # Ajusta los niveles según la sección del eje z que quieras mostrar
ax5.set_title('Abertura circular 0.01mm: Longitud de onda de 550 nm')
ax5.set_xlabel('X m')
ax5.set_ylabel('Y m')
ax5.plot(max_550, 0, 'go', label=f'Segundo máximo del patrón 550nm: x={max_550:.2f}m')

# Creación del tercer subplot 3D
ax3 = fig.add_subplot(233, projection='3d')
ax3.plot_surface(x, y, values3, cmap='Reds', norm=norm)
ax3.set_title('Abertura circular 0.01mm: Longitud de onda de 650 nm')
ax3.set_xlabel('X m')
ax3.set_ylabel('Y m')
ax3.set_zlabel('Intensidad en la pantalla')

# Creación del tercer subplot 2D
ax6 = fig.add_subplot(236)
ax6.contourf(x3, y3, values3, cmap='Reds', levels=np.arange(z_min, z_max, step), norm=norm)  # Ajusta los niveles según la sección del eje z que quieras mostrar
ax6.set_title('Abertura circular 0.01mm: Longitud de onda de 650 nm')
ax6.set_xlabel('X m')
ax6.set_ylabel('Y m')
ax6.plot(max_650, 0, 'ro', label=f'Segundo máximo del patrón 650nm: x={max_650:.2f}m')

fig2, ax = plt.subplots()

# Agregar los datos del primer gráfico 2D
contour1 = ax.contourf(x, y, values1, cmap='Blues', levels=np.arange(z_min, z_max, step), norm=norm)
# Agregar el punto para max_400
ax.plot(max_400, 0, 'bo', label=f'Segundo máximo del patrón 400nm: x={max_400:.2f}m')

# Agregar los datos del segundo gráfico 2D
contour2 = ax.contourf(x, y, values2, cmap='Greens', levels=np.arange(z_min, z_max, step), norm=norm)
# Agregar el punto para max_550
ax.plot(max_550, 0, 'go', label=f'Segundo máximo del patrón 550nm: x={max_550:.2f}m')

# Agregar los datos del tercer gráfico 2D
contour3 = ax.contourf(x, y, values3, cmap='Reds', levels=np.arange(z_min, z_max, step), norm=norm, alpha=0.5)
# Agregar el punto para max_650
ax.plot(max_650, 0, 'ro', label=f'Segundo máximo del patrón 650nm: x={max_650:.2f}m')

# Configurar los títulos y las etiquetas de los ejes
ax.set_title('Combinación de los tres gráficos 2D')
ax.set_xlabel('X m')
ax.set_ylabel('Y m')

# Agregar la leyenda
ax.legend()
ax4.legend()
ax5.legend()
ax6.legend()

# Mostrar el gráfico
plt.show()



