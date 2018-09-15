import serial
import datetime
import time
import threading
import math
import os
from db import*
from relatorio import*
import numpy as np
import cv2
import sys
import string
from data_input_stream import DataInputStream


def lerArduino():
	global x
	x = ""
	comunicacaoSerial = serial.Serial('/dev/ttyACM0', 9600)
	while 1 :
	  x = comunicacaoSerial.read().decode("utf-8")


#Pasta de video
raiz = os.getcwd()
videos = raiz+"/videos"
imagens = raiz+"/imagens"

if os.path.exists(videos):
	#Checo tudo do dire
	pass

else:
	#Crio o dire
	os.mkdir("videos")

#variaveis iniciais
global modo, dataHora


#ID do terminal vem do txt
cu = 0
while True:
    id ="ID"+str(cu)+".dat"
    try:
        with open(id, 'rb') as f:
            dis = DataInputStream(f)
            #val = dis.read_int()
            string = dis.read_utf()
            break
    except:
        pass
    
    cu+=1
idTerm = string.decode("utf-8")
print(idTerm)
kon = Conexao()
#Modo de atuacao
modo = int(kon.modo(int(idTerm)))
#ID do Estacionamento vem do banco
idUnd = int(kon.idUnd())

#Tempo de gravacao
tempo_gravacao = float(kon.tempo_gravacao(int(idTerm)))


#Uma thread para o arduino

lerArd = threading.Thread(target=lerArduino)
lerArd.start()
#x = "1"
#Insiro um registro para ter o nControle
objeto = Info(None, None, None,None,None, None, None)
iD = kon.cadastra(objeto)


