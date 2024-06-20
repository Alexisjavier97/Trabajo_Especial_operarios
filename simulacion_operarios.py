import numpy as np
from matplotlib import pyplot as plt
from numpy import arange

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

def estimar(N: int, S: int, TF: float, TR: float, Operarios: int, NSim: int) -> tuple[float, float, list]:
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

def genera_histograma(muestra1: list, muestra2: list, label1 = "1 operario", label2 = "2 operarios", bin_width = 1):
	"""Genera dos histogramas de dos muestras distintas en un mismo gráfico."""
	max_data = max(max(muestra1), max(muestra2))
	fig, axs = plt.subplots()
	axs.hist((muestra1, muestra2), bins = arange(0, max_data + bin_width, bin_width), color = ["red", "lime"])
	plt.xlabel("Tiempo de vida del supermercado (meses)")
	plt.ylabel("Frecuencias")
	plt.title("Histograma de dos muestras")
	plt.hist(muestra1, density=True, label=label1 ,color='red')
	plt.hist(muestra2, density=True, label=label2 ,color='lime')
	plt.legend(loc='upper right')
	plt.grid(True)
	plt.show()

def histograma1():
"""Genera un Histograma de comparación de un operario con S=3 máquinas de repuesto y S=4 máquinas de repuesto
Tambien muestra la desviacion estandar generada y su media muestral para cada caso"""
	muestra1=estimar(7,3,1,1/8,1,10000)
	muestra2=estimar(7,4,1,1/8,1,10000)

	print("Un Operario considerando 3 cajas de repuesto (Rojo) ")
	print("    Media muestral: ",muestra1[0])
	print("    Desviacion estandar: ",muestra1[1])

	print("Un Operario considerando 4 cajas de repuesto (Verde) ")
	print("    Media muestral: ",muestra2[0])
	print("    Desviacion estandar: ",muestra2[1])
	
	genera_histograma(muestra1[2],muestra2[2], label1 = "1 operario, S = 3", label2 = "1 operario, S = 4")

def histograma2():
"""Genera un Histograma de comparación de un operario y dos operarios con S=3 para ambos casos
Tambien muestra la desviacion estandar generada y su media muestral para cada caso"""
	muestra1=estimar(7,3,1,1/8,1,10000)
	muestra2=estimar(7,3,1,1/8,2,10000)

	print("Un Operario considerando 3 cajas de repuesto (Rojo) ")
	print("    Media muestral: ",muestra1[0])
	print("    Desviacion estandar: ",muestra1[1])

	print("Dos Operarios considerando 3 cajas de repuesto (Verde) ")
	print("    Media muestral: ",muestra2[0])
	print("    Desviacion estandar: ",muestra2[1])
	
	genera_histograma(muestra1[2],muestra2[2], label1 = "1 operario, S = 3", "2 operarios, S = 3")

def histograma3():	
"""Genera un Histograma de comparación de dos operarios en paralelo con tres cajas de repuesto y
un operario con cuatro cajas de repuesto. Tambien muestra la desviacion estandar generada y su media muestral
para cada caso"""
	muestra1=estimar(7,4,1,1/8,1,10000)
	muestra2=estimar(7,3,1,1/8,2,10000)

	print("Un Operario con S = 4 (Rojo) ")
	print("    Media muestral: ",muestra1[0])
	print("    Desviacion estandar: ",muestra1[1])

	print("Dos Operarios con S = 3 (Verde) ")
	print("    Media muestral: ",muestra2[0])
	print("    Desviacion estandar: ",muestra2[1])
	
	genera_histograma(muestra1[2],muestra2[2], label1 = "1 operario, S = 4", label2 = "2 operarios, S = 1")

def mostrar_menu():
	print("\nSeleccione el histograma y sus resultados que desea ver: \n")	

	print("    1. Mostrar resultados con 1 operario, S = 3 y 1 operario, S = 4.\n")
	print("    2. Mostrar resultados con 1 operario, S = 3 y 2 operarios, S = 3.\n")
	print("    2. Mostrar resultados con 2 operarios, S = 3 y 1 operarios, S = 4.\n")
	print("    4. Salir\n")

def main():
	mostrar_menu()

while True:
		mostrar_menu()
		opcion = input("    Ingrese su opción: ")

		if opcion == '1':
			histograma1()

		elif opcion == '2':
			histograma2()

		elif opcion == '3':
			histograma3()
		elif opcion == '4':
			print("Saliendo del programa...")
			break
		else:
			print("Opción no válida. Por favor, ingrese una opción válida.")

if __name__ == "__main__":
    main()
