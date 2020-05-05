# -*- coding: utf-8 -*-
def find_number(string):
	cont,i = 0,0
	list =[]
	while i < len(string):
		if(string[i].isdigit()):
			if cont == 0:
				list.append(i)
				cont += 1
			if i+1 < len(string) and string[i+1].isdigit()==False:
				list.append(i+1)
				break
				
		i += 1
	return list
try:
	#Busca episodios que faltan
	episodios = open("episodios.txt","r",encoding='utf-8')
	episodios_list = episodios.readlines()
	episodios.close()
	episodios_list = episodios_list
	nro_cap_faltantes = []
	for x in episodios_list:
		if(x != '\n' and ('Episodio' in x)):
			value = find_number(x)
			nro_cap_faltantes.append(int(x[value[0]:value[1]]))

	import pathlib

	path = pathlib.Path("/media/conan/Conan4069/animes/Detective Conan")
	conan = open('episodios faltantes detective conan.txt','w')
	count = 0
	nro_cap_disponibles = []

	for detective in path.iterdir():
		if ('_DC_sub' in str(detective.stem)):
			nro = find_number(str(detective.stem))
			cap = detective.stem[nro[0]:nro[1]]
			nro_cap_disponibles.append(int(cap))
	nro_cap_faltantes.sort()
	nro_cap_disponibles.sort()
	conan.write('#######----Episodios por buscar de detective conan----########\n')
	for x in nro_cap_faltantes:
		if x not in nro_cap_disponibles:
			conan.write(str(x) + ',')
	conan.write('\n#######----Episodios Que tengo y no estan en la lista----########\n')
	for x in nro_cap_disponibles:
		if x not in nro_cap_faltantes:
			conan.write(str(x) + ',')
	conan.close()


except FileNotFoundError:
	print('Felicidades no tienes caps por buscar')
