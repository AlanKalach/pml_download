#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 20:37:57 2019

@author: jkalach
"""

import pandas as pd
import numpy as ny
import json
import urllib
from datetime import datetime
from datetime import timedelta

base_link="https://ws01.cenace.gob.mx:8082/SWPML/SIM/"
links=[]

#Parametros requeridos por el programa - input unico
parameters=["BCS","MDA","07TCB-115","2024","01","01","2024","06","01","JSON"]
# parameters=["Sistema Eléctrico","Mercado","Nodo(s)","Año Inicial","Mes Inicial","Día Inicial",
#             "Año Final","Mes Final","Dia Final","Formato de Salida"]
#Sistema eléctrico: SIN, BCA, BCS.
#Mercado: MDA,MTR
#Lista de nodos de los cuales se desea obtener información 
#   (La lista de nodos debe ser separada por comas sin espacio).
#Año inicial, para un periodo de tiempo. Formato AAAA
#Mes inicial, para un periodo de tiempo. Formato MM
#Día Inicial, para un periodo de tiempo. Formato DD
#Año final, para un periodo de tiempo. Formato AAAA
#Mes final, para un periodo de tiempo. Formato MM
#Día final, para un periodo de tiempo. Formato DD
#Formato de salida XML o JSON, por omisión es XML (Opcional)

#Nombre del archivo de excel de salida
file_name = "PMLs"+parameters[2]+"-"+parameters[3]+parameters[4]+parameters[5]+"-"+parameters[6]+parameters[7]+parameters[8]+".xlsx"

#Calculo del intervalo de dias requerido

initial_date = datetime(int(parameters[3]),int(parameters[4]),int(parameters[5]))
final_date = datetime(int(parameters[6]),int(parameters[7]),int(parameters[8]))
time_delta = final_date-initial_date
time_delta_num=time_delta.days

#Si el intervalo de dias es menor a 6, se hace el proceso 1 vez

if time_delta_num <=6:
    #Concatenar Link de acuerdo a la sintaxis del CENACE
    for i in range(len(parameters)):
    #Arreglar formato 0 al principio en días y meses
        if len(parameters[i])<2:
            parameters[i]="0"+parameters[i]
        base_link=base_link+"/"+parameters[i]
    links.append(base_link)
    base_link="https://ws01.cenace.gob.mx:8082/SWPML/SIM/"

#Si el intervalo de dias es mayor a 6, se entra en el loop para generar varios links
else:
    intermediate_date1 = initial_date
    while time_delta_num > 6:
        intermediate_date2 = intermediate_date1 + timedelta(days=6)
        time_delta = final_date - intermediate_date2
        time_delta_num=time_delta.days
        parameters[3]= str(intermediate_date1.year)
        parameters[4]= str(intermediate_date1.month)
        parameters[5]= str(intermediate_date1.day)
        parameters[6]= str(intermediate_date2.year)
        parameters[7]= str(intermediate_date2.month)
        parameters[8]= str(intermediate_date2.day)

                    #Concatenar Link de acuerdo a la sintaxis del CENACE
        for i in range(len(parameters)):
        #Arreglar formato 0 al principio en días y meses
            if len(parameters[i])<2:
                parameters[i]="0"+parameters[i]
            base_link=base_link+"/"+parameters[i]
        links.append(base_link)
        base_link="https://ws01.cenace.gob.mx:8082/SWPML/SIM/"
        intermediate_date1 = intermediate_date2 + timedelta(days=1)
        
#El último intervalo menor a 6 se ejecuta de manera separada y al final
    if time_delta_num >0:
        intermediate_date2 = intermediate_date1 + timedelta(days=time_delta_num-1)
        parameters[3]= str(intermediate_date1.year)
        parameters[4]= str(intermediate_date1.month)
        parameters[5]= str(intermediate_date1.day)
        parameters[6]= str(intermediate_date2.year)
        parameters[7]= str(intermediate_date2.month)
        parameters[8]= str(intermediate_date2.day)
    
#Concatenar Link de acuerdo a la sintaxis del CENACE
        for i in range(len(parameters)):
                        #Arreglar formato 0 al principio en días y meses
            if len(parameters[i])<2:
                parameters[i]="0"+parameters[i]
            base_link=base_link+"/"+parameters[i]
        links.append(base_link)
        base_link="https://ws01.cenace.gob.mx:8082/SWPML/SIM/"
        

#Descargar JSON de información nodal a una variable llamada data (diccionario)
df_list=[]
for i in range(len(links)):
    response = urllib.request.urlopen(links[i])
    data = json.loads(response.read())
#Almacenar diccionarios de datos en una lista
    data = pd.DataFrame(data['Resultados'][0]['Valores'])  # transpose to look just like the sheet above
    df_list.append(data)

#Escribir un Excel con la información del diccionario "data" de manera iterativa
writer = pd.ExcelWriter(file_name,engine='xlsxwriter')
row = 0
for i in range(len(df_list)):
#el encabezado solo se utiliza en la primera iteración
    if i<=0:
        df_list[i].to_excel(writer,sheet_name="Validation",startrow=row , startcol=0)   
        row = row + len(df_list[i].index) + 1
    else:
        df_list[i].to_excel(writer,sheet_name="Validation",startrow=row , startcol=0, header=False)   
        row = row + len(df_list[i].index) + 0
writer.save()

    