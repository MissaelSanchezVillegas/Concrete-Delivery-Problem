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

class camion:
	def __init__(self,ida):
		self.id=ida
		self.capacidad=int
		self.costouso=float
		self.ventanastart=int
		self.ventanafinal=int
		self.origen=str
		self.final=str
	def __str__(self):
		regresar=str(self.id)
		return regresar

class deposito:
	def __init__(self,ida):
		self.id=ida
		self.mintimelag=float
		self.servtime=float
		self.ventanastart=int
		self.ventanafinal=int
		self.coord=[]
		self.particion=[]
	def __str__(self):
		regresar=str(self.id)
		return regresar

class cliente:
	def __init__(self,ida):
		self.id=ida
		self.demanda=int
		self.listcam=[]
		self.listdep=[]
		self.ventanastart=int
		self.ventanafinal=int
		self.tiempomin=int
		self.tiempomax=int
		self.primeraentrega=int
		self.servtime=float
		self.penalcost=float
		self.costoouts=float
		self.kmin=int
		self.coord=[]
		self.particion=[]
	def __str__(self):
		regresar=str(self.id)
		return regresar

def caprom(camiones):
	a=0
	b=0
	for x in camiones:
		a=a+x.capacidad
		b=b+1
	return (a/b)

def kminimo(cliente,f):
	a=cliente.demanda
	kmin=10000000
	for y in cliente.listcam:
		b=y.capacidad
		if(b<kmin):
			kmin=b
	return ceil(a/kmin)

def siguiente(numero):   #cij->ci(j+1)
	indice=0
	for a in numero:
		if(a=="s"):
			return numero[:indice+1]+str(int(numero[indice+1:])+1)
		indice=indice+1

def sint(lista):
	nuevalinea=[]
	a=lista.index("\t")
	nuevalinea.append(''.join(listainstancia[0:a]))
	for x in range(0,len(lista)):
		if(lista[-x-1]=="\t"):
			b=len(lista)-x
			nuevalinea.append(''.join(listainstancia[b:-1]))
			return nuevalinea


capacitycamion=[]
clientes=[]
origenes=[]
origenescoord=dict()
finalescoord=dict()
finales=[]
coor=[0,0]
camiones2=[]
depositos=[]
macost=dict()
matime=dict()


file= open('instancia 10_6_6_3.txt',"r")
filesol= open('solreducida.txt',"r")

startday=int(file.readline())
enday=int(file.readline())
horasdeposito=int(file.readline())
horascamion=int(file.readline())
numcamiones=int(file.readline())       
numclientes=int(file.readline())
numdepositos=int(file.readline())
numorigenes=int(file.readline())        
numfinales=int(file.readline())	
oscoord=(file.readline()[2:-1])


linea=file.readline()
while linea[0]=="o":
	origenes.append(linea[0:2])
	a=str.find(linea," ")
	b=str.find(linea," ",a+1)
	origenescoord[linea[0:2]]=[int(linea[a+1:b]),int(linea[b+1:-1])]
	linea=file.readline()
while linea[0]=="f":
	finales.append(linea[0:2])
	a=str.find(linea," ")
	b=str.find(linea," ",a+1)
	finalescoord[linea[0:2]]=[int(linea[a+1:b]),int(linea[b+1:-1])]
	linea=file.readline()


#camiones
for x in range(0,numcamiones):                #inst de camiones
	camiones2.append(camion("k" +str(x+1)))
	#print(linea[:-1])
	camiones2[x].capacidad=int(linea[3:])        #capacidad del camion k
	linea=file.readline()
	camiones2[x].costouso=int(linea[3:])               #inst de costo
	linea=file.readline()
	camiones2[x].origen=("o"+str(linea[3:-1]))
	linea=file.readline()
	camiones2[x].final=("f"+str(linea[3:-1]))
	linea=file.readline()
	for a in linea:
		a=str.find(linea," ")
		b=str.find(linea," ",a+1)
		camiones2[x].ventanastart=int(linea[a+1:b])
		camiones2[x].ventanafinal=int(linea[b+1:-1])
	linea=file.readline()

