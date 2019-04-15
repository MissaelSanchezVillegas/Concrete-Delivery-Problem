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
		self.kmin=int
		self.coord=[]
		self.particion=[]
	def __str__(self):
		regresar=str(self.id)
		return regresar

def conj(nombre, texto, lista, f):    #funcion que escribe un conjunto en gams
	f.write(str(nombre))
	f.write(" ")
	f.write(str(texto))
	f.write(" ")  
	f.write("/") 
	if(type(lista)==list):
		for x in lista:
			f.write(str(x)) 
			if(x!=lista[-1]):
				f.write(",")
	else:
		f.write(str(lista))
	f.write("/")
	f.write("\n")

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

def partdep(deposito,clientes):
	count=0
	for y in clientes:
		for z in y.listdep:
			if(deposito.id==z):
				count=count+len(y.particion)
	return count


numreplica=4
for replica in range(0,numreplica):
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


	file= open("instancia 10_6_6_"+str(replica)+".txt","r")

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

	f = open("instanciagams "+str(numcamiones)+"_"+str(numclientes)+"_"+str(numdepositos)+"_"+str(replica)+".gms","w");
	f.write("option ResLim=1800;\n")
	f.write("sets")

	#camiones
	for x in range(0,numcamiones):                #inst de camiones
		indice=linea.index(" ")
		camiones2.append(camion("k" +str(x+1)))
		#print(linea[indice+1:-1])
		camiones2[x].capacidad=int(linea[indice+1:-1])        #capacidad del camion k
		linea=file.readline()
		camiones2[x].costouso=int(linea[indice+1:-1])               #inst de costo
		linea=file.readline()
		camiones2[x].origen=("o"+str(linea[indice+1:-1]))
		linea=file.readline()
		camiones2[x].final=("f"+str(linea[indice+1:-1]))
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
		indice=linea.index(" ")
		depositos[x].servtime=int(linea[indice+1:])
		linea=file.readline()
		depositos[x].mintimelag=int(linea[indice+1:])          #minimo timpo entre camioes
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


	f.write("\n")
	f.write("k")
	f.write(" ")
	f.write("lista de camiones")
	f.write(" ")  
	f.write("/") 
	for x in range(0,len(camiones2)):
		#print(camiones2[x])
		f.write(str(camiones2[x].id)) 
		if(x!=len(camiones2)-1):
			f.write(",")
	f.write("/")
	f.write("\n")
	conj("o","lista de origenes",origenes,f)
	conj("f","lista de finales",finales,f)

	for x in range(0,len(camiones2)):             #origen del camion
		f.write("ok"+str(x+1)+"(o)")
		f.write(" ")
		f.write("origen de camion k"+str(x+1))
		f.write(" ")  
		f.write("/") 
		f.write(str(camiones2[x].origen)) 
		f.write("/")
		f.write("\n")
	for x in range(0,len(camiones2)):             #origen del camion
		f.write("fk"+str(x+1)+"(f)")
		f.write(" ")
		f.write("final de camion k"+str(x+1))
		f.write(" ")  
		f.write("/") 
		f.write((camiones2[x].final)) 
		f.write("/")
		f.write("\n")


	#clientes
	for x in range(0,numclientes):                 #subconjuntos de camiones
		clientes.append(cliente("c"+str(x+1)))     #adicion de clientes
		indice=linea.index(" ")
		clientes[x].demanda=int(linea[indice+1:])         #instanciqa de demanda de cliente
		linea=file.readline()    
		clientes[x].servtime=int(linea[indice+1:])					  #inst de tiempo de servicio
		linea=file.readline()  
		clientes[x].penalcost=int(linea[indice+1:])  
		linea=file.readline() 
		clientes[x].tiempomin=int(linea[indice+1:])
		linea=file.readline()
		clientes[x].tiempomax=int(linea[indice+1:])           #inst
		linea=file.readline()
		for a in linea:
			a=str.find(linea," ")						#coordenadas del cliente
			b=str.find(linea," ",a+1)        
			clientes[x].coord.append(int(linea[a+1:b]))
			clientes[x].coord.append(int(linea[b+1:-1]))

		linea=file.readline()
		f.write("ck"+str(x+1))
		f.write(" ")
		f.write("subconjunto de camiones del cliente "+str(x+1))
		f.write(" ")  
		f.write("/") 
		esp=0
		ctdr=0
		ant=0
		for a in linea[0:-1]:
			if(esp==1):
				if(a==" " and ctdr<len(linea)-2):
					f.write(",")
					clientes[x].listcam.append(camiones2[int(linea[ant+2:ctdr])-1])   #para obtener el kmin
					ant=ctdr
				else:
					f.write(str(a))
			if(a==" "and ctdr<len(linea)-2):
				esp=1
				ant=ctdr
			ctdr=ctdr+1
		clientes[x].listcam.append(camiones2[int(linea[ant+2:ctdr])-1])
		f.write("/")
		f.write("\n")
		clientes[x].kmin=kminimo(clientes[x],f)


		linea=file.readline()
		f.write("cd"+str(x+1))
		f.write(" ")
		f.write("subconjunto de depositos del cliente "+str(x+1))
		f.write(" ")  
		f.write("/") 
		esp=0
		ctdr=0
		ant=0
		for a in linea[0:-1]:
			if(esp==1):
				if(a==" " and ctdr<len(linea)-2):
					f.write(",")
					clientes[x].listdep.append(linea[ant+1:ctdr])
					ant=ctdr
				else:
					f.write(str(a))
			if(a==" "):
				esp=1
				ant=ctdr
			ctdr=ctdr+1
		clientes[x].listdep.append(linea[ant+1:ctdr])
		f.write("/")
		f.write("\n")

		linea=file.readline()
		for a in linea:
			a=str.find(linea," ")						#ventana de tiempo
			b=str.find(linea," ",a+1)        
			clientes[x].ventanastart=int(linea[a+1:b])
			clientes[x].ventanafinal=int(linea[b+1:-1])
		linea=file.readline()	
		clientes[x].primeraentrega=int(linea[3:])
		linea=file.readline()	

	f.write("c")                        #conjunto de clientes
	f.write(" ")
	f.write("conjunto de clientes")
	f.write(" ")  
	f.write("/") 
	for x in range(0,numclientes):
		f.write(str(clientes[x].id))
		if(x!=numclientes-1):
			f.write(",")
	f.write("/")
	f.write("\n")


	for x in range(0,numclientes):
		f.write("cs"+str(x+1))                        #conjunto de clientes
		f.write(" ")
		f.write("particion de cliente "+str(x+1))
		f.write(" ")  
		f.write("/")
		to=clientes[x].kmin
		for y in range(0,to):
			clientes[x].particion.append("c"+str(x+1)+"s"+str(y+1))
			f.write("c"+str(x+1)+"s"+str(y+1))
			if(y!=(to-1)):
				f.write(",")
		f.write("/")
		f.write("\n")

	f.write("d")                        #conjunto de depositos
	f.write(" ")
	f.write("conjunto de depositos")
	f.write(" ")  
	f.write("/") 
	for x in range(0,numdepositos):
		f.write(str(depositos[x].id))
		if(x!=numdepositos-1):
			f.write(",")
	f.write("/")
	f.write("\n")


	for x in range(0,numdepositos):
		f.write("ds"+str(x+1))                        #conjunto de depositos
		f.write(" ")
		f.write("particion de deposito "+str(x+1))
		f.write(" ")  
		f.write("/")
		to=min(floor((depositos[x].ventanafinal-depositos[x].ventanastart)/depositos[x].mintimelag)+1 , partdep(depositos[x],clientes))
		for y in range(0,to):                        #NO SE TE OLVIDE CAMBIAR ESTO...ES TO PERO PONE MUCHAS VARIABLES PARA LA PRUEBA GAMS....ARREGLADO
			depositos[x].particion.append("d"+str(x+1)+"s"+str(y+1))
			f.write("d"+str(x+1)+"s"+str(y+1))
			if(y!=(to-1)):
				f.write(",")
		f.write("/")
		f.write("\n")


	f.write("ds conjunto de particion de depositos / ")
	for x in range(0,numdepositos):
		f.write("set.ds"+str(x+1))
		if(x!=(numdepositos-1)):
			f.write(", ")
	f.write(" / \n")

	f.write("cs conjunto de particion de clientes / ")
	for x in range(0,numclientes):
		f.write("set.cs"+str(x+1))
		if(x!=(numclientes-1)):
			f.write(", ")
	f.write(" / \n")

	#f.write("os")                        #conjunto de outsorcing
	#f.write(" ")
	#f.write("conjunto de outsorcing")
	#f.write(" ")  
	#f.write("/") 
	#f.write("os1")
	#f.write("/")
	#f.write("\n")

	f.write("v")                        #verticces del grafo
	f.write(" ")
	f.write("conjunto de vertices de grafo")
	f.write(" ")  
	f.write("/")
	for x in range(0,numclientes):
		f.write("set.cs"+str(x+1)+", ")
	for x in range(0,numdepositos):
		f.write("set.ds"+str(x+1)+", ")
	f.write("set.o, set.f/ ")                #no se puso el outsorcing en el grafo
	f.write("\n")
	f.write("u(v) conjuto de clientes y depositos /")
	for x in range(0,numclientes):
		f.write("set.cs"+str(x+1)+", ")
	for x in range(0,numdepositos):
		if(x!=numdepositos-1):
			f.write("set.ds"+str(x+1)+", ")
		else:
			f.write("set.ds"+str(x+1))
	f.write("/\n")
	for a in range(0,numclientes):
		f.write("css"+str(a+1)+"(v) particion del cliente "+str(a+1)+ " en sub /set.cs"+str(a+1)+"/\n")	
	f.write("fss(v) subconjunto de finales /set.f/\n")
	f.write("dss(u) subconjunto de depositos / ")
	for x in range(0,numdepositos):
		f.write("set.ds"+str(x+1))
		if(x!=(numdepositos-1)):
			f.write(", ")
	f.write(" / \n")
	f.write("css(u) subconjunto de clientes / ")
	for x in range(0,numclientes):
		f.write("set.cs"+str(x+1))
		if(x!=(numclientes-1)):
			f.write(", ")
	f.write(" / \n")
	f.write("oss(v) subconjunto del grafo de origenes / ")
	for x in range(0,numorigenes):
		f.write("o"+str(x+1))
		if(x!=(numorigenes-1)):
			f.write(", ")
	f.write(" / \n")
	f.write("alias(v,av)")
	f.write("\n")
	f.write("alias(u,au);")
	f.write("\n \n")

	f.write("Parameters")
	f.write("\n")
	f.write("capacidadcamion(k) capacidad de cemento de camion k")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numcamiones):
		f.write(str(camiones2[x].id)+" "+ str(camiones2[x].capacidad))
		if(x!=(numcamiones-1)):
			f.write("\n")
	f.write(" /")


	f.write("\n")
	f.write("costocamion(k) costo de usar el camion k")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numcamiones):
		f.write(str(camiones2[x].id)+" "+ str(camiones2[x].costouso))
		if(x!=(numcamiones-1)):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("vik(k) ventana inicial de camion k")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numcamiones):
		f.write(str(camiones2[x].id)+" "+ str(int(camiones2[x].ventanastart)))
		if(x!=(numcamiones-1)):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("vfk(k) ventana final de camion k")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numcamiones):
		f.write(str(camiones2[x].id)+" "+ str(int(camiones2[x].ventanafinal)))
		if(x!=(numcamiones-1)):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("mtl(d) mintimelag del deposito d")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numdepositos):
		f.write(str(depositos[x].id)+" "+ str(depositos[x].mintimelag))
		if(x!=(numdepositos-1)):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("vid(dss) ventana inicial de los nodos de particion del deposito d")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numdepositos):
		for y in depositos[x].particion:
			f.write(str(y)+" "+ str(int(depositos[x].ventanastart)))
			if(y!=depositos[x].particion[-1]):
				f.write("\n")
		if(x!=numdepositos-1):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("vfd(dss) ventana final de los nodos de particion del deposito d")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numdepositos):
		for y in depositos[x].particion:
			f.write(str(y)+" "+ str(int(depositos[x].ventanafinal)))
			if(y!=depositos[x].particion[-1]):
				f.write("\n")
		if(x!=numdepositos-1):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("srt(v) tiempo de servicio del nodo v")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numdepositos):
		for y in depositos[x].particion:
			f.write(str(y)+" "+ str(int(depositos[x].servtime)))
			if(y!=depositos[x].particion[-1]):
				f.write("\n")
		f.write("\n")
	for x in range(0,numclientes):
		for y in clientes[x].particion:
			f.write(str(y)+" "+ str(int(clientes[x].servtime)))
			if(y!=clientes[x].particion[-1]):
				f.write("\n")
		if(x!=numclientes-1):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("dem(c) demanda del cliente c")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numclientes):
		f.write(str(clientes[x].id)+" "+ str(clientes[x].demanda))
		if(x!=(numclientes-1)):
			f.write("\n")
	f.write("/ ")

	f.write("\n")
	f.write("vic(css) ventana inicial de los nodos de particion del cliente c")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numclientes):
		for y in clientes[x].particion:
			f.write(str(y)+" "+ str(int(clientes[x].ventanastart)))
			if(y!=clientes[x].particion[-1]):
				f.write("\n")
		if(x!=numclientes-1):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("vfc(css) ventana final de los nodos de particion del cliente c")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numclientes):
		for y in clientes[x].particion:
			f.write(str(y)+" "+ str(int(clientes[x].ventanafinal)))
			if(y!=clientes[x].particion[-1]):
				f.write("\n")
		if(x!=numclientes-1):
			f.write("\n")
	f.write(" /")


	f.write("\n")
	f.write("pcc(c) costo de penalizacion por incumplimiento al cliente c")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numclientes):
		f.write(str(clientes[x].id)+" "+ str(int(clientes[x].penalcost)))
		if(x!=numclientes-1):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("tmin(css) tiempo minimo de los nodos de particion del cliente c")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numclientes):
		for y in clientes[x].particion:
			f.write(str(y)+" "+ str(int(clientes[x].tiempomin)))
			if(y!=clientes[x].particion[-1]):
				f.write("\n")
		if(x!=numclientes-1):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("tmax(css) tiempo maximo de los nodos de particion del cliente c")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numclientes):
		for y in clientes[x].particion:
			f.write(str(y)+" "+ str(int(clientes[x].tiempomax)))
			if(y!=clientes[x].particion[-1]):
				f.write("\n")
		if(x!=numclientes-1):
			f.write("\n")
	f.write(" /")

	f.write("\n")
	f.write("tpent(css) tiempo de primera entrega a mas tardar del cliente c")
	f.write("\n")
	f.write("/ ")
	for x in range(0,numclientes):
		for y in clientes[x].particion:
			if(y==clientes[x].particion[0]):
					f.write(str(y)+" "+ str(int(clientes[x].primeraentrega)))
			#if(y!=clientes[x].particion[-1]):
			#	f.write("\n")
		if(x!=numclientes-1):
			f.write("\n")
	f.write(" /")


	f.write("\n")
	f.write("outc(c) costo de que el outsourcer se encargue del cliente c")
	f.write("\n")
	f.write("/ ")
	count=0
	clcount=1
	primer=0
	segundo=0
	for a in linea:
		count=count+1
		if(a==" "):
			primer=int(segundo)
			segundo=int(count)
			f.write("c"+str(clcount)+" "+str(linea[primer:segundo])+"\n")
			clcount=clcount+1
		elif(a=="\n"):
			primer=int(segundo)
			segundo=int(count)
			f.write("c"+str(clcount)+" "+str(linea[primer:segundo]))
			clcount=clcount+1
	f.write("/")


	f.write("\n")
	f.write("mady(v,av,k) matriz de adyacencia")
	f.write("\n")
	f.write("/ ")
	for k in camiones2:
		for o in origenes:
			for d in depositos:
				for p in d.particion:
					if(k.origen==o):
						f.write(str(o)+"."+str(p)+"."+str(k)+" =1"+"\n")  #origenes fabricas
	for k in camiones2:
		for o in origenes:
			for s in finales:
				if(k.origen==o):
					if(k.final==s):
						f.write(str(o)+"."+str(s)+"."+str(k)+" =1"+"\n")  #origenes finales
	for k in camiones2:
		for d in depositos:
			for p in d.particion:
				for c in clientes:
					for z in c.particion:
						if(k in c.listcam):
							if(d.id in c.listdep):
								f.write(str(p)+"."+str(z)+"."+str(k)+" =1"+"\n")  #fabricas clientes
	for k in camiones2:
		for d in depositos:
			for p in d.particion:
				for c in clientes:
					for z in c.particion:
						if(k in c.listcam):
							f.write(str(z)+"."+str(p)+"."+str(k)+" =1"+"\n")  #clientes fabricas
	for k in camiones2:
		for s in finales:
			for c in clientes:
				for z in c.particion:
					if(k in c.listcam):
						if(k.final==s):
							f.write(str(z)+"."+str(s)+"."+str(k)+" =1"+"\n")  #clientes finales
	f.write(" /\n")



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
				macost["o"+str(o+1)]["o"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["o"+str(o+1)]["o"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numfinales):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["o"+str(o+1)]["f"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["o"+str(o+1)]["f"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numdepositos):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["o"+str(o+1)]["d"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["o"+str(o+1)]["d"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numclientes):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["o"+str(o+1)]["c"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["o"+str(o+1)]["c"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1

	del costolinea
	for z in range(0,numfinales):
		linea=file.readline()

	for z in range(0,numdepositos):
		linea=file.readline()
		#print(linea)
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
				macost["d"+str(z+1)]["o"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["d"+str(z+1)]["o"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numfinales):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["d"+str(z+1)]["f"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["d"+str(z+1)]["f"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numdepositos):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["d"+str(z+1)]["d"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["d"+str(z+1)]["d"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numclientes):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["d"+str(z+1)]["c"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["d"+str(z+1)]["c"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
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
				macost["c"+str(z+1)]["o"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["c"+str(z+1)]["o"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numfinales):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["c"+str(z+1)]["f"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["c"+str(z+1)]["f"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numdepositos):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["c"+str(z+1)]["d"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["c"+str(z+1)]["d"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numclientes):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["c"+str(z+1)]["c"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["c"+str(z+1)]["c"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1



	f.write("mcost(v,av,k) matriz de costos")
	f.write("\n")
	f.write("/ ")
	for x, a in macost.items():
		for y, b in a.items():
			for z, c in b.items():
	#[o][][]
				if(x[0]=="o"):
			#[o][d][k]
					if(y[0]=="d"):
						for w in depositos[int(y[1:])-1].particion:
							f.write(x+"."+str(w)+"."+str(z)+" ="+str(c)+"\n")
			#[o][f][k]
					elif(y[0]=="f"):
						f.write(x+"."+str(y)+"."+str(z)+" ="+str(c)+"\n")
	#[d][][]
				elif(x[0]=="d"):
			#[d][c][k]
					if(y[0]=="c"):
						for w in depositos[int(x[1:])-1].particion:
							for e in clientes[int(y[1:])-1].particion:
								f.write(str(w)+"."+str(e)+"."+str(z)+" ="+str(c)+"\n")
	#[c][][]
				elif(x[0]=="c"):
			#[d][c][k]
					if(y[0]=="d"):
						for w in clientes[int(x[1:])-1].particion:
							for e in depositos[int(y[1:])-1].particion:
								f.write(str(w)+"."+str(e)+"."+str(z)+" ="+str(c)+"\n")
					elif(y[0]=="f"):
						for w in clientes[int(x[1:])-1].particion:
							f.write(str(w)+"."+str(y)+"."+str(z)+" ="+str(c)+"\n")
	f.write("/ \n")

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
		macost["o"+str(o+1)]=dict()
		#print(linea[:-1])
		for x in range(0,numorigenes):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["o"+str(o+1)]["o"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["o"+str(o+1)]["o"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numfinales):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["o"+str(o+1)]["f"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["o"+str(o+1)]["f"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numdepositos):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["o"+str(o+1)]["d"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["o"+str(o+1)]["d"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numclientes):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["o"+str(o+1)]["c"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["o"+str(o+1)]["c"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
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
		#print(linea[:-1])
		for x in range(0,numorigenes):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["d"+str(z+1)]["o"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["d"+str(z+1)]["o"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numfinales):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["d"+str(z+1)]["f"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["d"+str(z+1)]["f"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numdepositos):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["d"+str(z+1)]["d"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["d"+str(z+1)]["d"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numclientes):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["d"+str(z+1)]["c"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["d"+str(z+1)]["c"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
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
				macost["c"+str(z+1)]["o"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["c"+str(z+1)]["o"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numfinales):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["c"+str(z+1)]["f"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["c"+str(z+1)]["f"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numdepositos):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["c"+str(z+1)]["d"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["c"+str(z+1)]["d"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1
		for x in range(0,numclientes):
			if(costolinea[lineacount]!="M" and costolinea[lineacount]!="M "):
				macost["c"+str(z+1)]["c"+str(x+1)]=dict()
				for k in range(0,numcamiones):
					macost["c"+str(z+1)]["c"+str(x+1)]["k"+str(k+1)]=int(costolinea[lineacount])
			lineacount=lineacount+1

	f.write("mtim(v,av,k) matriz de tiempos")
	f.write("\n")
	f.write("/ ")
	for x, a in macost.items():
		for y, b in a.items():
			for z, c in b.items():
	#[o][][]
				if(x[0]=="o"):
			#[o][d][k]
					if(y[0]=="d"):
						for w in depositos[int(y[1:])-1].particion:
							f.write(x+"."+str(w)+"."+str(z)+" ="+str(c)+"\n")
			#[o][f][k]
					elif(y[0]=="f"):
						f.write(x+"."+str(y)+"."+str(z)+" ="+str(c)+"\n")
	#[d][][]
				elif(x[0]=="d"):
			#[d][c][k]
					if(y[0]=="c"):
						for w in depositos[int(x[1:])-1].particion:
							for e in clientes[int(y[1:])-1].particion:
								f.write(str(w)+"."+str(e)+"."+str(z)+" ="+str(c)+"\n")
	#[c][][]
				elif(x[0]=="c"):
			#[d][c][k]
					if(y[0]=="d"):
						for w in clientes[int(x[1:])-1].particion:
							for e in depositos[int(y[1:])-1].particion:
								f.write(str(w)+"."+str(e)+"."+str(z)+" ="+str(c)+"\n")
					elif(y[0]=="f"):
						for w in clientes[int(x[1:])-1].particion:
							f.write(str(w)+"."+str(y)+"."+str(z)+" ="+str(c)+"\n")
	f.write("/; \n")

	#variables
	f.write("variables \n")
	f.write("\tz funcion objetivo \n")
	f.write("\tx(v,av,k) si el camion k va del nodo v al nodo av \n")
	f.write("\tw(v,k) tiempo de llegada al nodo v \n")
	f.write("\ty(c) si cumplio con la demanda del cliente c \n")
	f.write("\th(c) si el outsourcer se encarga del cliente c; \n")
	f.write("binary variables x, y, h; \n")
	f.write("positive variable w; \n")

	#ecuaciones
	f.write("Equations \n")
	f.write("\tcost define objetive function \n")
	f.write("\tvari(v,av,k) ecuacion de validacion de arista \n")
	f.write("\tvariw(u,k) ecuacion de validacion de variable w\n")
	for a in range(0,numcamiones):
		f.write("\tor"+str(a+1)+" ecuacion de salida de origen\n")
	for a in range(0,numcamiones):
		f.write("\tfi"+str(a+1)+" ecuacion de llegada a nodos finales\n")
	f.write("\tflow(u,k) ecuacion de conservacion de flujo\n ")
	f.write("\tvisit(u) ecuacion que solo permite ser visitado cada nodo de deposito y cliente 1 vez \n")
	for a in range(0,numclientes):
		nuevo=1
		for b in clientes[a].particion:
			if(b!=clientes[a].particion[-1]):
				f.write("\tsalto"+str(a+1)+str(nuevo)+" ecuacion que no permite saltos del cliente "+str(a+1)+" en la visita "+str(nuevo)+"\n")
			nuevo=nuevo+1
	for a in range(0,numclientes):
		f.write("\tdem"+str(a+1)+" ecuacion que verifica que si se decide cumplir una demanda se realice \n")
	f.write("\ttinic(u,k) ecuacion que garantiza la ventana inicial del camion k en el nodo u \n")
	f.write("\ttfin(u,k) ecuacion que garantiza la ventana final del camion k en el nodo u \n")
	f.write("\ttinicd(dss,k) ecuacion que garantiza el tiempo inicial de depositos \n")
	f.write("\ttfind(dss,k) ecuacion que garantiza el tiempo final de depositos \n")
	f.write("\ttinicc(css,k) ecuacion que garantiza la ventana de tiempo inicial de clientes \n")
	f.write("\ttfinc(css,k) ecuacion que garantiza la ventana de tiempo final de clientes \n")
	f.write("\tvalxw(v,av,k) conexion entre las variables x y w \n")
	for a in range(0,numclientes):
		for b in range(0,len(clientes[a].particion)-1):
			f.write("\tlagmin"+str(clientes[a].particion[b])+" ecuacion de lag min \n")
	for a in range(0,numclientes):
		for b in range(0,len(clientes[a].particion)-1):
			f.write("\tlagmax"+str(clientes[a].particion[b])+" ecuacion de lag max \n")
	for a in range(0,numdepositos):
		for b in range(0,len(depositos[a].particion)-1):
			f.write("\tlagmin"+str(depositos[a].particion[b])+" ecuacion de lag min \n")
	for a in range(0,numclientes):
		f.write("\tpren"+str(a+1)+" ecuacion que garantiza la primera entrega del cliente "+str(a+1)+" antes de la fecha limite \n")
	f.write(";")

	#def de ecuaciones
	f.write("cost.. z =e= sum((oss,dss,k), mady(oss,dss,k)*costocamion(k)*x(oss,dss,k)) + sum((v,av,k), mady(v,av,k)*mcost(v,av,k)*x(v,av,k)) + sum(c,(1-y(c))*pcc(c)) + sum(c,h(c)*outc(c)); \n")
	f.write("vari(v,av,k).. x(v,av,k)=e=x(v,av,k)*mady(v,av,k);\n")
	f.write("variw(u,k).. sum(v,x(v,u,k))*1500=g=w(u,k);\n")
	for a in range(0,numcamiones):
		f.write("or"+str(a+1)+".. sum(v,mady(\""+str(camiones2[a].origen)+"\",v,\"k"+str(a+1)+"\")*x(\""+str(camiones2[a].origen)+"\",v,\"k"+str(a+1)+"\"))=e=1;\n")
	for a in range(0,numcamiones):
		f.write("fi"+str(a+1)+".. sum(v,mady(v,\""+str(camiones2[a].final)+"\",\"k"+str(a+1)+"\")*x(v,\""+str(camiones2[a].final)+"\",\"k"+str(a+1)+"\"))=e=1;\n")
	f.write("flow(u,k).. sum(v,x(v,u,k))-sum(v,x(u,v,k))=e=0;\n")
	f.write("visit(u).. sum((v,k),x(u,v,k)*mady(u,v,k))=l=1;\n")
	for a in range(0,numclientes):
		f.write("dem"+str(a+1)+".. sum(css"+str(a+1)+",sum(k,sum(v,x(css"+str(a+1)+",v,k)*mady(css"+str(a+1)+",v,k)*capacidadcamion(k)))) + h(\"c"+str(a+1)+"\")*dem(\"c"+str(a+1)+"\")=g=dem(\"c"+str(a+1)+"\")*y(\"c"+str(a+1)+"\");\n")
	for a in range(0,numclientes):
		nuevo=1
		for b in clientes[a].particion:
			if(b!=clientes[a].particion[-1]):
				siguiente(b)
				f.write("salto"+str(a+1)+str(nuevo)+".. sum(v,sum(k,x(\""+str(siguiente(b))+"\",v,k)))-sum(v,sum(k,x(\""+str(b)+"\",v,k))) =l= 0;\n")
			nuevo=nuevo+1
	f.write("tinic(u,k).. w(u,k)=g=vik(k)*sum(v,x(v,u,k));\n")
	f.write("tfin(u,k).. w(u,k)=l=vfk(k)*sum(v,x(v,u,k));\n")
	f.write("tinicd(dss,k).. w(dss,k)=g=vid(dss)*sum(v,x(v,dss,k));\n")
	f.write("tfind(dss,k).. w(dss,k)=l=vfd(dss)*sum(v,x(v,dss,k));\n")
	f.write("tinicc(css,k).. w(css,k)=g=vic(css)*sum(v,x(v,css,k));\n")
	f.write("tfinc(css,k).. w(css,k)=l=vfc(css)*sum(v,x(v,css,k));\n")
	f.write("valxw(v,av,k).. 1000000*(x(v,av,k)-1)+srt(v)+mtim(v,av,k)=l=w(av,k)-w(v,k);\n")
	for a in range(0,numclientes):
		for b in range(0,len(clientes[a].particion)-1):
			nextt=siguiente(clientes[a].particion[b])
			f.write("lagmin"+str(clientes[a].particion[b])+".. sum(k,w(\""+str(nextt)+"\",k)-w(\""+str(clientes[a].particion[b])+"\",k))=g=tmin(\""+str(nextt)+"\")*sum(v,sum(k,x(v,\""+str(clientes[a].particion[b])+"\",k))); \n")
	for a in range(0,numclientes):
		for b in range(0,len(clientes[a].particion)-1):
			nextt=siguiente(clientes[a].particion[b])
			f.write("lagmax"+str(clientes[a].particion[b])+".. sum(k,w(\""+str(nextt)+"\",k)-w(\""+str(clientes[a].particion[b])+"\",k))=l=tmax(\""+str(nextt)+"\"); \n")
	for a in range(0,numdepositos):
		for b in range(0,len(depositos[a].particion)-1):
			nextt=siguiente(depositos[a].particion[b])
			f.write("lagmin"+str(depositos[a].particion[b])+".. sum(k,w(\""+str(nextt)+"\",k)-w(\""+str(depositos[a].particion[b])+"\",k))=g=mtl(\""+str(depositos[a].id)+"\")*sum(v,sum(k,x(v,\""+str(depositos[a].particion[b])+"\",k))); \n")
	for a in range(0,numclientes):
		f.write("pren"+str(a+1)+".. sum(k,w(\""+str(clientes[a].id)+"s1\",k))=l=tpent(\""+str(clientes[a].id)+"s1\");\n")
	f.write("Model cemento /all/ ; \n")
	f.write("Solve cemento using MIP minimizing z ; \n")






	file.close()
	f.close()





