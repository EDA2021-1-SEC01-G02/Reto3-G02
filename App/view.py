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
    
catalog = None

"""
Menu principal.
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.init()
        to_print = controller.loadData(catalog)
        print('Numero de elementos: %s \n' 'Alto del arbbol: %s'  %(to_print[0][0],to_print[0][1]))
        print('Primera fecha donde huvo un avistamiento: ' + str(to_print[1]))
        print('Ultima fecha donde huvo un avistamiento: ' + str(to_print[2]))


    elif int(inputs[0]) == 2:
        ciudad = input("Digite la ciudad a consultar: ")
        resultados = controller.countCity(catalog,ciudad)
        print('\n''El numero de ciudades (elementos del map) es: %s \n' 'El alto del arbol es de: %s' %(resultados[0], resultados[1]))
        print('En %s hay %s avistamientos' %(ciudad.capitalize(), resultados[2]))
   


    else:
        sys.exit(0)
sys.exit(0)
