#generadora de instancia
from random import randint
from random import random
from random import choice
from math import ceil
from math import floor
from math import sqrt
from scipy.stats import norm
import scipy.stats as stats

def distancia(coor1,coor2):
	potencia1=(coor2[1]-coor1[1])**2
	potencia2=(coor2[0]-coor1[0])**2
	return sqrt(potencia1+potencia2)

def costo(distan):
	return round(distan/2000)*10

def tiempo(distan):
	if(type(distan)==int):
		time=distan/1000/40*60        #inst 40km/hr
		minim=round(time*(-1)/10)	#cotas minimas de la normaas
		maxim=round(time/10)		#cotas maximas de la normal
		a=min(max(norm.rvs(loc=0,scale=(time/10),size=1)[0],minim),maxim)  #valor normal añadido al tiempo constante
		time=int(time+float(a))
	elif(distan==0):
		return 0
	else:
		time="M"
		return time
	#print(time)
	return time


numreplica=1
for replica in range(0,numreplica):
	capacitycam=[]
	coordnodos=dict()
	contador=0
	distancias=dict()

	tiposdecamion=2
	startday=420                   #comienzo del dia (en minutos)
	enday=1080					   #final del dia (en minutos)
	horasdeposito=10			   #horas de trabajo deposito
	horascamion=8				   #horas de trabajo camion
	numcamiones=25	 		       #numero de camiones
	numclientes=100	   			   #numero de clientes
	numdepositos=15	   			   #numero de depositos
	numorigenes=2  				   #numero de origenes
	numfinales=2		   		   #numero de finales
	capoutsourcing=7               #capacidad de camiones de outs
	costoutsourcing=350            #costo base de outsourcing 
	penalizacion=100               #coeficiente de penalizacion
	longcoord=30000				   #longitud de mapa para coordenadas cada unidad es 1mts             
	lambdad=floor(2*longcoord/5)   #distancia a partir de cual se cobra el aditivo
	costolambdad=10				   #costo de uso de aditivo
	kmin=  7 
	origenesset=set()
	finalesset=set()

	for x in range(0,tiposdecamion):
		capacitycam.append(7+x)   #capacidades de camiones
	cc=capacitycam.copy()

	kc=[]
	dc=[]
	for x in range(0,numcamiones):
		kc.append("k"+str(x+1))
	for x in range(0,numdepositos):
		dc.append("d"+str(x+1))

	f=open("instancia "+str(numcamiones)+"_"+str(numclientes)+"_"+str(numdepositos)+"_"+str(replica)+".txt","w");
	f.write(str(startday)+"\n")				#comienzo del dia
	f.write(str(enday)+"\n")				#final del dia
	f.write(str(horasdeposito)+"\n")		#horas que trabajan los depositos
	f.write(str(horascamion)+"\n")			#horas que trabajan los camiones
	f.write(str(numcamiones)+"\n") #numero de camiones
	f.write(str(numclientes)+"\n") #numero de clientes
	f.write(str(numdepositos)+"\n") #numeo de depositos
	f.write(str(numorigenes)+"\n") #numero de origenes
	f.write(str(numfinales)+"\n") #numero de finales
	coords=[round(randint(0,longcoord)/10)*10,round(randint(0,longcoord)/10)*10]  #coordenadas de outsourcer

	f.write("s "+str(coords[0]*10)+" "+str(coords[1]*10)+"\n") 
	for x in range(0,numorigenes):
		coordnodos["o"+str(x+1)]=[round(randint(0,longcoord)/10)*10,round(randint(0,longcoord)/10)*10]
		f.write("o"+str(x+1)+" "+str(coordnodos["o"+str(x+1)][0]*10)+" "+str(coordnodos["o"+str(x+1)][1]*10)) #coordenadas de origenes
		f.write("\n") 
		origenesset.add(x+1)
	for x in range(0,numfinales):
		coordnodos["f"+str(x+1)]=[round(randint(0,longcoord)/10)*10,round(randint(0,longcoord)/10)*10]
		f.write("f"+str(x+1)+" "+str(coordnodos["f"+str(x+1)][0]*10)+" "+str(coordnodos["f"+str(x+1)][1]*10))  #coordenadas de finales
		f.write("\n")
		finalesset.add(x+1)
	for x in range(0,numcamiones):
		if(contador>=tiposdecamion):
			f.write("k"+str(x+1)+" "+str(cc.pop())+"\n")                                             #capacidad del camion
		else:
			f.write("k"+str(x+1)+" "+str(capacitycam[randint(0,len(capacitycam)-1)])+"\n")
		f.write("k"+str(x+1)+" "+str(randint(10,20))+"\n")  										 #costo de usar el camion
		if(len(origenesset)>0 and len(finalesset)>0):        										 #origenes y finales de los camiones                               
			f.write("k"+str(x+1)+" "+str(origenesset.pop())+"\n")						
			f.write("k"+str(x+1)+" "+str(finalesset.pop())+"\n")
		elif(len(origenesset)>0):
			f.write("k"+str(x+1)+" "+str(origenesset.pop())+"\n")
			f.write("k"+str(x+1)+" "+str(randint(1,numfinales))+"\n")
		elif(len(finalesset)>0):
			f.write("k"+str(x+1)+" "+str(randint(1,numorigenes))+"\n")
			f.write("k"+str(x+1)+" "+str(finalesset.pop())+"\n")
		else:
			f.write("k"+str(x+1)+" "+str(randint(1,numorigenes))+"\n")									
			f.write("k"+str(x+1)+" "+str(randint(1,numfinales))+"\n")									


		valoresca=stats.gamma.rvs(1.5,size=1)                         #gamma significa que los camiones tienen una alta probabilidad de empezar su dia al inicio
		valoresca[0]=valoresca[0]*2
		valorvca=floor(valoresca[0])/2
		if((valorvca+startday/60)<=((enday/60)-horascamion)):
			f.write("k"+str(x+1)+" " +str(int(startday+(60*valorvca))) +" ")     #inicio y fin de dia de trabajo de los camiones
			f.write(str(int(startday+(60*valorvca)+(horascamion*60)))+"\n")
		else:
			f.write("k"+ str(x+1)+" "+str(int(enday-horascamion*60))+" ") 
			f.write(str(enday)+"\n")	

	for x in range(0,numdepositos):
		servtime=randint(5,10)*3                                         #tiempo de servicio de depositos
		coordnodos["d"+str(x+1)]=[round(randint(0,longcoord)/10)*10,round(randint(0,longcoord)/10)*10]
		f.write("d"+str(x+1)+" "+str(servtime)+"\n")               
		f.write("d"+str(x+1)+" "+str(randint(5,9)*2)+"\n")              #parametro, mintimelag del deposito
		f.write("d"+str(x+1)+" "+str((coordnodos["d"+str(x+1)][0]*10))+" "+str(coordnodos["d"+str(x+1)][1]*10)+"\n")  #coordenadas
		valores=stats.gamma.rvs(2,size=1)
		valorv=floor(valores[0]*2)/2
		if((valorv+startday/60)<=((enday/60)-horasdeposito) and x!=0 and x!=numdepositos-1):
			f.write("d"+str(x+1)+" "+str(int(startday+(60*valorv)))+" "+str(int(startday+(60*valorv)+horasdeposito*60))+"\n")  #ventanas de tiempo
		elif(x==0):
			f.write("d"+str(x+1)+" "+str(enday-horasdeposito*60)+" "+str(enday)+"\n")
		else:
			f.write("d"+str(x+1)+" "+str(startday)+" "+str(startday+horasdeposito*60)+"\n")
			

	demandalist=[]
	verc=kc.copy()
	verd=dc.copy()
	for x in range(0,numclientes):
		a=kc.copy()
		ab=dc.copy()
		demanda=randint(7,15)                                			 #demanda de los clientes
		demandalist.append(demanda)                                       
		minimo=randint(12,18)*2                                           #parametro, tiempo minimo entre cam       
		coordnodos["c"+str(x+1)]=[round(randint(0,longcoord)/10)*10,round(randint(0,longcoord)/10)*10]
		f.write("c"+str(x+1)+" "+ str(demanda)+"\n") 			 #demanda del cliente
		f.write("c"+str(x+1)+" "+str(randint(10,15))+"\n")                 #parametro, tiempo de servicio
		f.write("c"+str(x+1)+" "+str(demanda*penalizacion)+"\n")  		   #parametro, costopenalizacion por incumplimiento
		f.write("c"+str(x+1)+" "+str(minimo)+"\n")                         #parametro,tiempo minimo entre camiones
		f.write("c"+str(x+1)+" "+str(round(minimo+min(60,minimo*2)))+"\n") #parametro, tiempo maximo entre camiones
		f.write("c"+str(x+1)+" "+str(coordnodos["c"+str(x+1)][0]*10)+" "+str(coordnodos["c"+str(x+1)][1]*10)+"\n")  #coordenadas del cliente 
		f.write("c" +str(x+1)+" ")
		randomize=randint(ceil(numcamiones/2),numcamiones)              
		for y in range(0,randomize):                            #camiones que pueden distribuir al cliente
			randindice=randint(0,len(a)-1)
			rand=a.pop(randindice)
			if(rand in verc):
				verc.remove(rand)
			if(y!=randomize-1):
				f.write(str(rand)+" ")
			else:
				f.write(str(rand))
		longverc=len(verc)
		if(x==(numclientes-1) and longverc>0 and x!=0):                     #aseguro que cada camion tenga un cliente minimo                                  		   
			f.write(" ")
			for h in range(0,longverc):
				if(h!=longverc-1):   
					f.write(str(verc.pop())+" ")
				else:
					f.write(str(verc.pop()))
		f.write("\n")
		f.write("c"+str(x+1)+ " ")
		randomize=randint(ceil(numdepositos/2),numdepositos)
		for y in range(0,randomize):                                #depositos que pueden distribuir al cliente
			randindice=randint(0,len(ab)-1)
			rand=ab.pop(randindice)
			if(rand in verd):
				verd.remove(rand)
			if(y!=randomize-1):
				f.write(str(rand)+" ")
			else:
				f.write(str(rand))
		longverd=len(verd)
		if(x==(numclientes-1) and longverd>0 and x!=0):                     #aseguro que cada deposito tenga un cliente minimo                                  		   
			f.write(" ")
			for h in range(0,longverd):
				if(h!=longverd-1):   
					f.write(str(verd.pop())+" ")
				else:
					f.write(str(verd.pop()))



		ancho=max(ceil(round((random()*10)+demanda))*10,int(ceil(demanda/kmin))*60+int(minimo)*kmin/10*10,90)
		f.write("\n")
		valores=stats.gamma.rvs(2,size=1)
		valorv=round((valores[0]+random()/1.5)*2)
		valorv=valorv/2
		if(valorv==0):
			f.write("c"+str(x+1)+" "+str(int(vstart))+" "+str(int(startday+30+(60*valorv)+ancho))+"\n")
		elif((valorv+startday/60)<=((enday/60)-ancho/60)):
			vstart=startday+(60*valorv)
			f.write("c"+str(x+1)+" "+str(int(vstart))+" "+str(int(startday+(60*valorv)+ancho))+"\n")  #ventana de tiempo
		else:
			vstart=enday-ancho
			f.write("c"+str(x+1)+" "+str(int(vstart))+" "+str(int(enday))+"\n")
		f.write("c"+str(x+1)+" "+str(int(vstart+round(ancho/30)*10))+"\n")                     #parametro, lo mas que puede tardar la primer entrega
		

	#costos de outsourcing
	for a in range(0,numclientes):
		dist=int(distancia(coords,coordnodos["c"+str(a+1)]))
		f.write(str((2*costo(dist)+costoutsourcing)*ceil(demandalist[a]/capoutsourcing)))
		if(a<numclientes-1):
			f.write(" ")
		else:
			f.write("\n")
		
	#matriz de costo                            #origenes, finales, depositos, clientes
	for a,x in coordnodos.items():
		distancias[a]=dict()
		#if(a=="s"):                              #ousourcing (trabajo a futuro)
		#	for b,y in coordnodos.items():
		#		if(b[0]=="c"):
		#			distancias[a][b]=int(distancia(x,y))
		#			f.write(str(costo(distancias[a][b]))+" ")
		#		elif(b[0]=="s"):
		#			distancias[a][b]=0
		#			f.write("0 ")
		#		else:
		#			distancias[a][b]="M"
		#			f.write("M ")
		#	f.write("\n")
		if(a[0]=="o"):						     #origenes
			for b,y in coordnodos.items():
				if(b[0]=="d"):
					distancias[a][b]=int(distancia(x,y))
					f.write(str(costo(distancias[a][b]))+" ")
				elif(a==b or b[0]=="f"):
					distancias[a][b]=0
					f.write("0 ")
				else:
					distancias[a][b]="M"
					f.write("M ")
			f.write("\n")
		elif(a[0]=="d"):						     #depositos
			for b,y in coordnodos.items():
				if(b[0]=="d" or b[0]=="c"):
					distancias[a][b]=int(distancia(x,y))
					if(distancias[a][b]<=lambdad or b[0]!="c"):
						f.write(str(costo(distancias[a][b]))+" ")
					else:
						f.write(str(costo(distancias[a][b])+costolambdad+ceil((distancias[a][b]-lambdad)/4000)*10)+" ")
				elif(a==b):
					distancias[a][b]=0
					f.write("0 ")
				else:
					distancias[a][b]="M"
					f.write("M ")
			f.write("\n")
		elif(a[0]=="c"):						     #clientes
			for b,y in coordnodos.items():
				if(b[0]=="d" or b[0]=="f"):
					distancias[a][b]=int(distancia(x,y))
					f.write(str(costo(distancias[a][b]))+" ")
				elif(a==b):
					distancias[a][b]=0
					f.write("0 ")
				else:
					distancias[a][b]="M"
					f.write("M ")
			f.write("\n")
		elif(a[0]=="f"):										#finales
			for b,y in coordnodos.items():
				distancias[a][b]="M"
				f.write("M ")
			f.write("\n")



	for a,x in coordnodos.items():
		for b,y in coordnodos.items():
			if(a==b):
				f.write("0 ")
			else:
				f.write(str(tiempo(distancias[a][b]))+" ")
		f.write("\n")

	f.close()







