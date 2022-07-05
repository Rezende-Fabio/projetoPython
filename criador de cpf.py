from random import randint
    
carac = randint(0, 9)
carac1 = randint(0, 9)
carac2 = randint(0, 9)
carac3 = randint(0, 9)
carac4 = randint(0, 9)
carac5 = randint(0, 9)
carac6 = randint(0, 9)
carac7 = randint(0, 9)
carac8 = randint(0, 9)

soma1 = carac *10 + carac1 *9 + carac2 *8 + carac3 *7 + carac4 *6 + carac5 *5 + carac6 *4 + carac7 *3 + carac8 *2
result1 = soma1 * 10 %11

soma2 = carac *11 + carac1 *10 + carac2 *9 + carac3 *8 + carac4 *7 + carac5 *6 + carac6 *5 + carac7 *4 + carac8 *3 + result1 *2
result2 = soma2 *10 %11

if result1 == 10:
    result1 = 0

if result2 == 10:
    result2 = 0

print(f"Aqui está o CPF válido: {carac}{carac1}{carac2}.{carac3}{carac4}{carac5}.{carac6}{carac7}{carac8}-{result1}{result2}")