#Looping de gravacao
k = False
os.chdir(videos)
nControle = 0
while True:
	#Tempo de gravacao
	tempo_gravacao = float(kon.tempo_gravacao(int(idTerm)))

	if modo == 1:

		#Carro entrando
		if x == '1':
			x = ""
			
			dat = datetime.datetime.now()

			date = str(dat.year) + str(dat.month).zfill(2) + str(dat.day).zfill(2)

			hora = str(dat.hour).zfill(2) + str(dat.minute).zfill(2) + str(dat.second).zfill(2)

			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			
			#Banco de dados
			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			if iD is not None:
				tupla = (iD, horaTela)
				print("Entrada Carro #Controle:%s %s" %tupla)
				nControle =  iD
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(iD,1, dat,"Carro",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)
				iD = None
			else:
				nControle+=1
				tupla = (nControle, horaTela)
				print("Entrada Carro #Controle:%s %s" %tupla)
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(None,1, dat,"Carro",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)

			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			

			#leitura da camera
			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Inicio Video #Controle:%s %s" %tupla)
			cap = cv2.VideoCapture()
			cap.open("rtsp://admin:@192.168.10.1")

			frame_width = int(cap.get(3))
			frame_height = int(cap.get(4))
 
			# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
			out = cv2.VideoWriter(str(nControle)+"_"+da+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))

			inicio = time.time()
			resultado = 0

			os.chdir(videos)

			while(cap.isOpened()):
			    ret, frame = cap.read()
			    if ret:
			        x = ""
			        out.write(frame)

			        fim = time.time()
			        resultado = fim - inicio

			        if(resultado >= tempo_gravacao):
			        	break

			    else:
			        break

			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Fim de Video #Controle:%s %s" %tupla)
			print("Proc Finalizado - aguardando veiculo #Controle:%s %s" %tupla)

			# Release everything if job is finished
			cap.release()
			out.release()

		#Carro Saindo
		if x == '2':
			

			dat = datetime.datetime.now()

			date = str(dat.year) + str(dat.month).zfill(2) + str(dat.day).zfill(2)

			hora = str(dat.hour).zfill(2) + str(dat.minute).zfill(2) + str(dat.second).zfill(2)

			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			
			#Banco de dados
			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			if iD is not None:
				tupla = (iD, horaTela)
				print("Saida Carro #Controle:%s %s" %tupla)
				nControle =  iD
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(iD,2, dat,"Carro",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)
				iD = None
			else:
				nControle+=1
				tupla = (nControle, horaTela)
				print("Saida Carro #Controle:%s %s" %tupla)
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(None,2, dat,"Carro",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)

			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			

			#leitura da camera
			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Inicio Video #Controle:%s %s" %tupla)
			cap = cv2.VideoCapture()
			cap.open("rtsp://admin:@192.168.10.1")

			frame_width = int(cap.get(3))
			frame_height = int(cap.get(4))
 
			# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
			out = cv2.VideoWriter(str(nControle)+"_"+da+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))

			inicio = time.time()
			resultado = 0

			os.chdir(videos)

			while(cap.isOpened()):
			    ret, frame = cap.read()
			    if ret:
			        x = ""
			        out.write(frame)

			        fim = time.time()
			        resultado = fim - inicio

			        if(resultado >= tempo_gravacao):
			        	break

			    else:
			        break

			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Fim de Video #Controle:%s %s" %tupla)
			print("Proc Finalizado - aguardando veiculo #Controle:%s %s" %tupla)

			# Release everything if job is finished
			cap.release()
			out.release()

		#Carro Erro
		if x == '3':
			

			dat = datetime.datetime.now()

			date = str(dat.year) + str(dat.month).zfill(2) + str(dat.day).zfill(2)

			hora = str(dat.hour).zfill(2) + str(dat.minute).zfill(2) + str(dat.second).zfill(2)

			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			
			#Banco de dados
			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			if iD is not None:
				tupla = (iD, horaTela)
				print("Erro Carro #Controle:%s %s" %tupla)
				nControle =  iD
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(iD,3, dat,"Carro",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)
				iD = None
			else:
				nControle+=1
				tupla = (nControle, horaTela)
				print("Erro Carro #Controle:%s %s" %tupla)
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(None,3, dat,"Carro",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)

			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			

			#leitura da camera
			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Inicio Video #Controle:%s %s" %tupla)
			cap = cv2.VideoCapture()
			cap.open("rtsp://admin:@192.168.10.1")

			frame_width = int(cap.get(3))
			frame_height = int(cap.get(4))
 
			# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
			out = cv2.VideoWriter(str(nControle)+"_"+da+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))

			inicio = time.time()
			resultado = 0

			os.chdir(videos)

			while(cap.isOpened()):
			    ret, frame = cap.read()
			    if ret:
			        x = ""
			        out.write(frame)

			        fim = time.time()
			        resultado = fim - inicio

			        if(resultado >= tempo_gravacao):
			        	break

			    else:
			        break

			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Fim de Video #Controle:%s %s" %tupla)
			print("Proc Finalizado - aguardando veiculo #Controle:%s %s" %tupla)

			# Release everything if job is finished
			cap.release()
			out.release()

		#Moto Entrando
		if x == '5':
			
			dat = datetime.datetime.now()

			date = str(dat.year) + str(dat.month).zfill(2) + str(dat.day).zfill(2)

			hora = str(dat.hour).zfill(2) + str(dat.minute).zfill(2) + str(dat.second).zfill(2)

			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			
			#Banco de dados
			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			if iD is not None:
				tupla = (iD, horaTela)
				print("Entrada Moto #Controle:%s %s" %tupla)
				nControle =  iD
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(iD,1, dat,"Moto",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)
				iD = None
			else:
				nControle+=1
				tupla = (nControle, horaTela)
				print("Entrada Moto #Controle:%s %s" %tupla)
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(None,1, dat,"Moto",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)

			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			

			#leitura da camera
			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Inicio Video #Controle:%s %s" %tupla)
			cap = cv2.VideoCapture()
			cap.open("rtsp://admin:@192.168.10.1")

			frame_width = int(cap.get(3))
			frame_height = int(cap.get(4))
 
			# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
			out = cv2.VideoWriter(str(nControle)+"_"+da+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))

			inicio = time.time()
			resultado = 0

			os.chdir(videos)

			while(cap.isOpened()):
			    ret, frame = cap.read()
			    if ret:
			        x = ""
			        out.write(frame)

			        fim = time.time()
			        resultado = fim - inicio

			        if(resultado >= tempo_gravacao):
			        	break

			    else:
			        break

			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Fim de Video #Controle:%s %s" %tupla)
			print("Proc Finalizado - aguardando veiculo #Controle:%s %s" %tupla)

			# Release everything if job is finished
			cap.release()
			out.release()


		#Moto Saindo
		if x == '6':

			dat = datetime.datetime.now()

			date = str(dat.year) + str(dat.month).zfill(2) + str(dat.day).zfill(2)

			hora = str(dat.hour).zfill(2) + str(dat.minute).zfill(2) + str(dat.second).zfill(2)

			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			
			#Banco de dados
			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			if iD is not None:
				tupla = (iD, horaTela)
				print("Saida Moto #Controle:%s %s" %tupla)
				nControle =  iD
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(iD,2, dat,"Moto",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)
				iD = None
			else:
				nControle+=1
				tupla = (nControle, horaTela)
				print("Saida Moto #Controle:%s %s" %tupla)
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(None,2, dat,"Moto",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)

			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			

			#leitura da camera
			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Inicio Video #Controle:%s %s" %tupla)
			cap = cv2.VideoCapture()
			cap.open("rtsp://admin:@192.168.10.1")

			frame_width = int(cap.get(3))
			frame_height = int(cap.get(4))
 
			# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
			out = cv2.VideoWriter(str(nControle)+"_"+da+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))

			inicio = time.time()
			resultado = 0

			os.chdir(videos)

			while(cap.isOpened()):
			    ret, frame = cap.read()
			    if ret:
			        x = ""
			        out.write(frame)

			        fim = time.time()
			        resultado = fim - inicio

			        if(resultado >= tempo_gravacao):
			        	break

			    else:
			        break

			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Fim de Video #Controle:%s %s" %tupla)
			print("Proc Finalizado - aguardando veiculo #Controle:%s %s" %tupla)

			# Release everything if job is finished
			cap.release()
			out.release()

		#Moto Erro
		if x == '4':
			
			dat = datetime.datetime.now()

			date = str(dat.year) + str(dat.month).zfill(2) + str(dat.day).zfill(2)

			hora = str(dat.hour).zfill(2) + str(dat.minute).zfill(2) + str(dat.second).zfill(2)

			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			
			#Banco de dados
			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			if iD is not None:
				tupla = (iD, horaTela)
				print("Erro Moto #Controle:%s %s" %tupla)
				nControle =  iD
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(iD,3, dat,"Moto",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)
				iD = None
			else:
				nControle+=1
				tupla = (nControle, horaTela)
				print("Erro Moto #Controle:%s %s" %tupla)
				print("Grava no Banco #Controle:%s %s" %tupla)
				objeto = Info(None,3, dat,"Moto",str(nControle)+"_"+da+'.avi', idTerm, idUnd)
				kon.cadastra(objeto)

			da = str(dat)
			da = da.replace(":", "-")
			da = da.replace(".", "-")
			

			#leitura da camera
			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Inicio Video #Controle:%s %s" %tupla)
			cap = cv2.VideoCapture()
			cap.open("rtsp://admin:@192.168.10.1")

			frame_width = int(cap.get(3))
			frame_height = int(cap.get(4))
 
			# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
			out = cv2.VideoWriter(str(nControle)+"_"+da+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))

			inicio = time.time()
			resultado = 0

			os.chdir(videos)

			while(cap.isOpened()):
			    ret, frame = cap.read()
			    if ret:
			        x = ""
			        out.write(frame)

			        fim = time.time()
			        resultado = fim - inicio

			        if(resultado >= tempo_gravacao):
			        	break

			    else:
			        break

			dat = datetime.datetime.now()
			horaTela = str(dat.hour).zfill(2)+":"+str(dat.minute).zfill(2)+":"+ str(dat.second).zfill(2)

			tupla = (nControle, horaTela)
			print("Fim de Video #Controle:%s %s" %tupla)
			print("Proc Finalizado - aguardando veiculo #Controle:%s %s" %tupla)

			# Release everything if job is finished
			cap.release()
			out.release()

	#caso for mangueira
	elif modo == 2:
		pass




