import numpy as np
from matplotlib import pyplot as plt

def simular(N: int, S: int, TF: float, TR: float, Operarios: int) -> float:
	"""Simula el tiempo que tarda el supermercado en dejar de ser operativo."""
	assert(N > 0 and S > 0 and TF > 0 and TR > 0 and Operarios > 0)
	cajas_a_reparar = 0 # numero de cajas en reparacion
	registro_de_tiempo = 0 # registra el tiempo desde el inicio hasta el momento en que el sistema deja de ser operativo
    
    # Comienza la simulacion.
	while cajas_a_reparar <=S:
    	# Se considera por separado el caso donde no hay cajas en reparación para evitar la división por 0
		if cajas_a_reparar == 0:
			registro_de_tiempo += np.random.exponential(TF/N)
			cajas_a_reparar += 1
            
		m = min(Operarios, cajas_a_reparar) # Cantidad de máquinas siendo reparadas
		X = np.random.exponential(TF/N) # Tiempo que tarda en fallar la siguiente caja
		Y = np.random.exponential(TR/m) # Tiempo que tarda en repararse la siguiente caja
        
        # Se elige el tiempo menor, se suma al registro de tiempo y se incrementa o disminuye la cantidad de cajas a reparar.
        # El otro tiempo se descarta. No es necesario utilizarlo debido a que la distribución es exponencial.
		if X<Y:
			cajas_a_reparar += 1
			registro_de_tiempo += X
		else:
			cajas_a_reparar -= 1
			registro_de_tiempo += Y
	return registro_de_tiempo

def estimar(N: int, S: int, TF: float, TR: float, Operarios: int, NSim: int) -> tuple:
	"""Estima el tiempo medio de fallo del supermercado mediante el método de Monte Carlo y su desviación estándar con la raíz cuadrada de la varianza muestral.
 	Devuelve además la muestra generada para poder realizar un histograma."""
	assert(N > 0 and S > 0 and TF > 0 and TR > 0 and Operarios > 0 and NSim > 0)
	media = 0
	muestra = []
	# Se estima la media con Monte Carlo.
	for _ in range(NSim):
		x_i = simular(N, S, TF, TR, Operarios)
		media += x_i
		muestra.append(x_i)
	media = media /NSim
	# Calcula la varianza muestral.
	suma = 0
	for i in range(NSim):
		suma += (muestra[i] - media)**2
	desviacion_estandar = (suma / (NSim - 1))**0.5
	return media, desviacion_estandar, muestra

def histogramas(muestra1: list, muestra2: list, bins = 40):
	"""Genera dos histogramas de dos muestras distintas en un mismo gráfico."""
	fig, axs = plt.subplots()
	axs.hist((muestra1, muestra2), bins = bins, color = ["red", "lime"])
	plt.xlabel("Tiempo de vida del supermercado (meses)")
	plt.ylabel("Frecuencia de ocurrencias")
	plt.title("Histograma de dos muestras")
	plt.hist(muestra1, density=True, label='1 opeario',color='red')
	plt.hist(muestra2, density=True, label='2 opearios',color='lime')
	plt.legend(loc='upper right')
	plt.grid(True)
	plt.show()

def histogramas_2(muestra1: list, muestra2: list, bins = 40):
	"""Genera dos histogramas de dos muestras distintas uno al lado del otro."""
	fig, axs = plt.subplots(1, 2)
	axs[0].set_xlim(0, 25)
	axs[1].set_xlim(0, 25)
	axs[0].hist(muestra1, bins=bins,edgecolor = 'black',color = "red")
	axs[1].hist(muestra2, bins=bins,edgecolor = 'black',color  = "lime")
	axs[0].set_xlabel('Tiempo de vida del supermercado (meses)')
	axs[0].set_ylabel('Frecuencia de ocurrencia')

	axs[1].set_xlabel('Tiempo de vida del supermercado (meses)')
	axs[1].set_ylabel('Frecuencia de ocurrencia')
	
	plt.hist(muestra1, density=True, label='1 opeario',color='red')
	axs[0].grid(True)
	plt.hist(muestra2, density=True, label='2 opearios',color='lime')
	axs[1].grid(True)
	plt.legend(loc='upper right')
	plt.show()
