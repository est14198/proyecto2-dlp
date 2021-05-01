# Universidad del Valle de Guatemala
# Diseno de Lenguajes de Programacion - Seccion 10
# Proyecto 1 - Algoritmo de Subconjuntos (Conversion AFN a AFD)
# Maria Fernanda Estrada 14198
# Marzo 2021



# Para generar graficas
from graphviz import Digraph


# Simbolos
epsilon = 'ε'
or_symbol = "|"
and_symbol = "~"
kleen_symbol = "*"
positive_closure_symbol = "+"
zero_or_one_symbol = "?"


# Crear diccionario con informacion del automata
def create_fa():
    fa = {
        "states": set(),
        "transitions": [],
        "initial_state": '',
        "final_states": []      
    }
    return fa


# KLEEN para completar subconjuntos. Determinar que estados ya se visitaron al aplicar KLEEN
def kleen(fn, state, checked):
    checked.add(state)
    for transition in fn['transitions']:
        if transition['from'] == state and transition['symbol'] == epsilon and transition['to'] not in checked:
            checked.update(kleen(fn, transition['to'], checked))  
    return checked


# Para moverse entre estados dado un alfabeto
def kleen_movs(state, states_d, fan, alphabet):
    new_transitions = []
    for letter in alphabet:
        new_state = set()
        for s in state:
            for transition in fan['transitions']:
                if (transition['from'] == s and transition['symbol'] == letter):
                    new_state.update(kleen(fan, transition['to'], set()))
        if(len(new_state)>0):
            new_state = frozenset(new_state)
            if (new_state not in states_d):
                states_d.add(new_state)
                new_states_d, new_new_transitions = kleen_movs(new_state, states_d, fan, alphabet)
                states_d.update(new_states_d)
                new_transitions += new_new_transitions
            new_transitions.append({'from': state, 'to': new_state, 'symbol': letter})
    return states_d, new_transitions


# Subconjuntos (AFN a AFD)
def subsets(fan, alphabet):
    afd = create_fa()

    # Estado inicial y se aplica KLEEN
    initial = fan['initial_state']
    initial = frozenset(kleen(fan, initial, set()))
    afd['initial_state'] = initial
    afd['states'].add(initial)

    # Transiciones y estados a partir del inicial dado un estado
    states, transitions = kleen_movs(afd['initial_state'], afd['states'], fan, alphabet)
    afd['states'].update(states)
    afd['transitions'] += transitions

    # Verificar quienes generan subconjuntos con el estado final
    for state in afd['states']:
        for s in state:
            if s in fan['final_states']:
                afd['final_states'].append(state)
                break

    # Pasos para "limpiar" el AFD generado. Colocar numeros en lugar del subconjnto como tal para que este ordenado.
    afd_clean = create_fa()
    afd_clean['transitions'] += afd['transitions']
    
    i=0
    for state in afd['states']:
        afd_clean['states'].add(i)
        # Limpiar estado inicial
        if(afd['initial_state'] == state):
            afd_clean['initial_state'] = i
        # Limpiar estados finales
        if(state in afd['final_states']):
            afd_clean['final_states'].append(i)
        # Limpiar transiciones de los estados normales
        for transition in afd_clean['transitions']:
            if(transition['from'] == state):
                transition['from'] = i
            if(transition['to'] == state):
                transition['to'] = i
        i += 1

    return afd_clean