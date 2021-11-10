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
    catalog['duration'] = om.newMap(omaptype='RBT',
                                        comparefunction=None)                        
    catalog["timeIndex"] = om.newMap(omaptype='RBT',
                                      comparefunction=compareHours) #TODO Configurar para filtrar por hora   
    catalog['area'] = om.newMap(omaptype='RBT',
                                      comparefunction=None)                            

    return catalog

# Funciones para agregar informacion al catalogo

def getLonRange(catalog, min, max):
    return om.values(catalog['area'], min, max)

def getLatRange(list, minLat, maxLat):
    size = lt.size(list)
    newList = lt.newList('ARRAY_LIST', None)
    for pos in range(1,size+1):
        temp =lt.getElement(list, pos)
        tempList = om.values(temp, minLat,maxLat)
        for ind in range(1, lt.size(tempList)+1):
            tList = lt.getElement(tempList,ind)
            for ind2 in range(1, lt.size(tList)+1):
                to_add = lt.getElement(tList, ind2)
                lt.addLast(newList, to_add)
    ms.sort(newList, sortLat)
    return newList, lt.size(newList)

def sortLat(item1, item2):
    if item1['latitude'] < item2['latitude']:
        return True
    else:
        return False

def addLon(catalog, sight):
    map = catalog['area']
    long =  round(float(sight['longitude']),2)
    lat =  round(float(sight['latitude']),2)
    if not om.contains(map, long):
        latMap = om.newMap(omaptype='RBT',
                                      comparefunction=None)  
        om.put(map, long, latMap)
    to_add = onlyMapValue(map, long)
    lst = lt.newList('ARRAY_LIST', None)
    if not om.contains(to_add, lat):
        om.put(to_add,lat,lst )
    latList = onlyMapValue(to_add, lat)
    lt.addLast(latList, sight)

def countCity(catalog, city):
    map = catalog['cityIndex'] #Seleccion del mapa de ciudades
    size =  (om.size(map)) #Tamaño
    height = (om.height(map)) #Altura
    cityList = onlyMapValue(map, city) #Accede a los datos
    citySize = lt.size(cityList) #Tamaño del grupo de datos
    ms.sort(cityList, sortDate) #Organizar datos de la ciudad segun la fecha
    table = agregarTabla(cityList, 3) #Obtener los 3 primeros y 3 ultimos
    return size, height, citySize, table #Tupla de datos

def addDuration(catalog, sight):
    map = catalog['duration']
    duration =  float(sight['duration (seconds)'])
    if not om.contains(map, duration):
        timeList = lt.newList('ARRAY_LIST', None)
        om.put(map, duration, timeList)
    to_add = onlyMapValue(map, duration)
    lt.addLast(to_add, sight)

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
    map = catalog["timeIndex"] #Selecciona el mapa de horas
    timeKeys = om.keys(map,timeMin,timeMax) #Llaves de los datos en el rango de tiempo

    for i in range (1,lt.size(timeKeys)+1): #Recorre el mapa
        timeTemp = lt.getElement(timeKeys,i) #Obtiene una hora
        timeList = onlyMapValue(map, timeTemp) #Accede a los datos
        timeListSize = lt.size(timeList)
        for j in range(1,timeListSize+1):
            tempData = lt.getElement(timeList,j)
            lt.addLast(result,tempData) #Añade a los datos del DataFrame


    latestSight = om.maxKey(map) #Llave del registro mas tardio en el mapa
    countLatestSight = lt.size(onlyMapValue(map,latestSight)) #Numero de registros

    latestTime = {}
    latestTime["0"] = latestSight,countLatestSight
    latestDF = pd.DataFrame.from_dict(latestTime, orient='index', columns= ["time","count"])

    print(result)
    #ms.sort(result, sortHours) #Organizar datos del rango segun la hora #TODO: Arreglar sort
    differentTimes = om.size(map) #Horas registradas unicas
    rangeSize = lt.size(result) #Cantidad de vistas en el rango de horas
    table = agregarTabla(result,3) #Obtener los 3 primeros y 3 ultimos
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