#depositos
for x in range(0,numdepositos):                            #inst de dep
	depositos.append(deposito("d"+str(x+1)))
	depositos[x].servtime=int(linea[3:])
	linea=file.readline()
	depositos[x].mintimelag=int(linea[3:])          #minimo timpo entre camioes
	linea=file.readline()
	for a in linea:
		a=str.find(linea," ")						#coordenadas
		b=str.find(linea," ",a+1)
		depositos[x].coord=[int(linea[a+1:b]),int(linea[b+1:-1])]
	linea=file.readline()    
	for a in linea:
		a=str.find(linea," ")						#ventana de tiempo
		b=str.find(linea," ",a+1)        
		depositos[x].ventanastart=int(linea[a+1:b])
		depositos[x].ventanafinal=int(linea[b+1:-1])
	linea=file.readline()


#clientes
for x in range(0,numclientes):                 #subconjuntos de camiones
	clientes.append(cliente("c"+str(x+1)))     #adicion de clientes
	clientes[x].demanda=int(linea[3:])         #instanciqa de demanda de cliente
	linea=file.readline()    
	clientes[x].servtime=int(linea[3:])					  #inst de tiempo de servicio
	linea=file.readline()  
	clientes[x].penalcost=int(linea[3:])  
	linea=file.readline() 
	clientes[x].tiempomin=int(linea[3:])
	linea=file.readline()
	clientes[x].tiempomax=int(linea[3:])           #inst
	linea=file.readline()
	for a in linea:
		a=str.find(linea," ")						#coordenadas del cliente
		b=str.find(linea," ",a+1)        
		clientes[x].coord.append(int(linea[a+1:b]))
		clientes[x].coord.append(int(linea[b+1:-1]))

	linea=file.readline()
	esp=0
	ctdr=0
	ant=0
	for a in linea[0:-1]:
		if(esp==1):
			if(a==" " and ctdr<len(linea)-2):
				clientes[x].listcam.append(camiones2[int(linea[ant+2:ctdr])-1])   #para obtener el kmin
				ant=ctdr
		if(a==" "and ctdr<len(linea)-2):
			esp=1
			ant=ctdr
		ctdr=ctdr+1
	clientes[x].listcam.append(camiones2[int(linea[ant+2:ctdr])-1])

	linea=file.readline() 
	esp=0
	ctdr=0
	ant=0
	for a in linea[0:-1]:
		if(esp==1):
			if(a==" " and ctdr<len(linea)-2):
				clientes[x].listdep.append(linea[ant+1:ctdr])
				ant=ctdr
		if(a==" "):
			esp=1
			ant=ctdr
		ctdr=ctdr+1
	clientes[x].listdep.append(linea[ant+1:ctdr])

	linea=file.readline()
	for a in linea:
		a=str.find(linea," ")						#ventana de tiempo
		b=str.find(linea," ",a+1)        
		clientes[x].ventanastart=int(linea[a+1:b])
		clientes[x].ventanafinal=int(linea[b+1:-1])
	linea=file.readline()	
	clientes[x].primeraentrega=int(linea[3:])
	linea=file.readline()

#costo outs
count=0
clcount=1
primer=0
segundo=0
for a in linea:
	count=count+1
	if(a==" "):
		primer=int(segundo)
		segundo=int(count)
		clientes[clcount-1].costoouts=float(linea[primer:segundo])
		clcount=clcount+1
	elif(a=="\n"):
		primer=int(segundo)
		segundo=int(count)
		clientes[clcount-1].costoouts=float(linea[primer:segundo])
		clcount=clcount+1


