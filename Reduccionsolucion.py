from random import randint
from random import random
from random import choice
from math import ceil
from math import floor
from math import sqrt
from scipy.stats import norm
import numpy as np
import string
import scipy.stats as stats

def listesp(lista):                    #funcion que quita los espacios
	nuevalista=[]
	for x in lista:
		if(x!=" "):
			nuevalista.append(x)
	return nuevalista

def sino(lista):                             #me dice si la variable x es 1 o no
	count=0
	indice=0
	for x in lista:
		if(x=="."):
			count=count+1
		if(count==4):
			if(lista[indice-1]=="1"):
				return True
			else:
				return False
		indice=indice+1

def sino2(lista):                             #me dice si la variable y o h es 1 o no
	count=0
	indice=0
	for x in lista:
		if(x=="."):
			count=count+1
		if(count==2):
			if(lista[indice-1]=="1"):
				return True
			else:
				return False
		indice=indice+1

def sitiempo(lista):                      #me regresa el valor de la variable w si existe
	count=0
	indice=0
	nuevalista=[]
	for x in lista:
		if(x=="."):
			count=count+1
		if(count==2 and x!="."):
			nuevalista.append(x)
		if(count==3):
			if(lista[indice+5]=="E" and lista[indice+4]=="0"):
				return 0
			elif(lista[indice-1]=="."):
				return "False"
			else:
				for y in range(0,3):
					nuevalista.append(lista[indice+y])
				if(float(''.join(nuevalista))>100):
					return nuevalista
				else:
					return 0
		indice=indice+1

def costo(lista):                      #me regresa el valor de la variable z
	indice=0
	nuevalista=[]
	for x in lista:
		if(x=="F"):
			primer=indice+1
		if(x=="+"):
			ultimo=indice-1
			for y in lista[primer:ultimo]:
				nuevalista.append(y)
			return nuevalista
		indice=indice+1

def nodollegadaycamion(lista):                      #me regresa el node de llegada y el camion en lo que respecta a la variable w
	indice=0
	copia=lista.copy()
	nuevalista=[]
	count=0
	aux=0
	for x in lista:
		if(x=="." and count==1):
			ultimo=indice
			nuevalista.append(''.join(lista[primerultimo+1:ultimo]))
			return nuevalista
		if(x=="." and count==0 and lista[0]!="d"):
			primerultimo=indice
			count=count+1
			nuevalista.append(''.join(copia[0:primerultimo]))
		if(x=="s" and lista[0]=="d"):
			aux=indice
		if(x=="." and count==0 and lista[0]=="d"):
			primerultimo=aux
			count=count+1
			nuevalista.append(''.join(copia[0:primerultimo]))
			primerultimo=indice	
		indice=indice+1

def numerodecamiones(lista):                                    #me regresa cuantos camiones hay
	indice=0
	count=0
	for x in lista:
		if(x=="/" and count==1):
			for y in range(1,5):
				if(lista[indice-y]=="k"):
					primer=indice-y+1
					return int(''.join(lista[primer:indice]))
		if(x=="/"):
			count=count+1
		indice=indice+1

f= open('solreducida.txt',"w")
file2= open('solgamsa.txt',"r")
listalinea=list(file2.readline())
ver0=list("VAR z")
ver=list("VAR x")
ver2=list("VAR w")
ver3=list("VAR y")
ver4=list("VAR h")
camionesd=dict()
numcamiones=0
liscamiones=dict()
clientesacumplir=[]
contador=1
contador2=1
contador3=1

while (len(listalinea)>0):                                   #llega a la parte de la solucion
	listalinea=list(file2.readline())

	if(len(listalinea)>20 and listalinea[17]=="c" and listalinea[18]=="a" and listalinea[19]=="m"):
		numcamiones=numerodecamiones(listalinea)
		for x in range(1,numcamiones+1):
			liscamiones['k'+str(x)]=[]


	if(len(listalinea)>10 and listalinea[5:10]==ver0): #trabajar con las variable z (fcn obj)
		listalinea=listesp(listalinea)
		cost=''.join(costo(listalinea))                #valor de fcn obj
		listalinea=list(file2.readline())
		print(cost)
		f.write("La instancia se resolvio con una funcion objetivo encontrada de "+str(cost)+"\n")



	if(len(listalinea)>10 and listalinea[5:10]==ver2): #trabajar con las variables w
		for x in range(0,3):								 #deshacerse de cosas inecesarias
			listalinea=list(file2.readline())
		listalinea=list(file2.readline())
		while (listalinea[0]!="\n"):   				#llega hasta la ultima variable w
			listalinea=listesp(listalinea)
			valor=sitiempo(listalinea)
			if(valor!="False"):
				if(valor!=0):
					valor=''.join(valor)
					listalinea=nodollegadaycamion(listalinea)
					camionesd[contador3]=[]
					camionesd[contador3]=[float(valor),listalinea[0],listalinea[1]]
					contador3=contador3+1
			listalinea=list(file2.readline())
		for key,values in camionesd.items():
			liscamiones[values[2]].append((values[0],key))

    
	if(len(listalinea)>10 and listalinea[5:10]==ver3): #trabajar con las variables y
		for x in range(0,3):								 #deshacerse de cosas inecesarias
			listalinea=list(file2.readline())
		listalinea=list(file2.readline())
		while (listalinea[0]!="\n"):
			listalinea=listesp(listalinea)
			if(sino2(listalinea)):        
				f.write("Al cliente "+str(contador)+" SI se le cumple su demanda\n")
			else:
				f.write("Al cliente "+str(contador)+" NO se le cumple su demanda\n")           
			contador=contador+1
			listalinea=list(file2.readline())


	if(len(listalinea)>10 and listalinea[5:10]==ver4): #trabajar con las variables h
		for x in range(0,3):								 #deshacerse de cosas inecesarias
			listalinea=list(file2.readline())
		listalinea=list(file2.readline())
		while (listalinea[0]!="\n"):
			listalinea=listesp(listalinea)
			if(sino2(listalinea)):
				f.write("El outsourcer se encargara de distribuir al cliente "+str(contador2)+"\n")        
			contador2=contador2+1
			listalinea=list(file2.readline())


			
for x in range(1,numcamiones+1):
	if(len(liscamiones['k'+str(x)])==0):
		f.write("El camion "+str(x)+" NO sera utilizado en este problema por lo cual terminara su jornada inmediatamente\n")
		del liscamiones['k'+str(x)]

print(camionesd)


for key,lists in liscamiones.items():
	f.write(key+"\n")
	lists.sort()
	for tiempo in lists:
		f.write(camionesd[tiempo[1]][1]+"		"+str(tiempo[0])+"\n")


f.close()
file2.close()
