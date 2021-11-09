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


from DISClib.DataStructures.bst import height
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
import pandas as pd
assert cf
import datetime
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def init():
    catalog = {'sights': None,
                'dateIndex': None
                }

    catalog['sights'] = lt.newList('ARRAY_LIST', None)
    catalog['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    catalog['cityIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=None)
    catalog["timeIndex"] = om.newMap(omaptype='RBT',
                                      comparefunction=None) #TODO Configurar para filtrar por hora                               
    return catalog

# Funciones para agregar informacion al catalogo

def countCity(catalog, city):
    map = catalog['cityIndex'] #Seleccion del mapa de ciudades
    size =  (om.size(map)) #Tamaño
    height = (om.height(map)) #Altura
    cityList = onlyMapValue(map, city) #Accede a los datos
    citySize = lt.size(cityList) #Tamaño del grupo de datos
    ms.sort(cityList, sortDate) #Organizar datos de la ciudad segun la fecha
    table = agregarTabla(cityList) #Obtener los 3 primeros y 3 ultimos
    return size, height, citySize, table #Tupla de datos

def addCity(catalog, sight):
    map = catalog['cityIndex']
    city =  sight['city']
    time = sight['datetime']
    time =  datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    if not om.contains(map, city):
        timeList = lt.newList('ARRAY_LIST', None)
        om.put(map, city, timeList)
    to_add = onlyMapValue(map, city)
    lt.addLast(to_add, sight)

#Req 3
def countTime(catalog,timeMin,timeMax):
    timeMin = datetime.datetime.strptime(timeMin,"%H:%M") #Conversion a datetime
    timeMin = timeMin.time() #Extraccion de hora
    timeMax = datetime.datetime.strptime(timeMax,"%H:%M")
    timeMax = timeMax.time()

    result = lt.newList("ARRAY_LIST", None) #Almacenamiento de datos para DataFram
    latestSight = datetime.datetime.strptime("00:00", "%H:%M") #Almacenamiento del registro mas tardio
    latestSight = latestSight.time() #Conversion a formato de hora
    countLatestSight = 0 #Contador de registros con la misma hora
    map = catalog["timeIndex"] #Selecciona el mapa de horas
    timeKeys = om.keys(map,timeMin,timeMax) #Llaves de los datos en el rango de tiempo

    for i in range (1,lt.size(timeKeys)+1): #Recorre el mapa
        timeTemp = lt.getElement(timeKeys,i) #Obtiene una hora
        timeList = onlyMapValue(map, timeTemp) #Accede a los datos
        timeListSize = lt.size(timeList)
        for i in range(1,timeListSize+1):
            tempData = lt.getElement(timeList,i)
            lt.addLast(result,tempData) #Añade a los datos del DataFrame

        compare = compareHours(timeTemp,latestSight) #Comparar si es mas tarde que el anterior
        if compare == 0: #Si son iguales
            countLatestSight+=1 #Uno mas al contador
        elif compare == 1: #Si el dato temporal es mas tarde
            latestSight = timeTemp
            countLatestSight = 1

    latestTime = {}
    latestTime["0"] = latestSight,countLatestSight
    latestDF = pd.DataFrame.from_dict(latestTime, orient='index', columns= ["time","count"])

    print(result)
    ms.sort(result, sortHours) #Organizar datos del rango segun la hora #TODO: sort de horas
    differentTimes = om.size(map) #Horas registradas unicas
    rangeSize = lt.size(result) #Cantidad de vistas en el rango de horas
    table = agregarTabla(result) #Obtener los 3 primeros y 3 ultimos
    return (differentTimes,latestDF,rangeSize,table) #Tupla de datos
    
def addTime(catalog,sight):
    map = catalog['timeIndex']
    time = sight['datetime'][11:16]
    time =  datetime.datetime.strptime(time, '%H:%M')
    hour = time.time()
    if not om.contains(map, hour):
        timeList = lt.newList('ARRAY_LIST', None)
        om.put(map, hour, timeList)
    to_add = onlyMapValue(map, hour)
    lt.addLast(to_add, sight)


def sortDate(item1,item2):
    if item1['datetime'] < item2['datetime']:
        return True
    else:
        return False

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
def getTen(list):
    return agregarTabla(list)


def agregarTabla(list):
    artStr = { }
    size = lt.size(list)
    for pos in range(1, 6): 
        temp = lt.getElement(list, pos)
        artStr[pos] = temp['datetime'],temp['city'],temp['state'], temp['country'],temp['shape'],temp['duration (seconds)'],temp['date posted'], temp['latitude'] , temp['longitude'] 
    for pos in range(size-4, size+1): 
        temp = lt.getElement(list, pos)
        artStr[pos] = temp['datetime'],temp['city'],temp['state'], temp['country'],temp['shape'],temp['duration (seconds)'],temp['date posted'], temp['latitude'] , temp['longitude'] 
    
    return  (pd.DataFrame.from_dict(artStr, orient='index', columns= ['datetime', 'city', 'state', 'country', 'shape', 'duration (seconds)', 'date posted', 'latitude', 'longitude']))


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
    return lt.size(catalog['sights']), om.height(catalog['dateIndex']),



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

def compareHours(hour1,hour2):
    """
    Compara dos horas

    0: Son iguales
    1: hour1 es mayor
    2: hour1 es menor
    """
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
        return 1
    else:
        return -1

def sortHours(item1,item2):
    if item1['datetime'] < item2['datetime']:
        return True
    else:
        return False

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