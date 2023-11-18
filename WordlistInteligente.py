#!/usr/bin/env python

from itertools import permutations, product, combinations

print("\033[95m#################################")
print("\033[95m#     \033[1m\033[94mIntelligent Wordlists\033[0m\033[95m     #")
print("\033[95m#################################")
print("\n")
print("ENTER para no utilizar un dato")
print("Si quieres introducir varios datos, que estén separados por comas y sin espacios.")
print("Ej: Daniel,Fernando,Juan")
print("\n")

#Introduce los valores del usuario en el diccionario separando por comas
def actualizar_dicc(texto):
    if texto == "fechas":
        valor = input("Introduce una o varias " + texto + " en el siguiente formato dd/mm/yyyy: ")
        if comprobacion_fechas(valor):
            if valor != "":
                dicc.update({texto : valor.split(",")})
            else:
                dicc.update({texto:[]})
        else:
            print("Una de las fechas introducidas no es válida.")
            actualizar_dicc(texto)
    else:
        valor = input("Introduce un@ o vari@s " + texto + ": ")
        if valor != "":
            dicc.update({texto : valor.split(",")})
        else:
            dicc.update({texto:[]})

#Preguntas que se le hacen al usuario
def pedir_info():
    actualizar_dicc("nombres")
    actualizar_dicc("apellidos")
    actualizar_dicc("apodos")
    actualizar_dicc("fechas")
    actualizar_dicc("palabras extra")

#Añade los valores de una clave con la primera letra en mayusculas y en minusculas
def generador_simple(diccionario, clave):
    if len(diccionario.get(clave)) != 0:
        lista = diccionario.get(clave)
        for item in lista:
            yield item
    yield ""
                
#funcion para comprobar que las fechas se han introducido bien
def comprobacion_fechas(texto):
    if texto != "":
        elementos = texto.split(",")
        for fecha in elementos:
            partes = fecha.split("/")
            if len(partes) != 3:
                return False
        return True
    else: return True

#Genera todo lo relacionado con fechas
def generador_fechas(diccionario):
    if diccionario.get("fechas"):
        fechas = tratar_fechas(diccionario.get("fechas"))
        for tupla in fechas:
            yield tupla[0] #dia
            yield tupla[1] #mes
            yield tupla[2] #año
            yield (tupla[2])[-2:] #dos ultimos digitos del año
            yield tupla[1]+tupla[2] #mes año
            yield tupla[1]+(tupla[2])[-2:] #mes año (dos digitos)
            yield tupla[0]+tupla[1] #dia mes
            yield tupla[0] + tupla[1]+tupla[2] #dia mes año
            yield tupla[0] + tupla[1]+ (tupla[2])[-2:] #dia mes año(dos digitos)
    else:
        yield ""

#recibe las fechas y devuelve una lista de fechas cuyos elementos son tuplas de las fechas separadas por /
def tratar_fechas(fechas):
    tratadas = []
    for fecha in fechas:
        tratadas.append((fecha.split("/")[0], fecha.split("/")[1], fecha.split("/")[2]))
    return tratadas

#añade simbolos al final de las strings de un generador, los simbolos añadidos tienen el nº combinaciones de digitos
def generador_simbolos(combinaciones):
    simbolos = ("#","$","&","%","*","+")
    for combinacion in permutations(simbolos,combinaciones):
        for prod in product(*combinacion):
            yield ''.join(prod)    

#Concatena a una lista de palabras comunes, las palabras extra del usuario
def generador_comunes(diccionario):
    comunes = {"amor", "contraseña", "password", "sonrisa", "felicidad", "exito", "123456", "12345", "1234", "123", "futbol", "perro", "gato", "alegria", "sol", "cielo", "estrella", "tequiero"}
    if diccionario.get('palabras extra'):
        comunes = comunes.union(set(diccionario.get('palabras extra')))
    for comun in comunes:
        yield comun

#combina de todas las formas posibles las strings de una lista
def combinaciones(lista_strings, minimo):
    #Nueva lista que añade mayusculas y minusculas. Cada elemento de una lista es una tupla con las dos opciones
    #si en mayusculas y minusculas es igual (un numero/fecha) se añade una tupla de solo un elemento para evitar combinaciones repetidas
    lista_modificada = []
    for item in lista_strings:
        # Añade la versión en minúsculas y en mayúsculas si son diferentes.
        item_lower = item.lower()
        item_cap = item.capitalize()
        if item_lower != item_cap:
            lista_modificada.append((item_lower, item_cap))
        else:
            lista_modificada.append((item_lower,))
    # Todos los tamaños de posibles combinaciones
    for r in range(minimo, len(lista_modificada) + 1):
        # Se hacen todas las permutaciones de la lista modificada, de tamaño r
        for perm in permutations(lista_modificada, r):
            # itertools.product toma un número variable de argumentos (*perm)
            # Cada argumento es una tupla con las versiones en mayúsculas y minúsculas de una palabra
            for prod in product(*perm):
                # Se excluyen casos de la misma palabra en mayúscula y minúscula
                if len(set(map(str.lower, prod))) == r:
                    yield "".join(prod)

