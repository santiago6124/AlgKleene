# main.py
from lark import Lark, Transformer

# Gramática para expresiones regulares
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

# Transformer para construir el árbol sintáctico
class RegexTransformer(Transformer):
    def union(self, items): return ('union', items[0], items[1])
    def concat(self, items): return ('concat', items[0], items[1])
    def star(self, items): return ('star', items[0])
    def CHAR(self, item): return str(item)

def parse_expression(regex):
    print("Parsing regex:", regex)
    parser = Lark(grammar, start='start', parser='lalr', transformer=RegexTransformer())
    return parser.parse(regex)

# Clase para representar estados únicos
class State:
    count = 0
    def __init__(self):
        self.id = State.count
        State.count += 1
    def __repr__(self):
        return f"q{self.id}"

def build_automata(tree):
    if isinstance(tree, str):
        s1, s2 = State(), State()
        return {
            'states': [s1, s2],
            'start': s1,
            'finals': [s2],
            'transitions': [(s1, s2, tree)]
        }

    typ = tree[0]

    if typ == 'union':
        a1 = build_automata(tree[1])
        a2 = build_automata(tree[2])
        s_start = State()
        states = [s_start] + a1['states'] + a2['states']
        transitions = a1['transitions'] + a2['transitions']
        transitions += [(s_start, a1['start'], 'λ'), (s_start, a2['start'], 'λ')]
        finals = a1['finals'] + a2['finals']
        return {
            'states': states,
            'start': s_start,
            'finals': finals,
            'transitions': transitions
        }

    if typ == 'concat':
        a1 = build_automata(tree[1])
        a2 = build_automata(tree[2])
        states = a1['states'] + a2['states']
        transitions = a1['transitions'] + a2['transitions']
        for f in a1['finals']:
            transitions.append((f, a2['start'], 'λ'))
        return {
            'states': states,
            'start': a1['start'],
            'finals': a2['finals'],
            'transitions': transitions
        }

    if typ == 'star':
        a = build_automata(tree[1])
        s_start = State()
        states = [s_start] + a['states']
        transitions = list(a['transitions'])
        transitions.append((s_start, a['start'], 'λ'))
        for f in a['finals']:
            transitions.append((f, a['start'], 'λ'))
            transitions.append((f, s_start, 'λ'))
        return {
            'states': states,
            'start': s_start,
            'finals': [s_start],
            'transitions': transitions
        }