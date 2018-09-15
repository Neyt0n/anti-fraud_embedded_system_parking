import datetime
import time
import os
from db import*
from relatorio import*
import numpy as np
import cv2
import sys
import string
from openalpr import Alpr
from pathlib import Path
import timestring
import pickle

#Pego o diretorio atual
raiz = os.getcwd()

raiz+="/videos"
print(raiz)
estado1 = False

#Variavei iniciais
kon = Conexao()
tempo_processo = float(kon.tempo_processo())

num_tentativas = int(kon.num_tentativas())

confiabilidade = float(kon.confiabilidade())

#Alpr
alpr = Alpr("br", "/etc/openalpr/openalpr.conf", "/home/pi/openalpr/runtime_data")
if not alpr.is_loaded():
	print("Error loading OpenALPR")
	sys.exit(1)

alpr.set_top_n(1)
alpr.set_default_region("md")
#Alfabeto
alfabeto = list(string.ascii_uppercase)
while True:
	#Pegando os dados
	tempo_processo = float(kon.tempo_processo())

	num_tentativas = int(kon.num_tentativas())

	confiabilidade = float(kon.confiabilidade())

	if os.path.exists(raiz):
		os.chdir(raiz)
		estado1 = False
		estado = False
		#Listo todos os arquivos da pasta
		#Crio lista de todos os arquivos
		data_criacao = lambda f: f.stat().st_ctime
		data_modificacao = lambda f: f.stat().st_mtime

		directory = Path(raiz)
		files = directory.glob('*.avi')
		arquivos = sorted(files, key=data_modificacao, reverse=False)
		
		b= ""
		if(len(arquivos) > 0):
			#Pegando um arquivo
			for n in arquivos:
				k = str(n)
				break

			c=0
			for j in k:
				if j == "/":
					c+=1
			h=0
			b = ""
			for j in k:
				if j == "/":
					h+=1
					continue
				if h == c:
					b+=j 

			for x in b:
				if x == "n":
					estado1 = False
					break
				else:
					estado1 = True
					print("Buscando placa no arquivo:")
					print("Arquivo: %s" %b)
					
					break

	else:
		#print("Diretorio nao encontrado")
		estado1 = False

	if estado1 == True:
		#Tentar ler placa

		cap = cv2.VideoCapture()
		cap.open(b)
		inicio = time.time()

		resultado = 0

		k = False

		num_ten = 0

		placa = ""

		est = True

		contador = 0

		while(cap.isOpened()):
			ret, frame = cap.read()
			if ret:

				if resultado >= tempo_processo:
					est = True
					break

				if num_ten >= num_tentativas:
					est = True
					break

				cv2.imwrite("img.jpg", frame)

				results = alpr.recognize_file("img.jpg")

				i = 0

				#Para o openalpr
				for plate in results['results']:
					i += 1
					print("Plate #%d" % i)
					print("   %12s %12s" % ("Plate", "Confidence"))

					for candidate in plate['candidates']:
						prefix = "-"
						if candidate['matches_template']:
							prefix = "*"

						print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

						#Adiciono somente as que tem 7 caracteres

						u = str(candidate['plate'])
						confia = float(candidate['confidence'])
						print(confia)
						print(u)
						if confia >= confiabilidade:
							contador = 0
							num_ten += 1
							if len(u) == 7:
								#Tem mais de 7 caracteres, testo se sao 3 letras e 4 numeros
								for v in u:
									validar = False
									#Testo se pertence ao alfabeto

									if contador < 3:
										for j in alfabeto:

											if v == j:
												contador+=1
												break
									else:
										#Valido se a proxima letra é do alfabeto
										try:
											if v == 'O':
												v = 0

											if v == 'Z':
												v = 7

											int(v)
											contador+=1

										except ValueError:
											contador = 0
											break

						#Caso ja tenha a placa mando pro obj
						if contador == 7:
							placa = u
							estado = True
							break


				fim = time.time()

				resultado = fim - inicio
				print(resultado)
				#Reconheceu mando pro banco
				if estado == True:
					print("Placa Encontrada")
					#Escreve no arquivo
					try:
						arq = open("placa.dat", "wb")
						#Placa
						pickle.dump(placa, arq)
						#Data
						dat = datetime.datetime.now()
						ds = dat.strftime('%d-%m-%Y %H:%M:%S')
						pickle.dump(ds, arq)

						arq.close()
					except:
						pass

					est = False

					#Para conseguir a data pra por no banco
					g = 0

					dat = ""
					hora = ""
					tipo = ""
					#akak
					#print(j)
					s = 0
					for x in b:

						if x != " " and s == 0:
							#print(x)
							dat += x
						else:
							s+=1

						if s >= 1:
							if x != ".":

								hora += x

							else:
								break

					j = ""
					g = 0

					#Vendo o tipo
					d = False
					for x in hora:
						if x == "_":
							d = True
							continue
						if d == True:
							tipo+= x

					for x in hora:

						if x == "-":
							g+=1
							if g == 3:
								j += "."
								continue
							else:
								j+=x
						else:
							j+=x

					hora = ""
					for x in j:
						 if x != "_":
						 	hora+=x
						 else:
						 	break



					hora = hora.replace("-", ":")

					dat = dat+hora

					#Mando pro tipo certo
					dat = timestring.Date(dat)
					dat = str(dat)
					kon = Conexao()

					if tipo == "entrada":
						tupla = (placa, dat)
						kon.att_placa_entrada(tupla)
						tupla = (1, dat)
						kon.att_processo_entrada(tupla)
						print("Atualizado o Registro com sucesso")

					else:
						tupla = (placa, dat)
						kon.att_placa_saida(tupla)
						tupla = (1, dat)
						kon.att_processo_saida(tupla)	
						print("Atualizado o Registro com sucesso")					


					print("Numero da placa Registrado no Banco: %s" %placa)
					estado = False
					break

			else:
				#Se n tiver mais frames paro
				break
		#N conseguiu ler
		if est == True:
			print("Placa Não Encontrada")
			#Nao leu placa mando

			#Para conseguir a data pra por no banco
			g = 0

			dat = ""
			hora = ""
			tipo = ""
			#akak
			#print(j)
			s = 0
			for x in b:

				if x != " " and s == 0:
					#print(x)
					dat += x
				else:
					s+=1

				if s >= 1:
					if x != ".":

						hora += x

					else:
						break

			j = ""
			g = 0

			#Vendo o tipo
			d = False
			for x in hora:
				if x == "_":
					d = True
					continue
				if d == True:
					tipo+= x

			for x in hora:

				if x == "-":
					g+=1
					if g == 3:
						j += "."
						continue
					else:
						j+=x
				else:
					j+=x

			hora = ""
			for x in j:
				 if x != "_":
				 	hora+=x
				 else:
				 	break

			hora = hora.replace("-", ":")

			dat = dat+hora

			#Mando pro tipo certo
			dat = timestring.Date(dat)
			dat = str(dat)
			kon = Conexao()

			if tipo == "entrada":
				tupla = (2, dat)
				kon.att_processo_entrada(tupla)

			else:
				tupla = (2, dat)
				kon.att_processo_saida(tupla)



		#Excluindo o arquivo de video
		try:
			os.remove(b)
		except:
			pass

