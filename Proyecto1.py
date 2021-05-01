# Universidad del Valle de Guatemala
# Diseno de Lenguajes de Programacion - Seccion 10
# Proyecto 1 - Programa principal (lectura de regex y cadena)
# Maria Fernanda Estrada 14198
# Marzo 2021



# Libreria para generar graficas
from graphviz import Digraph
# Importar funciones para generar Arbol
from Arbol import *
# Importar funciones para generar AFN (Thompson)
from Thompson import *
# Importar funciones para generar AFD (Subconjuntos)
from Subconjuntos import *
# Importar funciones para generar AFD (Directo)
from Directo import *
# Libreria para obtener timepo de simulacion
import time


# Simbolos
epsilon = 'ε'
or_symbol = "|"
and_symbol = "~"
kleen_symbol = "*"
positive_closure_symbol = "+"
zero_or_one_symbol = "?"


# Leer input. Verificar si hay error. Si hay, volver a pedir la expresion e indicar error. Si no hay, seguir con el programa.
while True:
    # Input regex
    regex_str = input("\nIngrese expresion regular: ")

    # Verificacion de errores
    if (regex_str.count("(") == regex_str.count(")")):
        if (regex_str.find("|*") == -1) and (regex_str.find("|+") == -1) and (regex_str.find("|?") == -1):
            if (regex_str[0] != "|") and (regex_str[0] != "+") and (regex_str[0] != "*") and (regex_str[0] != "?"):
                
                # Obtener alfabeto
                letters = regex_str.replace('|','')
                letters = letters.replace('*','')
                letters = letters.replace('+','')
                letters = letters.replace('?','')
                letters = letters.replace('(','')
                letters = letters.replace(')','')

                alphabet = set()
                for l in letters:
                    alphabet.add(l)

                # Generar arbol
                node = create_node(regex_str)
                read_r(node, alphabet)
                d = Digraph(comment='Tree')
                grph(node, d)
                d.render('Arbol 1.gv', view=True)

                # Generar AFN
                fas = thompson(node)
                grph_fas(fas, 'AFN (Thompson)')

                # Generar AFD
                afd_sub = subsets(fas, alphabet)
                grph_fas(afd_sub, 'AFD (Subconjuntos)')

                # Directo
                node_pos = add_hashtag(node)
                sym = add_first_last_pos(node_pos)
                d2 = Digraph(comment='Tree2')
                grph_2(node_pos,d2)
                d2.render('Arbol 2.gv', view=True)
                afd_direct = make_direct_afd(node_pos, sym, alphabet)
                grph_fas(afd_direct, 'AFD (Directo)')

                break

            else:
                print("\n *** ERROR EN LA EXPRESION REGULAR. VERIFICAR OPERADORES/PARENTESIS. ***")
        else:
            print("\n *** ERROR EN LA EXPRESION REGULAR. VERIFICAR OPERADORES/PARENTESIS. ***")
    else:
        print("\n *** ERROR EN LA EXPRESION REGULAR. VERIFICAR OPERADORES/PARENTESIS. ***")


# Simular determinista
def simulate_det(cadena, afd):
    current_state = afd['initial_state']
    regected = False
    for s in cadena:
        found_transition = False
        for transition in afd['transitions']:
            if(transition['from'] == current_state and transition['symbol'] == s):
                current_state = transition['to']
                found_transition = True
                break
        if(found_transition == False):
            regected = True
            break
    
    if(regected == False and current_state in afd['final_states']):
        print('ACEPTADO')
    else:
        print('RECHAZADO')


# Simular no determinista
def simulate_non_det(cadena, afn):
    current_state = {afn['initial_state']}
    regected = False
    for s in cadena:
        current_state_kleen = current_state.copy()
        for st in current_state:
            current_state_kleen.update(kleen(afn, st, set()))
        next_state = set()
        for transition in afn['transitions']:
            if(transition['from'] in current_state_kleen and transition['symbol'] == s):
                next_state.add(transition['to'])
        if(len(next_state) == 0):
            regected = True
            break
        else:
            current_state = next_state.copy()
    current_state_kleen = current_state.copy()
    for st in current_state:
        current_state_kleen.update(kleen(afn, st, set()))
    for st in current_state_kleen:
        if(regected == False and st in afn['final_states']):
            print('ACEPTADO')
            return
    print('RECHAZADO')

# Para simular la cadena en AFD y AFN
while(True):
    cadena = input('Ingrese cadena: ')

    # Determinista directo
    print('\nDeterminista Directo')
    start = time.perf_counter()
    simulate_det(cadena, afd_direct)
    finish = time.perf_counter()
    print('Tiempo de directo: {}s'.format(finish-start))

    # Determinista subconjuntos
    print('\nDeterminista Subconjuntos')
    start = time.perf_counter()
    simulate_det(cadena, afd_sub)
    finish = time.perf_counter()
    print('Tiempo de subconjuntos: {}s'.format(finish-start))

    # No determinista Thompson
    print('\nNo Determinista Thompson')
    start = time.perf_counter()
    simulate_non_det(cadena, fas)
    finish = time.perf_counter()
    print('Tiempo de Thompson: {}s'.format(finish-start))