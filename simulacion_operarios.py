import numpy as np
from matplotlib import pyplot as plt

def simular(N, S, TF, TR, Operarios):
	cajas_a_reparar = 0 # numero de cajas en reparacion
	registro_de_tiempo = 0 # registra el tiempo desde el inicio hasta el momento en que el sistema deja de ser operativo
    
    # Comienza la simulacion.
	while cajas_a_reparar <=S:
    	# Se considera por separado el caso donde no hay cajas en reparación para evitar la división por 0
		if cajas_a_reparar == 0:
			registro_de_tiempo += np.random.exponential(N/TF)
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

def estimar(N, S, TF, TR, Operarios, NSim):
	media = 0
	muestra = [] # Se almacenan los datos de la simulación para estimar la varianza y para hacer histogramas.
	# Se estima la media con Monte Carlo.
	for _ in range(NSim):
		x_i = simular(N, S, TF, TR, Operarios)
		media += x_i
		muestra.append(x_i)
	media = media /NSim
	# Se estima la desviación estándar con el estimador de máxima verosimilitud.
	suma = 0
	for i in range(NSim):
		suma += (muestra[i] - media)**2
	desviacion_estandar = (suma / (NSim - 1))**0.5
	return media, desviacion_estandar, muestra

def histogramas(muestras, bins = 100):
	# Muestra dos histogramas de dos muestras distintas en el mismo gráfico.
	fig, axs = plt.subplots(1, 1)
	axs.hist(muestras, bins = bins, color = ["red", "lime"])
	plt.show()

