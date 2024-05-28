import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QScrollArea, QFileDialog
from PyQt6.QtGui import QPainter, QPaintEvent, QFont
from PyQt6.QtCore import Qt, QFile

class Estudiante:
    def __init__(self, id, nombre, carrera):
        self.id = id
        self.nombre = nombre
        self.carrera = carrera

class Nodo:
    def __init__(self, estudiante):
        self.estudiante = estudiante
        self.izquierda = None
        self.derecha = None

class ArbolBusqueda:
    def __init__(self):
        self.raiz = None

    def insertar(self, estudiante):
        if self.raiz is None:
            self.raiz = Nodo(estudiante)
        else:
            self._insertar_recursivo(self.raiz, estudiante)

    def _insertar_recursivo(self, nodo, estudiante):
        if estudiante.id < nodo.estudiante.id:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(estudiante)
            else:
                self._insertar_recursivo(nodo.izquierda, estudiante)
        elif estudiante.id > nodo.estudiante.id:
            if nodo.derecha is None:
                nodo.derecha = Nodo(estudiante)
            else:
                self._insertar_recursivo(nodo.derecha, estudiante)

    def eliminar(self, id):
        self.raiz = self._eliminar_recursivo(self.raiz, id)

    def _eliminar_recursivo(self, nodo, id):
        if nodo is None:
            return nodo

        if id < nodo.estudiante.id:
            nodo.izquierda = self._eliminar_recursivo(nodo.izquierda, id)
        elif id > nodo.estudiante.id:
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, id)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda

            nodo.estudiante = self._encontrar_minimo(nodo.derecha).estudiante
            nodo.derecha = self._eliminar_recursivo(nodo.derecha, nodo.estudiante.id)

        return nodo

    def _encontrar_minimo(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    def buscar(self, id):
        return self._buscar_recursivo(self.raiz, id)

    def _buscar_recursivo(self, nodo, id):
        if nodo is None:
            return None
        if nodo.estudiante.id == id:
            return nodo.estudiante
        if id < nodo.estudiante.id:
            return self._buscar_recursivo(nodo.izquierda, id)
        return self._buscar_recursivo(nodo.derecha, id)

    def listar_estudiantes(self):
        estudiantes = []
        self._inorden(self.raiz, estudiantes)
        return estudiantes

    def _inorden(self, nodo, estudiantes):
        if nodo:
            self._inorden(nodo.izquierda, estudiantes)
            estudiantes.append(nodo.estudiante)
            self._inorden(nodo.derecha, estudiantes)

    def obtener_info(self):
        info = {
            "Tamaño": self.obtener_tamanio(),
            "Niveles": self.obtener_niveles(),
            "Balanceado": self.es_balanceado()
        }
        return info

    def obtener_tamanio(self):
        return self._obtener_tamanio_recursivo(self.raiz)

    def _obtener_tamanio_recursivo(self, nodo):
        if nodo is None:
            return 0
        return 1 + self._obtener_tamanio_recursivo(nodo.izquierda) + self._obtener_tamanio_recursivo(nodo.derecha)

    def obtener_niveles(self):
        return self._obtener_niveles_recursivo(self.raiz)

    def _obtener_niveles_recursivo(self, nodo):
        if nodo is None:
            return 0
        return max(self._obtener_niveles_recursivo(nodo.izquierda), self._obtener_niveles_recursivo(nodo.derecha)) + 1

    def es_balanceado(self):
        return self._es_balanceado_recursivo(self.raiz)

    def _es_balanceado_recursivo(self, nodo):
        if nodo is None:
            return True
        altura_izquierda = self._obtener_niveles_recursivo(nodo.izquierda)
        altura_derecha = self._obtener_niveles_recursivo(nodo.derecha)
        if abs(altura_izquierda - altura_derecha) <= 1:
            return self._es_balanceado_recursivo(nodo.izquierda) and self._es_balanceado_recursivo(nodo.derecha)
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz de Árbol Binario")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.arbol = ArbolBusqueda()

        self.label = QLabel("ID:")
        self.layout.addWidget(self.label)

        self.input_text = QLineEdit()
        self.layout.addWidget(self.input_text)

        self.label_nombre = QLabel("Nombre:")
        self.layout.addWidget(self.label_nombre)

        self.input_nombre = QLineEdit()
        self.layout.addWidget(self.input_nombre)

        self.label_carrera = QLabel("Carrera:")
        self.layout.addWidget(self.label_carrera)

        self.input_carrera = QLineEdit()
        self.layout.addWidget(self.input_carrera)

        self.insertar_button = QPushButton("Agregar Estudiante")
        self.insertar_button.clicked.connect(self.insertar_valor)
        self.layout.addWidget(self.insertar_button)

        self.eliminar_button = QPushButton("Eliminar Estudiante")
        self.eliminar_button.clicked.connect(self.eliminar_valor)
        self.layout.addWidget(self.eliminar_button)

        self.buscar_button = QPushButton("Buscar Estudiante")
        self.buscar_button.clicked.connect(self.buscar_valor)
        self.layout.addWidget(self.buscar_button)

        self.listar_button = QPushButton("Listar Estudiantes")
        self.listar_button.clicked.connect(self.listar_estudiantes)
        self.layout.addWidget(self.listar_button)

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.layout.addWidget(self.info_text)

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.layout.addWidget(self.scroll_area)

        self.visualizacion_widget = VisualizacionWidget()
        self.scroll_area.setWidget(self.visualizacion_widget)

        self.actualizar_visualizacion()

        # Agregar botones para guardar y cargar
        self.guardar_button = QPushButton("Guardar")
        self.guardar_button.clicked.connect(self.guardar_archivo)
        self.layout.addWidget(self.guardar_button)

        self.cargar_button = QPushButton("Cargar")
        self.cargar_button.clicked.connect(self.cargar_archivo)
        self.layout.addWidget(self.cargar_button)

    def insertar_valor(self):
        try:
            id = int(self.input_text.text())
            nombre = self.input_nombre.text()
            carrera = self.input_carrera.text()
            estudiante = Estudiante(id, nombre, carrera)
            self.arbol.insertar(estudiante)
            self.actualizar_info()
            self.actualizar_visualizacion()
        except ValueError:
            self.info_text.append("Ingrese un ID válido.")

    def eliminar_valor(self):
        try:
            id = int(self.input_text.text())
            self.arbol.eliminar(id)
            self.actualizar_info()
            self.actualizar_visualizacion()
        except ValueError:
            self.info_text.append("Ingrese un ID válido.")

    def buscar_valor(self):
        try:
            id = int(self.input_text.text())
            estudiante = self.arbol.buscar(id)
            if estudiante:
                mensaje = f"Estudiante encontrado - ID: {estudiante.id}, Nombre: {estudiante.nombre}, Carrera: {estudiante.carrera}"
            else:
                mensaje = f"Estudiante con ID {id} no encontrado."
            self.info_text.append(mensaje)
        except ValueError:
            self.info_text.append("Ingrese un ID válido.")

    def listar_estudiantes(self):
        estudiantes = self.arbol.listar_estudiantes()
        self.info_text.clear()
        for est in estudiantes:
            self.info_text.append(f"ID: {est.id}, Nombre: {est.nombre}, Carrera: {est.carrera}")
        self.guardar_lista_estudiantes(estudiantes)

    def actualizar_info(self):
        info = self.arbol.obtener_info()
        self.info_text.clear()
        for clave, valor in info.items():
            self.info_text.append(f"{clave}: {valor}")

    def actualizar_visualizacion(self):
        self.visualizacion_widget.actualizar_arbol(self.arbol.raiz)

    def guardar_arbol(self, nodo, file):
        if nodo:
            file.write(f"{nodo.estudiante.id},{nodo.estudiante.nombre},{nodo.estudiante.carrera}\n")
            self.guardar_arbol(nodo.izquierda, file)
            self.guardar_arbol(nodo.derecha, file)
        else:
            file.write("None\n")

    def guardar_archivo(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "Archivos de Texto (*.txt)")

        if filename:
            with open(filename, 'w') as file:
                file.write("Árbol Binario:\n")
                self.guardar_arbol(self.arbol.raiz, file)

    def cargar_archivo(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Cargar Archivo", "", "Archivos de Texto (*.txt)")

        if filename:
            with open(filename, 'r') as file:
                self.arbol.raiz = self.cargar_arbol(file)
                self.actualizar_visualizacion()

    def cargar_arbol(self, file):
        linea = file.readline().strip()
        if linea == "Árbol Binario:":
            linea = file.readline().strip()
        return self.cargar_nodo(linea, file)

    def cargar_nodo(self, linea, file):
        if linea == "None":
            return None
        datos = linea.split(',')
        estudiante = Estudiante(int(datos[0]), datos[1], datos[2])
        nodo = Nodo(estudiante)
        nodo.izquierda = self.cargar_nodo(file.readline().strip(), file)
        nodo.derecha = self.cargar_nodo(file.readline().strip(), file)
        return nodo

    def guardar_lista_estudiantes(self, estudiantes):
        filename, _ = QFileDialog.getSaveFileName(self, "Guardar Lista", "", "Archivos de Texto (*.txt)")
        if filename:
            with open(filename, 'w') as file:
                for est in estudiantes:
                    file.write(f"ID: {est.id}, Nombre: {est.nombre}, Carrera: {est.carrera}\n")

class VisualizacionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.arbol = None

    def actualizar_arbol(self, raiz):
        self.arbol = raiz
        self.update()

    def paintEvent(self, event):
        if self.arbol:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.dibujar_arbol(painter, self.arbol, 200, 50, 0)

    def dibujar_arbol(self, painter, nodo, x, y, nivel):
        if nodo:
            painter.drawText(x - 15, y + 15, str(nodo.estudiante.id))

            separacion_horizontal = 80
            separacion_vertical = 50
            dx = separacion_horizontal * (2 ** (nivel + 1))
            dy = separacion_vertical

            if nodo.izquierda:
                x_izquierda = x - dx
                y_izquierda = y + dy
                painter.drawLine(x, y + 20, x_izquierda, y_izquierda + 20)
                self.dibujar_arbol(painter, nodo.izquierda, x_izquierda, y_izquierda, nivel + 1)

            if nodo.derecha:
                x_derecha = x + dx
                y_derecha = y + dy
                painter.drawLine(x, y + 20, x_derecha, y_derecha + 20)
                self.dibujar_arbol(painter, nodo.derecha, x_derecha, y_derecha, nivel + 1)

            self.setMinimumWidth(max(x + dx + 20, self.parent().width()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