#Diccionario de costos
for o in range(0,numorigenes):
	linea=file.readline()
	costolinea=[]
	lineacount=0
	count=0
	clcount=1
	primer=0
	segundo=0
	for a in linea:
		count=count+1
		if(a==" "):
			primer=int(segundo)
			segundo=int(count)
			costolinea.append(linea[primer:segundo-1])
		elif(a=="\n"):
			clcount=clcount+1
	macost["o"+str(o+1)]=dict()
	for x in range(0,numorigenes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["o"+str(o+1)]["o"+str(x+1)]=int(costolinea[lineacount])	
		lineacount=lineacount+1
	for x in range(0,numfinales):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["o"+str(o+1)]["f"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numdepositos):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["o"+str(o+1)]["d"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numclientes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["o"+str(o+1)]["c"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1

del costolinea
for z in range(0,numfinales):
	linea=file.readline()

for z in range(0,numdepositos):
	linea=file.readline()
	costolinea=[]
	lineacount=0
	count=0
	clcount=1
	primer=0
	segundo=0
	for a in linea:
		count=count+1
		if(a==" "):
			primer=int(segundo)
			segundo=int(count)
			costolinea.append(linea[primer:segundo-1])
		elif(a=="\n"):
			clcount=clcount+1
	macost["d"+str(z+1)]=dict()
	for x in range(0,numorigenes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["d"+str(z+1)]["o"+str(x+1)]=int(costolinea[lineacount])		
		lineacount=lineacount+1
	for x in range(0,numfinales):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["d"+str(z+1)]["f"+str(x+1)]=int(costolinea[lineacount])

		lineacount=lineacount+1
	for x in range(0,numdepositos):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["d"+str(z+1)]["d"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numclientes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["d"+str(z+1)]["c"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1

del costolinea
for z in range(0,numclientes):
	linea=file.readline()
	costolinea=[]
	lineacount=0
	count=0
	clcount=1
	primer=0
	segundo=0
	for a in linea:
		count=count+1
		if(a==" "):
			primer=int(segundo)
			segundo=int(count)
			costolinea.append(linea[primer:segundo-1])
		elif(a=="\n"):
			clcount=clcount+1
	macost["c"+str(z+1)]=dict()
	for x in range(0,numorigenes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["c"+str(z+1)]["o"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numfinales):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["c"+str(z+1)]["f"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numdepositos):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["c"+str(z+1)]["d"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numclientes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			macost["c"+str(z+1)]["c"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1




del costolinea
#diccionario de tiempos
for o in range(0,numorigenes):
	linea=file.readline()
	costolinea=[]
	lineacount=0
	count=0
	clcount=1
	primer=0
	segundo=0
	for a in linea:
		count=count+1
		if(a==" "):
			primer=int(segundo)
			segundo=int(count)
			costolinea.append(linea[primer:segundo-1])
		elif(a=="\n"):
			clcount=clcount+1
	matime["o"+str(o+1)]=dict()
	for x in range(0,numorigenes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["o"+str(o+1)]["o"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numfinales):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["o"+str(o+1)]["f"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numdepositos):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["o"+str(o+1)]["d"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numclientes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["o"+str(o+1)]["c"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1

del costolinea
for z in range(0,numfinales):
	linea=file.readline()

for z in range(0,numdepositos):
	linea=file.readline()
	costolinea=[]
	lineacount=0
	count=0
	clcount=1
	primer=0
	segundo=0
	for a in linea:
		count=count+1
		if(a==" "):
			primer=int(segundo)
			segundo=int(count)
			costolinea.append(linea[primer:segundo-1])
		elif(a=="\n"):
			clcount=clcount+1
	matime["d"+str(z+1)]=dict()
	for x in range(0,numorigenes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["d"+str(z+1)]["o"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numfinales):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["d"+str(z+1)]["f"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numdepositos):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["d"+str(z+1)]["d"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numclientes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["d"+str(z+1)]["c"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1

del costolinea
for z in range(0,numclientes):
	linea=file.readline()
	costolinea=[]
	lineacount=0
	count=0
	clcount=1
	primer=0
	segundo=0
	for a in linea:
		count=count+1
		if(a==" "):
			primer=int(segundo)
			segundo=int(count)
			costolinea.append(linea[primer:segundo-1])
		elif(a=="\n"):
			clcount=clcount+1
	matime["c"+str(z+1)]=dict()
	for x in range(0,numorigenes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["c"+str(z+1)]["o"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numfinales):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["c"+str(z+1)]["f"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numdepositos):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["c"+str(z+1)]["d"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1
	for x in range(0,numclientes):
		if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
			matime["c"+str(z+1)]["c"+str(x+1)]=int(costolinea[lineacount])
		lineacount=lineacount+1











#Aqui empieza la verificacion

clientescumplidos=[]
clientesnocumplidos=[]
clientesporouts=[]                             #clientes que se encarga el outsourcer
camionessol=dict()                             #representacion de la sol en un dict
lagminmax=dict()								#diccionario para los lagmin y max
listainstancia=list(filesol.readline())
count=0
for x in range(0,len(listainstancia)):        #para obtener el valor de la solucion del txt
	if(listainstancia[-x]==" " and count==0):
		funcionobjetivosol=float(''.join(listainstancia[-x:-1]))
		count=1
count=0
countclientes=1
while(len(listainstancia)>0):
	while(len(listainstancia)>0 and listainstancia[0]!="k"):
		if(listainstancia[0]=="A"):                               #clientes que se le cumple la demanda
			for x in range(13,16):
				if(listainstancia[x]=="S"):
					clientescumplidos.append("c"+str(countclientes))
				elif(listainstancia[x]=="N"):
					clientesnocumplidos.append("c"+str(countclientes))
			countclientes=countclientes+1

		if(listainstancia[3]=="o"):                               #clientes que se le cumple la demanda via outsourcer
			clientesporouts.append("c"+str(''.join(listainstancia[52:-1])))
			

		if(count==1):
			listainstanciareducida=sint(listainstancia)
			#print(listainstanciareducida)	
			camionessol[camionactual].append((listainstanciareducida[0],float(listainstanciareducida[1])))		
		listainstancia=list(filesol.readline())
	count=1
	camionactual=''.join(listainstancia[:-1])
	listainstancia=list(filesol.readline())
	if(len(listainstancia)>0):
		camionessol[camionactual]=[]

print(camionessol)
clientespormi=list( set(clientescumplidos) - set(clientesporouts) )    #clientes que satisfago sin el outsourcer
demandaporcumplir=dict()
costototal=0
costocamionesuso=0
costoincumplimiento=0
costodeoutsourcer=0
costotransporte=0
checador=set([])

for x in clientesporouts:                       #costo del outsourcer
	costodeoutsourcer= costodeoutsourcer + clientes[int(x[1:])-1].costoouts

for x in clientesnocumplidos:                   #costo por incumplimiento
	costoincumplimiento=costoincumplimiento + clientes[int(x[1:])-1].penalcost

for x in clientespormi:
	demandaporcumplir[x]=0



for key,lista in camionessol.items():
	time=float(camionessol[key][0][1])

	#costo por usar camion
	costocamionesuso=camiones2[int(key[1:])-1].costouso+costocamionesuso


	#verificar que empiecen en un origen y terminen en un fin
	if(camionessol[key][0][0][0]!="o"):
		print("solucion infactible debido a que el camion "+key+" no inicia en origen")
	if(camionessol[key][-1][0][0]!="f"):
		print("solucion infactible debido a que el camion "+key+" no termina en final")

	#verificar que empiecen a su hora y terminen a su hora
	if(float(camionessol[key][1][1])<float(camiones2[int(key[1:])-1].ventanastart)):
		print("solucion infactible debido a que el camion "+key[1:]+" inicia antes de jornada")
	if(float(camionessol[key][-2][1])>float(camiones2[int(key[1:])-1].ventanafinal)):
		print("solucion infactible debido a que el camion "+key[1:]+" inicia despues de jornada")


	fact=0
	indice=0
	for nodo,tiempo in lista:

		#verificar que solo distribuye a clientes correctos
		if(nodo[0]=="c"):
			for camiono in clientes[int(nodo[1:nodo.index("s")])-1].listcam:
				if(camiono.id==key):
					fact=1
			if(fact==0):
				print("solucion infactible debido a que el camion "+key[1:]+" no puede repartir al cliente "+str(nodo[1:nodo.index("s")]))

		#verificar que provienen del deposito correcto
		fact=0
		if(nodo[0]=="c"):
			for depositoo in clientes[int(nodo[1:nodo.index("s")])-1].listdep:
				if(depositoo==lista[indice-1][0]):
					fact=1
			if(fact==0):
				print("solucion infactible debido a que el deposito "+lista[indice-1][0]+" no puede repartir al cliente "+str(nodo[1:nodo.index("s")]))

		#verificar que cumplen la demanda
		if(nodo[0]=="c" and (nodo[0:nodo.index("s")] in clientespormi)):
			demandaporcumplir[nodo[0:nodo.index("s")]]=demandaporcumplir[nodo[0:nodo.index("s")]] + float(camiones2[int(key[1:])-1].capacidad)



		#verificar que sigan un camino (no teletransportarse)
		if(nodo[0]=="c"):
			if(lista[indice-1][0][0]!="d"):
				print("solucion infactible debido a teleport del camion " + key[1:])
			if(lista[indice+1][0][0]!="d" and lista[indice+1][0][0]!="f"):
				print("solucion infactible debido a teleport del camion " + key[1:])
		if(nodo[0]=="d"):
			if(lista[indice+1][0][0]!="c"):
				print("solucion infactible debido a teleport del camion " + key[1:])
			if(lista[indice-1][0][0]!="c" and lista[indice-1][0][0]!="o"):
				print("solucion infactible debido a teleport del camion " + key[1:])


		#verificar las ventanas de tiempo de los clientes
		if(nodo[0]=="c"):
			if(tiempo<clientes[int(nodo[1:nodo.index("s")])-1].ventanastart):
				print("solucion infactible debido a que el camion " +key[1:]+" visita al cliente "+ nodo[1:nodo.index("s")]+ " antes de tiempo")
			if(tiempo>clientes[int(nodo[1:nodo.index("s")])-1].ventanafinal):
				print("solucion infactible debido a que el camion " +key[1:]+" visita al cliente "+ nodo[1:nodo.index("s")]+ " despues de tiempo")

		#verificar las ventanas de tiempo de los depositos
		if(nodo[0]=="d"):
			if(tiempo<depositos[int(nodo[1:])-1].ventanastart):
				print("solucion infactible debido a que el camion " +key[1:]+" visita al deposito "+ nodo[1:]+ " antes de tiempo")
			if(tiempo>depositos[int(nodo[1:])-1].ventanafinal):
				print("solucion infactible debido a que el camion " +key[1:]+" visita al deposito "+ nodo[1:]+ " despues de tiempo")

		#verificar que la primer entrega sea antes de un deadline
		if(nodo[0]=="c" and nodo[nodo.index("s")+1]=="1"):
			if(tiempo>clientes[int(nodo[1:nodo.index("s")])-1].primeraentrega):
				print("solucion infactible debido a que el cliente "+ nodo[1:nodo.index("s")]+ " recibio su primer entrega despues de tiempo")
	
		#costo de transporte
		if(nodo[0]!="f"):
			if("s" in nodo):
				costotransporte=costotransporte + macost[nodo[0:nodo.index("s")]][lista[indice+1][0]]
			elif("s" in lista[indice+1][0]):
				costotransporte=costotransporte + macost[nodo][lista[indice+1][0][0:lista[indice+1][0].index("s")]]
			else:
				costotransporte=costotransporte + float(macost[nodo][lista[indice+1][0]])

		#tiempos de traslado y serv
		if(nodo[0]!="f"):
			
			if("s" in nodo):
				time=matime[nodo[0:nodo.index("s")]][lista[indice+1][0]] + clientes[int(nodo[1:nodo.index("s")])-1].servtime
			elif("s" in lista[indice+1][0]):
				time=matime[nodo][lista[indice+1][0][0:lista[indice+1][0].index("s")]] + depositos[int(nodo[1:])-1].servtime
			else:
				time=matime[nodo][lista[indice+1][0]]

			if((lista[indice+1][1]-tiempo)<time):
				print("solucion erronea debido a que el los tiempos no son correctos")
			

		#crear nuevo dict para los lagmin y max
		if(nodo[0]=="c"):
			nodon=nodo[0:nodo.index("s")]
		else:
			nodon=nodo
		if(nodon not in checador):
			lagminmax[nodon]=[]
			lagminmax[nodon].append(tiempo)
			checador.add(nodon)
		else:
			lagminmax[nodon].append(tiempo)






		indice=indice+1


#continuacion de fact de demanda
for key,valor in demandaporcumplir.items():
	if(clientes[int(key[1:])-1].demanda>valor):
		print("solucion infactible debido a que el cliente "+key[1]+" realmente no se cumple con la demanda")

#verificar si el costo total es correcto
costototal=costoincumplimiento+costodeoutsourcer+costocamionesuso+costotransporte
if(float(costototal)!=funcionobjetivosol):
	print("solucion erronea debido a que el los costos no coinciden")



for lists in lagminmax.values():       #ordenar los tiempos
	lists.sort()
for keys,lists in lagminmax.items():
	indice=0
	if(keys[0]=="d" and len(lists)>1):
		for x in lists[0:-1]:	
			if(lists[indice+1]-x<depositos[int(keys[1:])-1].mintimelag):
				print("solucion infactible debido a que violan el lagmin del deposito "+key[1:])

			indice=indice+1
	elif(keys[0]=="c" and len(lists)>1):
		for x in lists[0:-1]:
			if(lists[indice+1]-x<clientes[int(keys[1:])-1].tiempomin):
				print("solucion infactible debido a que violan el lagmin del cliente "+key[1:])
			if(lists[indice+1]-x>clientes[int(keys[1:])-1].tiempomax):
				print("solucion infactible debido a que violan el lagmax del cliente "+key[1:])

			indice=indice+1



file.close()


