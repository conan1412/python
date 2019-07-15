'''
@author Miguel Eduardo Villamizar 
@email mevr02@gmail.com
 '''
def generate_letter(number):
    values = {
        'UNITS': (
            '',
            'UN ',
            'DOS ',
            'TRES ',
            'CUATRO ',
            'CINCO ',
            'SEIS ',
            'SIETE ',
            'OCHO ',
            'NUEVE ',
            'DIEZ ',
            'ONCE ',
            'DOCE ',
            'TRECE ',
            'CATORCE ',
            'QUINCE ',
            'DIECISEIS ',
            'DIECISIETE ',
            'DIECIOCHO ',
            'DIECINUEVE ',
            'VEINTE '
        ),        
        'TENS' : (
            '',
            'VEINTI',
            'TREINTA ',
            'CUARENTA ',
            'CINCUENTA ',
            'SESENTA ',
            'SETENTA ',
            'OCHENTA ',
            'NOVENTA ',
            'CIEN '
        ),
        'HUNDREDS' : (
            'CIENTO ',
            'DOSCIENTOS ',
            'TRESCIENTOS ',
            'CUATROCIENTOS ',
            'QUINIENTOS ',
            'SEISCIENTOS ',
            'SETECIENTOS ',
            'OCHOCIENTOS ',
            'NOVECIENTOS '
        ),
        'BIGUNITS' : (
            ('',''),
            ('MIL ','MIL '),
            ('MILLON ','MILLONES '),
            ('MIL MILLONES ','MIL MILLONES '),
            ('BILLON ','BILLONES '),
            ('MIL BILLONES ','MIL BILLONES '),
            ('TRILLON ','TRILLONES '),
            ('MIL TRILLONES','MIL TRILLONES'),
            ('CUATRILLON','CUATRILLONES'),
            ('MIL CUATRILLONES','MIL CUATRILLONES'),
            ('QUINTILLON','QUINTILLONES'),
            ('MIL QUINTILLONES','MIL QUINTILLONES'),
            ('SEXTILLON','SEXTILLONES'),
            ('MIL SEXTILLONES','MIL SEXTILLONES'),
            ('SEPTILLON','SEPTILLONES'),
            ('MIL SEPTILLONES','MIL SEPTILLONES'),
            ('OCTILLON','OCTILLONES'),
            ('MIL OCTILLONES','MIL OCTILLONES'),
            ('NONILLON','NONILLONES'),
            ('MIL NONILLONES','MIL NONILLONES'),
            ('DECILLON','DECILLONES'),
            ('MIL DECILLONES','MIL DECILLONES'),
            ('UNDECILLON','UNDECILLONES'),
            ('MIL UNDECILLONES','MIL UNDECILLONES'),
            ('DUODECILLON','DUODECILLONES'),
            ('MIL DUODECILLONES','MIL DUODECILLONES'),
        )
    }
    #Change if your point float is spanish or english
    number = number.split(".")
    count = 0
    big_letter = ''
    i = len(number) - 1
    while(i >= 0):
        letter = ''
        zero = False
        one = False
        tens = False
        if(len(number[i]) == 3):
            if(int(number[i]) == 100):
                letter += 'CIEN '
            else:
                if(int(number[i][0]) != 0):
                    letter += values['HUNDREDS'][int(number[i][0])-1]
                else:
                    zero = True
                if(int(number[i][1:]) > 20):
                    letter += values['TENS'][int(number[i][1])-1]
                    tens = True
                if(tens):
                    if(int(number[i][2]) == 0 or int(number[i][1]) == 2):
                        if(count == 0 and int(number[i][2]) == 1):
                            letter += 'UNO '
                        else:
                            letter += values['UNITS'][int(number[i][2])]
                    else:
                        if(count == 0 and int(number[i][2]) == 1):
                            letter += 'Y UNO '
                        else:
                            letter += 'Y ' + values['UNITS'][int(number[i][2])]
                    if (int(number[i][2]) == 1):
                        one = True
                else:
                    if(count == 0 and int(number[i][1:]) == 1):
                        letter += 'UNO '
                    else:
                        letter += values['UNITS'][int(number[i][1:])]
        if(len(number[i]) == 2):
            if(int(number[i][0:]) > 20):
                letter += values['TENS'][int(number[i][0])-1]
                tens = True
            if(tens):
                if(int(number[i][1]) == 0 or int(number[i][0]) == 2):
                    if(count == 0 and int(number[i][1]) == 1):
                        letter += 'UNO '
                    else:
                        letter += values['UNITS'][int(number[i][1])]
                else:
                    if(count == 0 and int(number[i][1]) == 1):
                        letter += 'Y UNO '
                    else:
                        letter += 'Y ' + values['UNITS'][int(number[i][1])]
                if (int(number[i][1]) == 1):
                    one = True
            else:
                letter += values['UNITS'][int(number[i][0:])]
        elif(len(number[i]) == 1):
            if(count == 0 and int(number[i][0]) == 1):
                letter += 'UNO '
            else:
                letter += values['UNITS'][int(number[i][0])]
            if (int(number[i][0]) == 1):
                    one = True
        if(one):
            if(count == 1):
                letter = values['BIGUNITS'][count][0]
            else:
                letter = letter + values['BIGUNITS'][count][0]
        else:
            if(not zero):
                letter = letter + values['BIGUNITS'][count][1]
        big_letter = letter + big_letter[0:]
        i -= 1
        count += 1
    return big_letter

def compute_number(cash):
    #Change if your point float is spanish or english
    cash = cash.split(",")
    if(len(cash) == 1):
        cash.append('00')
    #change for defined  other million point
    cash[0]= cash[0].replace(".","")
    i = len(cash[0]) - 1
    count = 1
    while(i>=0):
        if(count == 3 and i > 0):
            #change el '.' depend of type of decimal
            cash[0] = cash[0][:i] + '.' + cash[0][i:] 
            count = 0
        count += 1  
        i -= 1
    letter = generate_letter(cash[0]) + 'CON ' + cash[1] + '/100'
    return letter

#Area for enter numbers
while True:
    print('###### Cambio de numero a letras ###### (Para salir presione s)\n')
    number = input('Ingrese valor: ')
    if(number == 's'):
        break
    if(number.replace(',','').replace('.','').isdigit()):
        print (compute_number(number) + "\n\n")
    else:
        print('Solo debe insertar numeros')