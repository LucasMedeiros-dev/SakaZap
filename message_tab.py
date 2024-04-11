from PySide6 import QtCore, QtWidgets


class MessagesTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.text = QtWidgets.QLabel(
            "Editar Mensagem a Ser Enviada.", alignment=QtCore.Qt.AlignLeft
        )

        self.text_box = QtWidgets.QTextEdit()
        self.text_box.setStyleSheet("background-color: #d3d3d3; color: #000000;")
        self.text_box.setPlaceholderText("Digite sua mensagem aqui...")

        layout.addWidget(self.text)
        layout.addWidget(self.text_box)

        self.button = QtWidgets.QPushButton("Salvar Mensagem")
        layout.addWidget(self.button)

        self.button.clicked.connect(self.salvar_mensagem)

    def salvar_mensagem(self):
        with open("confs.cfg", "w", encoding="utf-8") as f:
            f.write(self.text_box.toPlainText())
        self.text_box.setText(self.text_box.toPlainText())
        self.text.setText("Mensagem Salva com Sucesso!")
