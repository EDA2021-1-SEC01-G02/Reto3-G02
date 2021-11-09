﻿"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.bst import height
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
import datetime
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def init():
    catalog = {'sights': None,
                'dateIndex': None,
                "hourIndex": om.newMap(omaptype="RBT",comparefunction=None)
                }

    catalog['sights'] = lt.newList('ARRAY_LIST', None)
    catalog['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    catalog['cityIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=None)                               
    return catalog

# Funciones para agregar informacion al catalogo

def countCity(catalog, city):
    map = catalog['cityIndex']
    size =  (om.size(map))
    height = (om.height(map))
    cityMap = onlyMapValue(map, city)
    citySize = 0
    lst = om.valueSet(cityMap)
    for pos in range(1, lt.size(lst)+1):
        temp = lt.getElement(lst, pos)
        sizeTemp = om.size(temp)
        citySize += sizeTemp
    return size, height, citySize

def addCity(catalog, sight):
    map = catalog['cityIndex']
    city = sight['city']
    time = sight['datetime']
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    if not om.contains(map, city):
        timeMap = om.newMap(omaptype='RBT',comparefunction=compareDates)
        om.put(map, city, timeMap)
    to_add = onlyMapValue(map, city)
    if not om.contains(to_add, time.date()):  
        hourmap = om.newMap(omaptype='RBT',
                                        comparefunction=compareDates)
        om.put(to_add, time.date(), hourmap)
    hourMap =  onlyMapValue(to_add, time.date())
    om.put(hourMap, time.time(), lt.newList('ARRAY_LIST') )
    final = onlyMapValue(hourMap, time.time())
    lt.addLast(final, sight )

def addSight(catalog, sight):
    lt.addLast(catalog['sights'], sight)
    updateDateIndex(catalog['dateIndex'], sight)
    return catalog

def updateDateIndex(catalog, sight):
    occurreddate = sight['datetime']
    sightDate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(catalog, sightDate.date())
    if entry is None:
        datentry = newDataEntry(sight)
        om.put(catalog, sightDate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, sight)
    return map

def addDateIndex(date, sight):
    lst = date['lstshape']
    lt.addLast(lst, sight)
    dateIndex = date['shapeIndex']
    shapentry = mp.get(dateIndex, sight['shape'])
    if (shapentry is None):
        entry = newSightEntry(sight['shape'], sight)
        lt.addLast(entry['lstsight'], sight)
        mp.put(dateIndex, sight['shape'], entry)
    else:
        entry = me.getValue(shapentry)
        lt.addLast(entry['lstsight'], sight)
    
    return date

#def updateHourIndex(catalog,sight):
    #ocurredHour = sight["datetime"]
    

# Funciones para creacion de datos


def onlyMapValue(map, key):
    pair = om.get(map, key)
    value = me.getValue(pair)
    return value

def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'shapeIndex': None, 'lstshape': None}
    entry['shapeIndex'] = mp.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=None)
    entry['lstshape'] = lt.newList('ARRAY_LIST', compareDates)
    return entry


# Funciones de consulta
def newSightEntry(sightype, sight):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    sientry = {'sight': None, 'lstsight': None}
    sientry['sight'] = sightype
    sientry['lstsight'] = lt.newList('ARRAY_LIST', None)
    return sientry

def sightSize(catalog):
    return lt.size(catalog['sights']), om.height(catalog['dateIndex'])

def extractByTimeRange(catalog,date1,date2):
    """
    Extrae los datos que esten en el rango de las horas.
    """
    result = lt.newList() #Lista a almacenar datos
    dateKeys = om.keySet(catalog) #Llaves para recorrer el mapa
    for i in range(1,lt.size(dateKeys)+1): #Recorrer
        date = lt.getElement(dateKeys,i) #Obtener llave
        node = om.get(catalog,date) #Obtener nodo
        print(node)
        nodeDateKeys = om.keySet(node) #Recorrer nodo
        for j in range(1,lt.getElement(nodeDateKeys)+1):
            ufoKey = lt.getElement(nodeDateKeys,j)
            temp = om.get(node,ufoKey)
            print(temp)
        print(node)
    return result

#def extractLatestSightByTime(catalog):
    #latestSight = 
    #for i in range():

def extractByDateRange(catalog,dateInf,dateSup):
    """
    Extrae los datos que esten en el rango de las fechas.
    """
    dateInf = datetime.datetime.strptime(dateInf,"%Y-%m-%d").date()
    dateSup = datetime.datetime.strptime(dateSup,"%Y-%m-%d").date()

    result = lt.newList()
    dateKeys = om.keys(catalog,dateInf,dateSup) #Llaves para recorrer el mapa
    for i in range(1,lt.size(dateKeys)+1): #Recorrer
        date = lt.getElement(dateKeys,i) #Obtener llave
        if ((compareDates(date,dateInf)==1) or (compareDates(date,dateInf)==0)) and ((compareDates(date,dateSup)==(-1)) or (compareDates(date,dateInf)==0)): #Verificar si esta en rango
            node = om.get(catalog,date) #Obtener nodo
            print(node)
            dateKeys = mp.keySet(node["value"]) #Llaves para recorrer el mapa
            print(dateKeys)
            for j in range(1,lt.size(node)+1):
                ufo = lt.getElement(node,j)
                print("LOL")
                print(ufo)


    return result




# Funciones utilizadas para comparar elementos dentro de una lista
def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

# Funciones de ordenamiento
def minKey(catalog):
    """
    Llave mas pequena
    """
    return om.minKey(catalog['dateIndex'])

def maxKey(catalog):
    """
    Llave mas pequena
    """
    return om.maxKey(catalog['dateIndex'])