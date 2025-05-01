# main.py
from lark import Lark, Transformer

# --- Parser ---
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

class RegexTransformer(Transformer):
    def union(self, items): return ('union', items[0], items[1])
    def concat(self, items): return ('concat', items[0], items[1])
    def star(self, items): return ('star', items[0])
    def CHAR(self, item): return str(item)

def parse_expression(regex):
    parser = Lark(grammar, start='start', parser='lalr', transformer=RegexTransformer())
    return parser.parse(regex)

class State:
    count = 0
    def __init__(self):
        self.id = State.count
        State.count +=1

def build_automata(tree):
    if isinstance(tree, str):
        s1, s2 = State(), State()
        return {'states':[s1,s2], 'start':s1, 'end':s2, 'transitions':[(s1,s2,tree)]}
    typ = tree[0]
    if typ == 'union':
        a1 = build_automata(tree[1])
        a2 = build_automata(tree[2])
        s_start, s_end = State(), State()
        transitions = a1['transitions'] + a2['transitions']
        transitions += [(s_start,a1['start'],'λ'), (s_start,a2['start'],'λ'), (a1['end'],s_end,'λ'), (a2['end'],s_end,'λ')]
        states = a1['states'] + a2['states'] + [s_start, s_end]
        return {'states':states, 'start':s_start, 'end':s_end, 'transitions':transitions}
    if typ == 'concat':
        a1 = build_automata(tree[1])
        a2 = build_automata(tree[2])
        transitions = a1['transitions'] + a2['transitions'] + [(a1['end'],a2['start'],'λ')]
        states = a1['states'] + a2['states']
        return {'states':states, 'start':a1['start'], 'end':a2['end'], 'transitions':transitions}
    if typ == 'star':
        a = build_automata(tree[1])
        s_start, s_end = State(), State()
        transitions = a['transitions']
        transitions += [(s_start,a['start'],'λ'), (a['end'],a['start'],'λ'), (a['end'],s_end,'λ'), (s_start,s_end,'λ')]
        states = a['states'] + [s_start, s_end]
        return {'states':states, 'start':s_start, 'end':s_end, 'transitions':transitions}

