#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-850 -*-

#Titulo				:serialKepcov3_5.py
#Descripción		:Biblioteca para el control de las funciones de las fuentes marca Kepco del SESLab.
#Autor          	:Javier Campos Rojas
#Fecha            	:enero-2017
#Versión         	:3.5
#Notas          	:
#==============================================================================

import serial
import numpy as np
import time

class Source:
	def __init__(self, name, port):				#Inicia la biblioteca Source, los parametros del puerto cargan una fuente a la vez
		k=serial.Serial()						#Crea el puerto
		k.baudrate=9600;						#define velocidad
		k.bytesize=serial.EIGHTBITS;			#Define tamaño de palabra
		k.parity=serial.PARITY_NONE;			#Define paridad
		k.stopbits=serial.STOPBITS_ONE;			#Define bit de parada
		k.timeout=0.5;							#tiempo de desconexión
		k.xonxoff=True;							#XONXOFF encendido
		k.rtscts=False;							#RTSCTS apagado
		k.write_timeout=0.5;					#tiempo de escritura
		k.dsrdtr=False;							#DSRDTR apagado
		k.inter_byte_timeout=None;				
		k.port=port;							#Puerto donde esta la fuente coenctada
		self.port=port;							#Permite a las demas funciones accesar al valor de puerto
		self.k=k;								#Permite a las demas funciones accesar al puerto abierto
		self.name=name;							#Permite a las demas funciones accesar al nombre de la fuente
		#k.open();
		
	def connectport(self):						#Función para conectarse al puerto
		try: 									
			self.k.open()						#Abre el puerto
			return "Conectado en puerto: " + self.k.port		#Si se conecta, muestra el puerto al cual se conecto
		except Exception, e:					#En caso que no lo abra muestra error de conexión
			return ("Error: " + "\n" +  str(e)[0:len(str(e))/2] + "\n" + str(e)[len(str(e))/2:len(str(e))]) 
			#exit()
		
		if self.k.isOpen():						#Si el puerto esta abierto
			try:									
				self.k.write('*idn?\n')			#escribe comando SCPI 
			except Exception, e1:				#Si no lo abre, muestra error de conexión
				return ("error de comunicacion: " + "\n" +  str(e)[0:len(str(e1))/2] + "\n" + str(e1)[len(str(e1))/2:len(str(e1))])
		
		else:
			return ("No se pudo abrir puerto serial")	#Si no esta abierto, muestra mensaje

	def WriteTrian(self,voltList,f,n,t2,C): 	#Función para crear una señal Triangular#Recibe: tensiones, periodo de muestreo, frecuencia onda
		self.voltList=voltList;					
		self.f=f
		self.n=n
		self.t2=t2
		self.timeStep=len(self.t)
		self.k.write('*RST\n');					#Comando para reiniciar fuente e iniciar modo remoto
		self.k.write('LIST:CLE\n');				#limpiar listas de tensión ingresadas en memoria
		self.k.write('LIST:VOLT ');				#Enviar lista de valores de tensión
		step=10;								#Se escribira la lista en 10 sublistas
		m=len(self.voltList)//step				#Calculos internos 
		m=m*step								#para creación de listas
		voltList1=self.voltList[0:m]			#Se crean las listas
		voltList2=self.voltList[m:len(self.voltList)]
		for j in range(0,step):					
			self.k.write('LIST:VOLT ');			#Se escribe listas de tensiones y se separan en sublistas
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);	#
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:VOLT ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(self.t2));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		self.k.write('LIST:VOLT?\n');
		self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('VOLT:MODE LIST\n');

	def WriteVoltSine(self, voltList,f,n,t2,C):
		self.voltList=voltList;
		self.f=f
		self.n=n
		self.t2=t2
		self.C=C
		self.k.write('*RST\n');
		self.k.write('LIST:CLE\n');
		step=10;
		m=len(self.voltList)//step
		m=m*step
		voltList1=self.voltList[0:m]
		voltList2=self.voltList[m:len(self.voltList)]
		for j in range(0,step):
			self.k.write('LIST:VOLT ');
			for i in range(j*len(voltList1)/step,(j+1)*len(voltList1)/step):
				self.volt_out=str(voltList1[i]);
				if i < ((j+1)*(len(voltList1)-1)/step):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:VOLT ');
		for i in range(0,len(voltList2)):
				self.volt_out=str(voltList2[i]);
				if i < len(voltList2):
					self.k.write(self.volt_out);
					self.k.write(',');
				else:
					self.k.write(self.volt_out);
					self.k.write('\n');
		self.k.write('LIST:VOLT:POIN \n');
		self.k.write('LIST:DWEL ');
		self.k.write(str(self.t2));
		self.k.write('\n');
		self.k.write('LIST:COUN ');
		self.k.write(str(self.n));
		self.k.write('\n');
		self.k.write('LIST:VOLT?\n');
		self.k.readline();
		self.k.write('OUTP ON\n');
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('VOLT:MODE LIST\n');

	def WriteVolt(self,voltValue,C):
		self.voltValue=voltValue;
		self.C=C
		self.k.write('*RST\n');
		self.k.write('OUTP ON\n');
		self.k.write('VOLT ');
		self.k.write(str(self.voltValue));
		self.k.write('\n');
		self.k.write('CURR ');
		self.k.write(str(self.C));
		self.k.write('\n');
		self.k.write('MEAS:VOLT?');
		self.k.write('\n');

	def identify(self):
		self.k.write('*idn?\n');
		name = self.k.readline()
		return name;
	
	def stop(self):
		self.k.write('*RST\n');
		self.k.write('LIST:CLE\n');
		
	def measV(self):
		self.k.write('MEAS:VOLT?\n')
		
	def readM(self):
		volt = self.k.readline()
		return volt;
		
	def measC(self):
		self.k.write('MEAS:CURR?\n')
		curr = self.k.readline()
		return curr;
		
	def calPlusFine(self,val):
		self.k.write('CAL:DATA ');
		self.k.write(str(val));
		self.k.write('\n');
		
	def calMinusFine(self,val):
		self.k.write('CAL:DATA ');
		self.k.write('-');
		self.k.write(str(val));
		self.k.write('\n');
	
	def calPlusCoarse(self,val):
		self.k.write('CAL:DPOT ');
		self.k.write(str(val));
		self.k.write('\n');
	
	def calMinusCoarse(self,val):
		self.k.write('CAL:DPOT ');
		self.k.write('-');
		self.k.write(str(val));
		self.k.write('\n');
	
	def calStart(self,password):
		self.k.write('*RST\n');
		self.k.write('SYST:PASS:CEN ');
		self.k.write(str(password));	
		self.k.write('\n');
		self.k.write('CAL:STAT 1\n');
		
	def calZero(self):
		self.k.write('CAL:VOLT ZERO\n');
		
	def calMax(self):
		self.k.write('CAL:VOLT MAX\n');
		
	def calMin(self):
		self.k.write('CAL:VOLT MIN\n');
		
	def calVPRmax(self):
		self.k.write('CAL:VPR MAX\n');
		
	def calVPRmin(self):
		self.k.write('CAL:VPR MIN\n');
		
	def calSave(self):
		self.k.write('CAL:DATA SAVE\n');
		self.k.write('CAL:STAT 0\n');
		self.k.write('CAL:STAT?\n');
		status = self.k.readline()
		return status;

	def connect(self):
		try: 
			self.k.open()
			return "Conectado"
		except Exception, e:
			return "error al abrir puerto serial: " + str(e)
			exit()
			
		if self.k.isOpen():
			try:
				flushInput()
				self.k.flushOutput()
				self.k.write('*idn?\n')
				time.sleep(0.1)
				n=0;
				while True:
					respuesta = self.k.readline()
					return("Fuente: "+respuesta)

				self.k.close()
			except Exception, e1:
				return "error de comunicacion: " + str(e1)
		
		else:
			return "No se pudo abrir puerto serial"
