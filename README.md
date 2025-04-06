![Python](https://img.shields.io/badge/python-3.9+-blue)
![PyQt5](https://img.shields.io/badge/library-PyQt5-yellow)

# 🔌 Logic Gate Circuit Editor - PyQt5 Project

A graphical logic gate circuit editor built using PyQt5. This interactive GUI application allows users to drag and drop logic gates onto a canvas, connect them to form digital circuits, and visually design logical structures. This project is perfect for students, beginners in GUI programming, or anyone curious about how to visualize digital logic.

---

## ✨ Features

- 🧱 Drag-and-drop support for basic logic gates: `AND`, `OR`, `NOT`, `XOR`, `XNOR`, `NAND`, `NOR`, `Input`, and `Output`.
- 🔗 Click-to-connect functionality to simulate wire connections between logic gates.
- 🗂️ Multi-tab interface for working on multiple circuits in the same session.
- 📁 File Menu with options: New, Open, Save, and Exit.
- 🎨 Clean and user-friendly layout with sidebar + canvas workspace.
- 🎯 Visually appealing, responsive graphics using `QGraphicsView`.

---

## 🧰 Technologies Used

| Language | Library         | Purpose                                                                 |
|----------|------------------|-------------------------------------------------------------------------|
| Python   | PyQt5            | GUI and graphics framework for building interactive apps               |
| QtCore   | PyQt5.QtCore     | Handling drag-and-drop events, item movement, positions                 |
| QtWidgets| PyQt5.QtWidgets  | Core widgets like `QListWidget`, `QMainWindow`, `QTabWidget`, etc.      |
| QtGui    | PyQt5.QtGui      | Used for `QPainter`, `QPen`, and `QDrag` for drawing and interaction    |

---

## 🛠️ How to Run the Project

1. Make sure you have Python installed (Python 3.6 or later).
2. Install PyQt5 if it's not already installed:
   ```bash
   pip install PyQt5
   Run the application using:
   python logic_gate_editor.py

   ## 📘 Learn More / Documentation

If you’re new to PyQt5 or GUI development, here are some beginner-friendly references:

- 🧠 [PyQt5 Official Documentation](https://doc.qt.io/qtforpython/)
- 📘 [Real Python – Introduction to PyQt](https://realpython.com/python-pyqt-gui-calculator/)
- 🎥 [YouTube – PyQt5 Beginner Tutorial (FreeCodeCamp)](https://www.youtube.com/playlist?list=PLzMcBGfZo4-lB8MZfHPLTEHO9zJDDLpYj)
- ✏️ [GeeksForGeeks – PyQt5 Basics](https://www.geeksforgeeks.org/pyqt5-tutorial/)
