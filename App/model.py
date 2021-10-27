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
def init():
    catalog = {'crimes': None,
                'dateIndex': None
                }

    catalog['sights'] = lt.newList('ARRAY_LIST', None)
    catalog['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return catalog

# Funciones para agregar informacion al catalogo
def addSight(catalog, sight):
    lt.addLast(catalog['crimes'], sight)
    updateDateIndex(catalog['dateIndex'], sight)
    return catalog

def updateDateIndex(catalog, sight):
    occurreddate = sight['datetime']
    crimedate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, crimedate.date())
    if entry is None:
        datentry = newDataEntry(sight)
        om.put(map, crimedate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, sight)
    return map

def addDateIndex(date, sight):

    lst = datentry['lstcrimes']
    lt.addLast(lst, crime)
    offenseIndex = datentry['offenseIndex']
    offentry = m.get(offenseIndex, crime['OFFENSE_CODE_GROUP'])
    if (offentry is None):
        entry = newOffenseEntry(crime['OFFENSE_CODE_GROUP'], crime)
        lt.addLast(entry['lstoffenses'], crime)
        m.put(offenseIndex, crime['OFFENSE_CODE_GROUP'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstoffenses'], crime)
    return datentry

# Funciones para creacion de datos

# Funciones de consulta

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
