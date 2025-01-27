﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Avistamientos en una ciudad")
    print("3- Contar los avistamientos por duración")
    print("4- Contar avistamientos por Hora/Minutos del día")
    print("5- Contar los avistamientos en un rango de fechas")
    print("6- Contar los avistamientos de una Zona Geográfica")
    print("7- Visualizar los avistamientos de una Zona Geográfica")
    
catalog = None

"""
Menu principal.
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        #start_time = time.process_time()
        catalog = controller.init()
        to_print = controller.loadData(catalog)
        #stop_time = time.process_time()
        print('Numero de elementos: %s \n' 'Alto del arbol: %s'  %(to_print[0][0],to_print[0][1]))
        print('Primera fecha donde huvo un avistamiento: ' + str(to_print[1]))
        print('Ultima fecha donde huvo un avistamiento: ' + str(to_print[2]))
        print(controller.flElements(catalog['sights']))
        #print((stop_time - start_time)*1000)

    elif int(inputs[0]) == 2:
        ciudad = input("Digite la ciudad a consultar: ")
        #start_time = time.process_time()
        resultados = controller.countCity(catalog,ciudad)
        #stop_time = time.process_time()
        print('\n''El numero de ciudades (elementos del map) es: %s \n' 'El alto del arbol es de: %s' %(resultados[0], resultados[1]))
        print('En %s hay %s avistamientos' %(ciudad.capitalize(), resultados[2]))
        print(resultados[3])
        #print((stop_time - start_time)*1000)

    elif int(inputs[0]) == 3:
        sights = controller.maxDuration(catalog)
        min = float(input('Ingrese el valor minimo del rango: '))
        max = float(input('Ingrese el valor maximo del rango: '))
        #start_time = time.process_time()
        range = controller.getDurRange(catalog, min, max)
        #stop_time = time.process_time()
        print('Hay %s diferentes duraciones de avistamiendo de OVNIS.' %(sights[1]))
        print('La mayor duracion de un avistamiento es:')
        print('Duration (seconds): %s. ' %(sights[0]))
        print('Count: %s' %(sights[2]))
        print('Hay %s avistamientos que duraron entre %s y %s' %(range[1], min, max))
        print('Los tres primero y los tres ultimos avistamientos del rango son:')
        print(range[0])
        #print((stop_time - start_time)*1000)

    #Requerimiento 3
    elif int(inputs[0]) == 4:
        print("Recuerde que usted debe digitar el tiempo en el formato de HH:MM ")
        horaInf = input("Ingrese el limite inferior: ")
        horaSup = input("Ingrese el limite superior: ")
        #start_time = time.process_time()
        resultado = controller.countTime(catalog,horaInf,horaSup)
        #stop_time = time.process_time()
        print("Hay %s horas unicas en los registros..." %(resultado[0]))
        print("El registro con la hora mas tarde es:")
        print(resultado[1])
        print("Hay un total de %s avistamientos entre: %s y %s" %(resultado[2],horaInf,horaSup))
        print("Los primeros tres y ultimos 3 avistamientos de OVNIS en este rango son:")
        print(resultado[3])
        #print((stop_time - start_time)*1000)

    #Requerimiento 4
    elif int(inputs[0]) == 5:
        print("Recuerde que usted debe digitar la fecha en el formato de AAAA-MM-DD")
        fechaInf = input("Ingrese el limite inferior: ")
        fechaSup = input("Ingrese el limite superior: ")
        #start_time = time.process_time()
        resultado = controller.countDate(catalog,fechaInf,fechaSup)
        #stop_time = time.process_time()
        print("Hay %s fechas unicas en los registros..." %(resultado[0]))
        print("El registro con la fecha mas antigua es:")
        print(resultado[1])
        print("Hay un total de %s avistamientos entre: %s y %s" %(resultado[2],fechaInf,fechaSup))
        print("Los primeros tres y ultimos 3 avistamientos de OVNIS en este rango son:")
        print(resultado[3])
        #print((stop_time - start_time)*1000)
    
    elif int(inputs[0]) == 6:
        minLon = float(input('Digite la longitud minima del rango: '))
        maxLon = float(input('Digite la longitud maxima del rango: '))
        minLat = float(input('Digite la latitud minima del rango: '))
        maxLat = float(input('Digite la latitud maxima del rango: '))

        #start_time = time.process_time()
        result = (controller.getAreaRange(catalog, minLon, maxLon, minLat, maxLat ))
        #stop_time = time.process_time()
        print('Avistamientos de OVNIS en una longitud entre el rango de %s y %s'%(minLon, maxLon))
        print('y en una latitud entre el rango de %s y %s' %(minLat, maxLat))
        print('Hay %s avistamientos diferentes en el area.'%(result[1]))
        print(result[0])
        #print((stop_time - start_time)*1000)
        pass

    elif int(inputs[0]) == 7:
        minLon = float(input('Digite la longitud minima del rango: '))
        maxLon = float(input('Digite la longitud maxima del rango: '))
        minLat = float(input('Digite la latitud minima del rango: '))
        maxLat = float(input('Digite la latitud maxima del rango: '))

        #start_time = time.process_time()
        controller.showAreaRange(catalog,minLon,maxLon,minLat,maxLat)
        #stop_time = time.process_time()
        print("Revisar el archivo index.html que se ha creado o actualizado en la raiz del repositorio.")
        #print((stop_time - start_time)*1000)

        

    else:
        sys.exit(0)
sys.exit(0)
