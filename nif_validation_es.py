########################################################
#
#	VALIDACAO DO NIF (spanish only)
#
#	NID
#	NIF
#	NIE (numero de identificaccion de estrangeros)
#
########################################################

import nif_validation


def test1():
	nif = '34871242E'
	return nif_validation.isNIFValid_ES(nif)


def test2():
	nif = 'Y4120867V'
	return nif_validation.isNIFValid_ES(nif)

		
		
def test3():
	nif = 'Y4120869V'
	return not nif_validation.isNIFValid_ES(nif)



def test4():
	nif = 'Z4120869V'
	return not nif_validation.isNIFValid_ES(nif)


#if test1() and test2() and test3() and test4():
#	print ("OK")
#else:
#	print ("not ok")
#exit()

	
################################################
#		DATABASE AND OPS
################################################

def ValidateInDatabase():

	import mysql.connector
	import re
	
	MYSQL_CONN_INFO = {
		'host': '127.0.0.1',
		'user': 'root',
		'password': '',
		'database': 'XXX'
	}


	mycursor = None
	mydb = None


	print ("\n\nAttempting to connect to MySql database ...")

	try:
		mydb = mysql.connector.connect(**MYSQL_CONN_INFO)
			
		if mydb:
			print ("## CONNECTED TO MYSQL DB ##")
			mycursor = mydb.cursor()
		else:
			print ("## UNABLE TO CONNECTO TO MYSQL ##")
	except Exception as e:
		print ("ERROR - ## UNABLE TO CONNECTO TO MYSQL ##", e)


	query_get_ents = '''
		select 
			ID_ENTIDADE, 
			NIF_NIPC 
		from 
			entidade 
		where 
			NIF_NIPC is not null
		and
			PAIS_ID_PAIS = 5
	'''

	query_insert = '''
		insert into
			ENTIDADE_NIF_INVALID(`ID_ENTIDADE`) 
		VALUES 
			(%s)
	'''

	print ("\n\nFectching all spanish entities with NIF ...")
	mycursor.execute(query_get_ents)
	entidades =  mycursor.fetchall()

	print ("\n\nChecking ...")
	counter = 0
	for entidade in entidades:
		counter += 1
		if counter % 1000 == 0:
			print (counter)
			mydb.commit()

		if nif_validation.isNIFValid_ES(re.sub(r'\W+', '', entidade[1])):
			mycursor.execute(query_insert, (entidade[0],))
			#print ("entidade com nif valido > ",entidade[0], entidade[1]) 


		

			
	mydb.commit()	

ValidateInDatabase()

