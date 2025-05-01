# main.py
# automata_visualizer.py
import graphviz
# automata_parser.py
from lark import Lark, Transformer
import tkinter as tk
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

# automata_builder.py
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

# automata_visualizer.py


def visualize(automata):
    dot = graphviz.Digraph()
    for s in automata['states']:
        shape = 'doublecircle' if s == automata['end'] else 'circle'
        dot.node(str(s.id), shape=shape)
    for s1, s2, label in automata['transitions']:
        dot.edge(str(s1.id), str(s2.id), label)
    dot.render('automata_output', view=True)




def main():
    print("\n--- Algoritmo de Kleene para Expresiones Regulares ---\n")
    regex_input = input("Ingrese la expresión regular (ejemplo: (ab+ba)): ")
    try:
        parsed_expr = parse_expression(regex_input)
        print(f"Expresión parseada exitosamente: {parsed_expr}")
    except Exception as e:
        print(f"Error al parsear la expresión regular: {e}")
        return
    try:
        automata = build_automata(parsed_expr)
        print("Autómata generado correctamente.")
    except Exception as e:
        print(f"Error al generar el autómata: {e}")
        return
    try:
        visualize(automata)
        print("Visualización generada correctamente.")
    except Exception as e:
        print(f"Error en la visualización: {e}")
        print("\n👉 Solución sugerida: Asegúrate de tener Graphviz instalado y que el ejecutable 'dot' esté en tu PATH del sistema.")
        print("Descarga Graphviz desde: https://graphviz.gitlab.io/download/")

if __name__ == "__main__":
    main()


def run_algorithm():
    regex_input = entry.get()
    try:
        parsed_expr = parse_expression(regex_input)
        status_label.config(text="✔️ Expresión parseada exitosamente")
        automata = build_automata(parsed_expr)
        visualize(automata)
        status_label.config(text="✔️ Visualización generada correctamente")
    except Exception as e:
        status_label.config(text=f"❌ Error: {e}")

root = tk.Tk()
root.title("Algoritmo de Kleene")
root.geometry("400x200")

label = tk.Label(root, text="Ingrese expresión regular:")
label.pack(pady=10)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

run_button = tk.Button(root, text="Generar Autómata", command=run_algorithm)
run_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()
