#Capitulos esenciales de detective conan los q me faltan por tener en mi coleccion personal

def find_number(string):
	cont,i = 0,0
	list =[]
	while i < len(string):
		if(string[i].isdigit()):
			if cont == 0:
				list.append(i)
				cont += 1
			if i+1 < len(string) and ((string[i+1].isdigit()==False and string[i+1].isalpha()==False) or string[i+1].isalpha()):
				list.append(i+1)
				break
				
		i += 1
	return list

import pathlib
path = pathlib.Path("C:/Users/mevr_/Downloads")

for detective in path.iterdir():
	if('AnimeMF.net' in str(detective)):
		nro = find_number(str(detective.stem))
		cap = detective.stem[nro[0]:nro[1]]
		detective.rename(str(detective).replace(detective.stem,str(cap)+'_DC_sub'))
	if('Seba_767' in str(detective)):
		nro = find_number(str(detective.stem))
		cap = detective.stem[nro[0]:nro[1]]
		detective.rename(str(detective).replace(detective.stem,str(cap)+'_DC_sub'))
	if('[APTX-Fansub]' in str(detective)):
		nro = find_number(str(detective.stem))
		cap = detective.stem[nro[0]:nro[1]]
		detective.rename(str(detective).replace(detective.stem,str(cap)+'_DC_sub'))
		
