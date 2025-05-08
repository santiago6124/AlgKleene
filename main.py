# main.py
from lark import Lark, Transformer

grammar = """
?start: expr
?expr: expr "+" term   -> union
     | term
?term: term factor     -> concat
     | factor
?factor: base "*"       -> star
       | base "!"       -> repeat3
       | base
?base: "(" expr ")"
     | CHAR
CHAR: /[a-z]/ | "λ"
%ignore " "
"""

class RegexTransformer(Transformer):
    def union(self, items): return ('union', items[0], items[1])
    def concat(self, items): return ('concat', items[0], items[1])
    def star(self, items): return ('star', items[0])
    def repeat3(self, items): 
        e1 = items[0]
        return ('concat', e1, ('concat', e1, ('star', e1)))
    def CHAR(self, item): return str(item)

def parse_expression(regex):
    print("Parsing regex:", regex)
    parser = Lark(grammar, start='start', parser='lalr', transformer=RegexTransformer())
    result = parser.parse(regex)
    print("Parsed tree:", result)
    return result

class State:
    count = 0
    def __init__(self):
        self.id = State.count
        State.count += 1
    def __repr__(self):
        return f"S{self.id}"

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
        states = a['states'] + [s_start]
        transitions = a['transitions'][:]
        finals = a['finals'] + [s_start]
        for f in a['finals']:
            transitions.append((f, s_start, 'λ'))
        transitions.append((s_start, a['start'], 'λ'))
        return {
            'states': states,
            'start': s_start,
            'finals': finals,
            'transitions': transitions
        }
