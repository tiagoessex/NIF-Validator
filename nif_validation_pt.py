########################################################
#
#	VALIDACAO DO NIF (portuguese only)
#
#	invalidos são gravados numa table à parte e não 
#	sinalizados num campo na table de entitidaes devido
#	a "quem sabe quem e quando vai mudar a tabela de entidades"? 
#
########################################################

import nif_validation

def test1():
	nif = '234543120'
	return not nif_validation.isNIFValid_PT(nif)

	

def test2():
	nif = '234543124'
	return nif_validation.isNIFValid_PT(nif)


def test3():
	nif = '234'
	return not nif_validation.isNIFValid_PT(nif)



def test4():
	nif = '2A4543124'
	return not nif_validation.isNIFValid_PT(nif)


#test1()
#test2()
#test3()
#test4()
		
################################################
#		DATABASE AND OPS
################################################

def ValidateInDatabase():

	import mysql.connector

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
			PAIS_ID_PAIS = 12
	'''

	query_insert = '''
		insert into
			ENTIDADE_NIF_INVALID(`ID_ENTIDADE`) 
		VALUES 
			(%s)
	'''

	print ("\n\nFectching all portuguese entities with NIF ...")
	mycursor.execute(query_get_ents)
	entidades =  mycursor.fetchall()

	print ("\n\nChecking ...")
	counter = 0
	for entidade in entidades:
		counter += 1
		if counter % 1000 == 0:
			print (counter)
			mydb.commit()

		if not nif_validation.isNIFValid_PT(entidade[1]):
			mycursor.execute(query_insert, (entidade[0],))


		

			
	mydb.commit()	


ValidateInDatabase()
