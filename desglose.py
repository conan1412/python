#Miguel Villamizar

valor_moneda = (20000,10000,5000,2000,1000,500,100,50,20,10,5,2)
nro_moneda = {'2': 0,'5': 0,'10': 0,'20': 0,'50': 0,'100': 0,'500': 0,'1000': 0,'2000': 0,'5000': 0,'10000': 0,'20000': 0 }
def desglosador (cantidad):
    cont = 0

    while cantidad > 0 and cont < len(valor_moneda):
        '''if (cantidad%valor_moneda[cont] == 0):
            cantidad -= valor_moneda[cont]
            nro_moneda[str(valor_moneda[cont])] += 1
            cont2 = 0
            while cont > cont2:
                if (cantidad%valor_moneda[cont2] == 0):
                    cont = cont2
                cont2 += 1
            continue'''
        if (cantidad >= valor_moneda[cont]):
            cantidad -= valor_moneda[cont]
            nro_moneda[str(valor_moneda[cont])] += 1
            continue
        cont += 1
    if cantidad != 0:
        print ("No hay un cambio exacto para ese valor faltaron %d Bsf"%cantidad)

valor = input("ingrese el valor a desglosar: ")
desglosador(valor)
print ("***Usted recibira***")

for indice in nro_moneda:
    if nro_moneda[indice] != 0:
        if indice == '100' or indice == '50' or indice == '10':
            print ("%d moneda(s) de %s Bsf" % (nro_moneda[indice],indice))
        else :
            print ("%d Billete(s) de %s Bsf" % (nro_moneda[indice],indice))
