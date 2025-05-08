import threading
from PIL import Image, ImageTk
import time
import graphviz
import tkinter as tk

from main import build_automata, parse_expression

def visualize(automata):
    dot = graphviz.Digraph()
    for s in automata['states']:
        dot.node(str(s.id), shape='doublecircle' if s in automata['finals'] else 'circle')
    for s1, s2, label in automata['transitions']:
        dot.edge(str(s1.id), str(s2.id), label)
    dot.render('automata_output', format='png')

def visualize_step_by_step(automata, canvas, status_label, delay):
    dot = graphviz.Digraph()
    for s in automata['states']:
        dot.node(str(s.id), shape='circle')
    dot.render('automata_step', format='png')
    for s in automata['states']:
        dot.node(str(s.id), shape='doublecircle' if s in automata['finals'] else 'circle')
        dot.render('automata_step', format='png')
        update_canvas(canvas, 'automata_step.png')
        status_label.config(text=f"✔️ Estado {s.id}")
        time.sleep(delay)
    for s1, s2, label in automata['transitions']:
        dot.edge(str(s1.id), str(s2.id), label)
        dot.render('automata_step', format='png')
        update_canvas(canvas, 'automata_step.png')
        status_label.config(text=f"✔️ Transición {s1.id} → {s2.id}")
        time.sleep(delay)

def update_canvas(canvas, img_path):
    img = Image.open(img_path)
    img_tk = ImageTk.PhotoImage(img)
    canvas.image = img_tk
    canvas.delete('all')
    canvas.create_image(canvas.winfo_width()//2, canvas.winfo_height()//2, anchor='center', image=img_tk)
    canvas.config(scrollregion=canvas.bbox('all'))

def run_step_by_step():
    regex_input = entry.get()
    delay = 1.0 - speed_scale.get() / 100
    def task():
        try:
            parsed_expr = parse_expression(regex_input)
            automata = build_automata(parsed_expr)
            visualize_step_by_step(automata, canvas, status_label, delay)
        except Exception as e:
            status_label.config(text=f"❌ Error: {e}")
    threading.Thread(target=task).start()

def run_instant():
    regex_input = entry.get()
    def task():
        try:
            parsed_expr = parse_expression(regex_input)
            automata = build_automata(parsed_expr)
            visualize(automata)
            update_canvas(canvas, 'automata_output.png')
            status_label.config(text="✔️ Autómata generado instantáneamente")
        except Exception as e:
            status_label.config(text=f"❌ Error: {e}")
    threading.Thread(target=task).start()

root = tk.Tk()
root.title("Algoritmo de Kleene")
root.geometry("900x700")
root.configure(bg='#f0f0f0')

label = tk.Label(root, text="Ingrese expresión regular:", font=('Arial', 12), bg='#f0f0f0')
label.pack(pady=5)

entry = tk.Entry(root, width=50, font=('Arial', 12))
entry.pack(pady=5)

frame_buttons = tk.Frame(root, bg='#f0f0f0')
frame_buttons.pack(pady=5)

instant_button = tk.Button(frame_buttons, text="Generar Instantáneo", font=('Arial', 12), bg='#4CAF50', fg='white', command=run_instant)
instant_button.pack(side='left', padx=10)

step_button = tk.Button(frame_buttons, text="Generar Paso a Paso", font=('Arial', 12), bg='#2196F3', fg='white', command=run_step_by_step)
step_button.pack(side='left', padx=10)

speed_scale = tk.Scale(root, from_=0, to=100, orient='horizontal', label='Velocidad de Animación', bg='#f0f0f0')
speed_scale.set(50)
speed_scale.pack(pady=5)

frame_canvas = tk.Frame(root)
frame_canvas.pack(fill='both', expand=True, padx=10, pady=10)

canvas = tk.Canvas(frame_canvas, bg='white')
scrollbar_y = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
scrollbar_x = tk.Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview)
canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
scrollbar_y.pack(side="right", fill="y")
scrollbar_x.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)

status_label = tk.Label(root, text="", font=('Arial', 11), bg='#f0f0f0')
status_label.pack(pady=5)

root.mainloop()
