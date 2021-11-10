"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    return model.init()
 
def loadData(catalog):
    file = cf.data_dir + 'UFOS/UFOS-utf8-small.csv'
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for sight in input_file:
        model.addSight(catalog, sight)
        model.addCity(catalog, sight)
        model.addDuration(catalog, sight)
        model.addTime(catalog, sight)

    
    return (model.sightSize(catalog)),(model.minKey(catalog)), (model.maxKey(catalog))

def flElements(catalog):
    
    return model.getTen(catalog)
# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def maxDuration(catalog):
    durMap = catalog['duration']
    values = model.mapSize(durMap)
    maxValue =  model.maxMap(durMap)
    lst = model.onlyMapValue(durMap, maxValue)
    return maxValue, values, model.getData(lst) 
    
def getDurRange(catalog, min, max):
    lists = model.getDurRange(catalog['duration'], min, max)
    getItems = model.getAllItems(lists)

    return model.agregarTabla(getItems[0],3), getItems[1]

def countCity(catalog,city):
    return model.countCity(catalog, city)

def countTime(catalog,timeMin,timeMax):
    return model.countTime(catalog,timeMin,timeMax)


