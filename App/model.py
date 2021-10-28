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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


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
def sightSize(catalog):
    return lt.size(catalog['sights'])

def init():
    catalog = {'sights': None,
                'dateIndex': None
                }

    catalog['sights'] = lt.newList('ARRAY_LIST', None)
    catalog['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return catalog

# Funciones para agregar informacion al catalogo
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

# Funciones para creacion de datos

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

def citySights(catalog,city):
     
    catalog[city] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    sightsCount = 0

    for i in range(0,lt.size(catalog["sights"])+1):
        temp = lt.getElement(catalog["sights"],i)
        if temp["city"] == city:
            om.put(catalog[city],temp["datetime"],temp)
            sightsCount += 1

    
    

    return (sightsCount)


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