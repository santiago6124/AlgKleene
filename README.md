# README.md

# Algoritmo de Kleene - Generador de Autómatas Finitos

Este proyecto implementa el **Algoritmo de Kleene**, que transforma expresiones regulares en autómatas finitos no deterministas (AFND) usando Python y los muestra gráficamente.

---

## 🚀 ¿Cómo funciona?

1. El usuario ingresa una **expresión regular** (por ejemplo, `(a+b)*c`).
2. El programa:
   - **Parsea** la expresión regular usando `lark` → convierte el texto en un árbol sintáctico.
   - **Construye el autómata** usando el algoritmo de Thompson (implementado a mano en Python).
   - **Genera la imagen del autómata** usando `graphviz`.
   - **Muestra la imagen en una interfaz gráfica** usando `tkinter` + `Pillow`.

---

## 📦 Requisitos

Antes de correrlo, instala las dependencias:

```bash
pip install lark graphviz pillow
```

Además:
- Descarga Graphviz desde [https://graphviz.gitlab.io/download/](https://graphviz.gitlab.io/download/)
- Asegúrate de que el ejecutable `dot` esté en tu PATH del sistema (Graphviz lo usa para renderizar los gráficos).

---

## 💻 Cómo ejecutarlo

```bash
python main.py
```

Se abrirá una ventana donde puedes:
1. Escribir tu expresión regular.
2. Presionar **Generar Autómata**.
3. Ver el autómata generado como imagen.

---

## 🔨 ¿Qué hacen las librerías?

- **Lark**
  - Parsea expresiones regulares (`ab+cd*`) en un árbol de operaciones (`union`, `concat`, `star`).
  - Permite transformar texto en estructuras que luego armamos en autómatas.
  - ¿Qué es LALR?
      LALR = Look-Ahead LR, es una técnica de análisis sintáctico descendente, usada por compiladores y herramientas de parsing como Yacc/Bison.

      LR significa que analiza de izquierda a derecha (L) y produce una derivación más a la derecha (R).
      
      El "A" de Look-Ahead significa que mira hacia adelante un token para tomar decisiones.
      
      Es eficiente y puede analizar muchas gramáticas comunes sin ambigüedad y sin consumir demasiada memoria.

- **Graphviz**
  - Crea y renderiza el grafo del autómata como archivo `.png`.
  - Los nodos representan estados; las aristas, transiciones.

- **Pillow (PIL)**
  - Carga y adapta la imagen `.png` del autómata para mostrarla en la interfaz.

- **Tkinter**
  - Proporciona la interfaz gráfica (ventana, entrada de texto, botón, canvas para imagen).

---

## 📚 Ejemplo de expresiones que puedes probar

- `a`
- `a+b`
- `ab`
- `(a+b)*c`
- `a*(b+c)`

---

## 🤓 Créditos

- Código escrito por: Santiago Carranza, Lorenzo Galaverna y Manuel Ferreras
- Basado en el algoritmo de Kleene
