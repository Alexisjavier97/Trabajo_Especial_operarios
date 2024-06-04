import numpy as np
import math
#Se realiza la simulación del sistema hasta el fallo del supermercado.
def simula_falla_supermercado(N,S,TF,TR,Operarios,NSim):
    x_i= [] # Resultados de cada simulación
    #Se realizan Nsim simulaciones
    tiempo_medio = 0 # Se estimará con Monte Carlo
    for i in range(NSim):
        #print("Simulación número", i)
        cajas_a_reparar = 0 # numero de cajas en reparacion

        registro_de_tiempo = 0 # registra el tiempo desde el inicio hasta el momento en que el sistema deja de ser operativo

        #La i-esima simulacion se realiza hasta que haya más de S máquinas en reparación
        while cajas_a_reparar <=S:
            # Se considera por separado el caso donde no hay cajas en reparación para evitar la división por 0
            if cajas_a_reparar == 0:
                registro_de_tiempo += np.random.exponential(N/TF)
                cajas_a_reparar += 1
            m = min(Operarios, cajas_a_reparar) # Cantidad de máquinas siendo reparadas
            X = np.random.exponential(TF/N) # Tiempo que tarda en fallar la siguiente caja
            Y = np.random.exponential(TR/m) # Tiempo que tarda en repararse la siguiente caja
            if X<Y:
                cajas_a_reparar += 1
                registro_de_tiempo += X
            else:
                cajas_a_reparar -= 1
                registro_de_tiempo += Y
        tiempo_medio += registro_de_tiempo
        x_i.append(registro_de_tiempo) # Se guarda el resgistro de tiempo de cada simulacion

    tiempo_medio = tiempo_medio / NSim
    # Se usa el estimador de máxima similitud para la varianza
    sum=0
    for i in range(NSim):
        sum+=(x_i[i] - tiempo_medio)**2
    varianza= 1/(NSim-1) *sum
    desviacion_estandar = math.sqrt(varianza)

    return  tiempo_medio , desviacion_estandar

valor = simula_falla_supermercado(7,3,1,(1/8), 2, 10000)
print("tiempo medio:",valor[0])
print("desviacion  :",valor[1])