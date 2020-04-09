########################################################
#
#	COUNTRIES:
#	
#
########################################################

#######################
#		PORTUGAL
#######################

def checkFirstDigits_PT(nif):
	if int(nif[0]) in [1,2,3,5,6,8]:
		return True 
	if int(nif[0:2]) in [45,70,71,72,74,75,77,78,79,90,91,98,99]:
		return True 
	return False

def getControl_PT(nif):
	total = 0
	for i in range(8):
		total += int(nif[7-i]) * (i+2)
	total %= 11
	if total < 2:
		return 0
	return 11 - total

def isWellFormated_PT(nif):
	if len(nif) < 9 or len(nif) > 9:
		return False
	if not nif.isdigit():
		return False
	return checkFirstDigits_PT(nif)

def isNIFValid_PT(nif):
	if not isWellFormated_PT(nif):
		return False
	return getControl_PT(nif) == int(nif[8])
	
	#try:	# use isdigit()?
	#	if len(nif) < 9 or len(nif) > 9:
	#		return False
	#	if checkFirstDigits_PT(nif) and getControlDigit_PT(nif) == int(nif[8]):
	#		return True
	#	else:
	#		return False
	#except:	# most likely a letter => not PT? => false
	#	return False



#######################
#		SPAIN
#
#
#	NIF / NIE / NIF
#	8c (8 DIGITS + 1 LETTER)
#	K7c
#	L7c
#	M7c
#	X7c
#	Y7c
#	Z7c
#
#######################

def isWellFormated_ES(nif):
	if len(nif) != 9:
		return False
	# nid => only last is alpha
	if nif[0].isdigit():
		if not nif[0:8].isdigit():
			return False
	else: # nie => first and last are alpha
		if not nif[0].isalpha() or nif[0] not in ['K','L','M','X','Y','Z']:
			return False

	if not nif[8].isalpha():
			return False
	return True
	
def getControl_ES(nif):
	values = {
		0: 'T',
		1: 'R',
		2: 'W',
		3: 'A',
		4: 'G',
		5: 'M',
		6: 'Y',
		7: 'F',
		8: 'P',
		9: 'D',
		10: 'X',
		11: 'B',
		12: 'N',
		13: 'J',
		14: 'Z',
		15: 'S',
		16: 'Q',
		17: 'V',
		18: 'H',
		19: 'L',
		20: 'C',
		21: 'K',
		22: 'E'
	}
	if not nif[0].isdigit():
		nif = nif[0:8].lower().replace("x", "0").replace("y", "1").replace("z", "2")
	remain = int(nif[0:8]) % 23
	return values[remain]
	



def isNIFValid_ES(nif):
	if not isWellFormated_ES(nif) or getControl_ES(nif) != nif[8]:
		return False
	return True


#######################
#		GERMANY
#
#	DE123046548	32012/26258	DE118620626	ATU3677941	PT98031090	HRB228000
#
#######################
