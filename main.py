# main.py
from lark import Lark, Transformer

# --- Parser ---
# Definimos la gramática de expresiones regulares: union (+), concatenación, estrella (*)
grammar = """
?start: expr
?expr: expr "+" term   -> union
     | term
?term: term factor     -> concat
     | factor
?factor: base "*"       -> star
       | base
?base: "(" expr ")"
     | CHAR
CHAR: /[a-z]/
%ignore " "
"""

# Transformador: convierte el árbol sintáctico en tuplas que describen las operaciones
class RegexTransformer(Transformer):
    def union(self, items): return ('union', items[0], items[1])
    def concat(self, items): return ('concat', items[0], items[1])
    def star(self, items): return ('star', items[0])
    def CHAR(self, item): return str(item)

# Función que parsea la expresión usando Lark y devuelve el árbol transformado
def parse_expression(regex):
    print("Parsing regex:", regex)
    parser = Lark(grammar, start='start', parser='lalr', transformer=RegexTransformer())
    print(parser.parse(regex))
    return parser.parse(regex)

# Clase que define cada estado del autómata, con un identificador único
class State:
    count = 0
    def __init__(self):
        self.id = State.count
        State.count +=1

# Función principal que construye el autómata a partir del árbol sintáctico
# Usa el algoritmo de Thompson

def build_automata(tree):
    typ = tree[0] # La estructura sera algo asi: ('union', subtree1, subtree2)
    if isinstance(tree, str):  # Caso base: símbolo simple
        s1, s2 = State(), State()
        return {'states':[s1,s2], 'start':s1, 'end':s2, 'transitions':[(s1,s2,tree)]}
    if typ == 'union':  # Unión: crea estados nuevos y combina los autómatas
        a1 = build_automata(tree[1])
        a2 = build_automata(tree[2])
        s_start, s_end = State(), State()
        states = a1['states'] + a2['states'] + [s_start, s_end]
        transitions = a1['transitions'] + a2['transitions']
        transitions += [(s_start,a1['start'],'λ'), (s_start,a2['start'],'λ'), (a1['end'],s_end,'λ'), (a2['end'],s_end,'λ')]
        return {'states':states, 'start':s_start, 'end':s_end, 'transitions':transitions}
    if typ == 'concat':  # Concatenación: conecta el final del primero con el inicio del segundo
        a1 = build_automata(tree[1])
        a2 = build_automata(tree[2])
        transitions = a1['transitions'] + a2['transitions'] + [(a1['end'],a2['start'],'λ')]
        states = a1['states'] + a2['states']
        return {'states':states, 'start':a1['start'], 'end':a2['end'], 'transitions':transitions}
    if typ == 'star':  # Estrella: agrega bucles y transiciones vacías (λ)
        a = build_automata(tree[1])
        s_start, s_end = State(), State()
        transitions = a['transitions']
        transitions += [(s_start,a['start'],'λ'), (a['end'],a['start'],'λ'), (a['end'],s_end,'λ'), (s_start,s_end,'λ')]
        states = a['states'] + [s_start, s_end]
        return {'states':states, 'start':s_start, 'end':s_end, 'transitions':transitions}