#Escribe todas las combinaciones de dos letras que corresponden a la primera letra de dos apellidos
def generador_combi_apellidos(diccionario):
    if diccionario.get("apellidos"):
        apellidos = diccionario.get("apellidos")
        letras = []
        for apellido in apellidos:
            letras.append(apellido[0])
        yield from combinaciones(letras,1)
    yield ""

# Escribe las contraseñas en chunks para no tener problemas de memoria (almacenar todas a la vez)
def escribir(diccionario, wordlist):
    chunk_size = 1000  # Define cuántas líneas quieres escribir a la vez
    contador = 0
    with open('wordlist.txt', 'w') as archivo:
        chunk = []
        for contrasena in generador_de_contrasenas(diccionario):
            chunk.append(contrasena+"\n")
            contador += 1
            if len(chunk) == chunk_size:
                archivo.writelines(chunk)
                chunk = []
            # Muestra el progreso cada cierto número de contraseñas generadas
            '''if contador % (contraseñas_estimadas // 10) == 0:
                print(f"{(contador / contraseñas_estimadas) * 100:.2f}% generado")'''
        # Escribe las contraseñas restantes si no llenaron el último chunk
        if chunk:
            archivo.writelines(chunk)


#-------------------------------Lógica para generar las contraseñas----------------------------------------------
def generador_de_contrasenas(diccionario):
          
    #todas las combinaciones (minimo 1) de nombres/apodos, apellidos, fechas, simbolos y comunes
    combinaciones_generadas = set()
    for nombre in generador_simple(diccionario,"nombres"):
        for apellido in generador_simple(diccionario,"apellidos"):
                for fecha in generador_fechas(diccionario):
                    for simbolo in generador_simbolos(1):
                        for comun in generador_comunes(diccionario):
                            # Crea la lista para la combinación actual
                            elementos_actuales = [nombre, apellido, fecha, simbolo, comun]
                            # Genera todas las combinaciones para estos elementos
                            for combinacion in combinaciones(elementos_actuales, 1):
                                # Verifica si la combinación ya se ha generado
                                if combinacion not in combinaciones_generadas:
                                    yield combinacion
                                    combinaciones_generadas.add(combinacion)
    
       
    #Nombres/apodos seguidos de dos inciales de apellidos mas fechas, simbolos y comunes
    for nombre in generador_simple(diccionario, "nombres"):
        for iniciales in generador_combi_apellidos(diccionario):
            for fecha in generador_fechas(diccionario):
                    for simbolo in generador_simbolos(1):
                        for comun in generador_comunes(diccionario):
                            # Crea la lista para la combinación actual
                            elementos_actuales = [nombre, iniciales, fecha, simbolo, comun]
                            # Genera todas las combinaciones para estos elementos
                            for combinacion in combinaciones(elementos_actuales, 1):
                                # Verifica si la combinación ya se ha generado
                                if combinacion not in combinaciones_generadas:
                                    yield combinacion
                                    combinaciones_generadas.add(combinacion)
 
    
def estimador_contraseñas(diccionario):
    variaciones = {
        'nombres': len(diccionario['nombres']) * 2,  # Asume 2 variantes por nombre
        'apellidos': len(diccionario['apellidos']) * 2,  # Asume 2 variantes por apellido
        'fechas': len(diccionario['fechas']) * 9,  # Asume 2 variantes por fecha
        'simbolos': 6, # Los símbolos solo cuentan una vez
        'extra': len(diccionario['palabras extra']) + 15
    }
    
    # Calcula todas las combinaciones posibles para cada número de elementos
    total_combinaciones = 0
    for i in range(1, len(variaciones) + 1):
        for combo in combinations(variaciones.values(), i):
            producto = 1
            for number in combo:
                producto *= number
            total_combinaciones += producto

    return total_combinaciones
    
#-----------------------------------------------MAIN--------------------------------------------------------------
dicc = dict()
pedir_info()
dicc["nombres"] = dicc.get("nombres") + dicc.get("apodos")
#contraseñas_estimadas = estimador_contraseñas
escribir(dicc, 'wordlist.txt')