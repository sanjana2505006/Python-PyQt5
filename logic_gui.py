from PyQt5.QtCore import Qt, QMimeData, QPointF
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QTabWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem,
    QListWidgetItem, QGraphicsLineItem
)
from PyQt5.QtGui import QPainter, QDrag, QPen
import sys


# ---------- Step 1A: Draggable Side Panel ----------
class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(item.text())
            drag.setMimeData(mime_data)
            drag.exec_(Qt.CopyAction)


# ---------- Custom Block with Connection Points ----------
class LogicGateBlock(QGraphicsRectItem):
    def __init__(self, gate_type, editor):
        super().__init__(0, 0, 100, 60)
        self.setBrush(Qt.white)
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.gate_type = gate_type
        self.editor = editor
        self.label = QGraphicsTextItem(gate_type, self)
        self.label.setDefaultTextColor(Qt.black)
        self.label.setPos(25, 20)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.editor.start_connection(self)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.editor.end_connection(self)
        super().mouseReleaseEvent(event)


class DropCanvas(QGraphicsView):
    def __init__(self, scene, editor):
        super().__init__(scene)
        self.editor = editor
        self.setAcceptDrops(True)
        self.setRenderHint(QPainter.Antialiasing)
        self.setStyleSheet("background-color: #fefefe; border: 1px solid #aaa;")

    def dragEnterEvent(self, event):
        print("🔵 dragEnterEvent triggered")
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            print("❌ No text in mimeData!")

    def dropEvent(self, event):
        print("🟢 dropEvent triggered")
        gate_type = event.mimeData().text()
        position = self.mapToScene(event.pos())
        print(f"📍 Dropped gate type: {gate_type} at position: {position}")
        self.editor.add_gate_node(gate_type, position)


# ---------- Logic Gate Editor ----------
class LogicGateEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.connection_start = None  # Track connection start block

    def init_ui(self):
        layout = QHBoxLayout()

        self.side_panel = DraggableListWidget()
        self.side_panel.addItems(["Input", "Output", "AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"])
        self.side_panel.setFixedWidth(150)

        self.scene = QGraphicsScene()
        self.canvas = DropCanvas(self.scene, self)
        self.canvas.setMinimumSize(600, 400)

        layout.addWidget(self.side_panel)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def add_gate_node(self, gate_type, position=None):
        block = LogicGateBlock(gate_type, self)
        self.scene.addItem(block)

        if position:
            block.setPos(position)
        else:
            block.setPos(100, 100)

    def start_connection(self, block):
        self.connection_start = block

    def end_connection(self, block):
        if self.connection_start and self.connection_start != block:
            start_pos = self.connection_start.sceneBoundingRect().center()
            end_pos = block.sceneBoundingRect().center()
            line = QGraphicsLineItem(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y())
            pen = QPen(Qt.black, 2)
            line.setPen(pen)
            self.scene.addItem(line)
        self.connection_start = None


# ---------- Logic Gate Node ----------
class LogicGateNode:
    def __init__(self, gate_type):
        self.gate_type = gate_type
        self.inputs = []
        self.output = None

    def compute_output(self):
        if self.gate_type == "AND":
            self.output = all(self.inputs)
        elif self.gate_type == "OR":
            self.output = any(self.inputs)
        elif self.gate_type == "NOT":
            if len(self.inputs) == 1:
                self.output = not self.inputs[0]
            else:
                self.output = None
        elif self.gate_type == "NAND":
            self.output = not all(self.inputs)
        elif self.gate_type == "NOR":
            self.output = not any(self.inputs)
        elif self.gate_type == "XOR":
            self.output = self.inputs.count(True) == 1
        elif self.gate_type == "XNOR":
            self.output = self.inputs.count(True) != 1
        elif self.gate_type == "Input":
            self.output = self.inputs[0] if self.inputs else None
        elif self.gate_type == "Output":
            self.output = self.inputs[0] if self.inputs else None
        else:
            self.output = None


# ---------- Main Window ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logic Gate Node Editor")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.create_menus()
        self.new_tab()

    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        new_action.triggered.connect(self.new_tab)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)

        edit_menu = menubar.addMenu("Edit")
        for action_name in ["Undo", "Redo", "Cut", "Copy", "Paste", "Delete"]:
            edit_menu.addAction(QAction(action_name, self))

        window_menu = menubar.addMenu("Window")
        theme_action = QAction("Change Theme", self)
        window_menu.addAction(theme_action)

    def new_tab(self):
        editor = LogicGateEditor()
        self.tabs.addTab(editor, f"New Circuit {self.tabs.count() + 1}")

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Circuit File", "", "Text Files (*.txt)")
        if file_name:
            print(f"Opened: {file_name}")

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Circuit File", "", "Text Files (*.txt)")
        if file_name:
            print(f"Saved: {file_name}")


# ---------- Run the App ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())