#Req4
def countDate (catalog,dateMin,dateMax):
    dateMin = datetime.datetime.strptime(dateMin,"%Y-%m-%d") #Conversion a datetime
    dateMin = dateMin.date() #Extraccion de fecha
    dateMax = datetime.datetime.strptime(dateMax,"%Y-%m-%d")
    dateMax = dateMax.date()

    result = lt.newList("ARRAY_LIST", None) #Almacenamiento de datos para DataFrame
    latestSight = datetime.datetime.now() #Almacenamiento del registro mas antiguo
    latestSight = latestSight.time() #Conversion a formato de fecha
    countLatestSight = 0 #Contador de registros con la misma fecha
    map = catalog["dateIndex"] #Selecciona el mapa de fechas
    dateKeys = om.keys(map,dateMin,dateMax) #Llaves de los datos en el rango de fechas
    

    for i in range (1,lt.size(dateKeys)+1): #Recorre el mapa
        dateTemp = lt.getElement(dateKeys,i) #Obtiene una fecha
        dateList = onlyMapValue(map, dateTemp) #Accede a los datos
        print(dateList)
        dateListSize = lt.size(dateList) #Obtiene el numero de registros
        for j in range(1,dateListSize+1):
            tempData = lt.getElement(dateList,j) #Obtiene un registro
            lt.addLast(result,tempData) #Añade a los datos del DataFrame

    latestSight = om.minKey(map)
    countLatestSight = lt.size(onlyMapValue(map,latestSight))

    latestDate = {}
    latestDate["0"] = latestSight,countLatestSight
    latestDF = pd.DataFrame.from_dict(latestDate, orient='index', columns= ["date","count"])

    print(result)
    differentDates = om.size(map) #Horas registradas unicas
    rangeSize = lt.size(result) #Cantidad de vistas en el rango de horas
    table = agregarTabla(result,3) #Obtener los 3 primeros y 3 ultimos
    return (differentDates,latestDF,rangeSize,table) #Tupla de datos


def sortDate(item1,item2):
    if item1['datetime'] < item2['datetime']:
        return True
    else:
        return False

def mapSize(map):
    return om.size(map)

def addSight(catalog, sight):
    lt.addLast(catalog['sights'], sight)
    updateDateIndex(catalog['dateIndex'], sight)
    return catalog

def updateDateIndex(catalog, sight):
    occurreddate = sight['datetime'] #Obtiene la fecha del avistamiento
    sightDate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S') #Convierte en formato de fecha y hora
    entry = om.get(catalog, sightDate.date()) #Obtiene el mapa de la fecha
    if entry is None:
        datentry = lt.newList('ARRAY_LIST', None)
        om.put(catalog, sightDate.date(), datentry)
    temp = onlyMapValue(catalog, sightDate.date())
    lt.addLast(temp, sight)
    

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

def getData(lst):
    return  lt.size(lst)

def getDurRange(map, min, max):
    return om.values(map, min, max)
    

def getAllItems(lst):
    newList = lt.newList('ARRAY_LIST', None)
    size = lt.size(lst)
    for pos in range(1,size+1):
        item =  lt.getElement(lst, pos)
        for sec in range(1, lt.size(item)+1):
            temp = lt.getElement(item,sec)
            lt.addLast(newList,temp)

    ms.sort(newList, compDur)
    return newList, lt.size(newList)

def compDur(dur1, dur2):
    """
    Compara dos fechas
    """
    if (float(dur1['duration (seconds)']) < float(dur2['duration (seconds)'] )):
        return True
    else:
        return False


def maxMap(map):

    return om.maxKey(map)
    

def onlyMapValue(map, key):
    pair = om.get(map, key)
    value = me.getValue(pair)
    return value



# Funciones de consulta
def getTen(list):
    return agregarTabla(list,5)


def agregarTabla(list,len):
    artStr = { }
    size = lt.size(list)
    if len == 5:
        for pos in range(1, len+1): 
            temp = lt.getElement(list, pos)
            artStr[pos] = temp['datetime'],temp['city'],temp['state'], temp['country'],temp['shape'],temp['duration (seconds)'],temp['date posted'], temp['latitude'] , temp['longitude'] 
        for pos in range(size-len+1, size+1): 
            temp = lt.getElement(list, pos)
            artStr[pos] = temp['datetime'],temp['city'],temp['state'], temp['country'],temp['shape'],temp['duration (seconds)'],temp['date posted'], temp['latitude'] , temp['longitude'] 
        return  (pd.DataFrame.from_dict(artStr, orient='index', columns= ['datetime', 'city', 'state', 'country', 'shape', 'duration (seconds)', 'date posted', 'latitude', 'longitude']))
    else:
        for pos in range(1, len+1): 
            temp = lt.getElement(list, pos)
            artStr[pos] = temp['datetime'],temp["datetime"][:11],temp['city'],temp['state'], temp['country'],temp['shape'],temp['duration (seconds)']
        for pos in range(size-len+1, size+1): 
            temp = lt.getElement(list, pos)
            artStr[pos] = temp['datetime'],temp['datetime'][:11],temp['city'],temp['state'], temp['country'],temp['shape'],temp['duration (seconds)'] 
        return  (pd.DataFrame.from_dict(artStr, orient='index', columns= ['datetime', "date", 'city', 'state', 'country', 'shape', 'duration (seconds)']))



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
    -1: hour1 es menor
    """
    if (hour1 == hour2):
        return 0
    elif (hour1 > hour2):
        return 1
    else:
        return -1

def sortHours(item1,item2):
    if item1['datetime'].time() < item2['datetime'].time():
        return True
    else:
        return False

def sortOnlyDates(item1,item2):
    print(item1)
    print("-")
    print(item2)
    if item1['datetime'].date() < item2['datetime'].date():
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