import mysql.connector
import base64
import io
import PIL.Image

class Conexao:

	#Metodo para conexao

	def update(self):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			cursor.execute("SELECT up FROM Configuracao")

			rs = cursor.fetchone()

			for x in rs:
				return x

			cursor.close()

		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def confiabilidade(self):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			cursor.execute("SELECT confiabilidade FROM Configuracao")

			rs = cursor.fetchone()

			for x in rs:
				return x

			cursor.close()

		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def tempo_processo(self):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			cursor.execute("SELECT tempo_processo FROM Configuracao")

			rs = cursor.fetchone()

			for x in rs:
				return x

			cursor.close()

		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def num_tentativas(self):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			cursor.execute("SELECT num_tentativas FROM Configuracao")

			rs = cursor.fetchone()

			for x in rs:
				return x

			cursor.close()

		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def idUnd(self):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			cursor.execute("SELECT id FROM Estacionamento")

			rs = cursor.fetchone()

			for x in rs:
				return x

			cursor.close()

		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def contador(self):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			cursor.execute("SELECT nControle FROM Registro ORDER BY id DESC LIMIT 1")

			rs = cursor.fetchone()

			for x in rs:
				return x

			cursor.close()

		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)
		    

	def tempo_gravacao(self, x):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			cursor.execute("SELECT tempo_gravacao FROM Configuracao WHERE equipamento = %s" %x)

			rs = cursor.fetchone()

			for x in rs:
				return x

			cursor.close()

		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def consultaData(self):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			cursor.execute("SELECT data_entrada, data_saida, data_erro FROM Registro ORDER BY id DESC LIMIT 1")

			rs = cursor.fetchone()

			return rs

			cursor.close()

		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def modo(self, x):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			cursor.execute("SELECT modo FROM Configuracao WHERE equipamento = %s" %x)

			rs = cursor.fetchone()

			for x in rs:
				return x

			cursor.close()

		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	#Para alterar banco

	def att_placa_entrada(self, tupla):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()


			sql = ("UPDATE Registro SET placa = %s WHERE data = %s and  tipo_entrada = '1'")

			cursor.execute(sql, tupla)

			db.commit()

			cursor.close()
			
		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def att_placa_saida(self, tupla):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			sql = ("UPDATE Registro SET placa = %s WHERE data = %s and  tipo_entrada = '2'")

			cursor.execute(sql, tupla)

			db.commit()

			cursor.close()
			
		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def att_processo_entrada(self, tupla):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			sql = ("UPDATE Registro SET processado = %s WHERE data = %s and  tipo_entrada = '1'")


			cursor.execute(sql, tupla)

			db.commit()

			cursor.close()
			
		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def att_processo_saida(self, tupla):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()

			sql = ("UPDATE Registro SET processado = %s WHERE data = %s and  tipo_entrada = '2'")

			cursor.execute(sql, tupla)

			db.commit()

			cursor.close()
			
		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

	def cadastra(self, objeto):
		try:
			db = mysql.connector.connect(user='root', password='123',
			                              host='localhost',
			                              database='Dados')

			cursor = db.cursor()
			foto = None
			id_foto = None

			"""if objeto.data is not None:
			
				#Para a foto
				with open(objeto.id_foto, 'rb') as f:
					photo = f.read()

				foto = base64.b64encode(photo)

			else:
				foto = None
			"""
			if objeto.iD is None:

				sql = "INSERT INTO Registro ( data , tipo_entrada, tipo_vei, processado, id_foto, foto, equipamento, estacionamento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
				val = (objeto.data, objeto.tipo_entrada, objeto.tipo_vei, 0, objeto.id_foto, foto, objeto.idTerm, objeto.idUnd)

			else:

				sql = "UPDATE Registro SET data =%s , tipo_entrada =%s, tipo_vei =%s, processado =%s, id_foto =%s, foto =%s, equipamento =%s, estacionamento =%s WHERE id = %s"
				val = (objeto.data, objeto.tipo_entrada, objeto.tipo_vei, 0, objeto.id_foto, foto, objeto.idTerm, objeto.idUnd, objeto.iD)

			cursor.execute(sql, val)

			db.commit()

			cursor.close()

			k = cursor.lastrowid

			return k
			
		#Caso aconteça erro
		except mysql.connector.Error as err:

			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Usuario ou senha invalido")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Banco de Dados não existe")
			else:
				print(err)

