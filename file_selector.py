import sys
from PySide6 import QtWidgets, QtCore


class FileSelectorWindow(QtWidgets.QWidget):
    file_selected = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        ## Set Size
        self.setFixedSize(500, 100)
        ## Set Title
        self.setWindowTitle("AutoZAP - Selecionar Arquivo")
        ## Set Layout
        self.layout = QtWidgets.QGridLayout(self)
        ## Create Widgets
        self.help_text = QtWidgets.QLabel("Selecione o arquivo que deseja acessar:")
        # Text Field
        self.text_field = QtWidgets.QLineEdit()
        self.text_field.setReadOnly(True)
        # Button
        self.button = QtWidgets.QPushButton("Abrir Arquivo")
        # Info Text
        self.info_text = QtWidgets.QLabel("Nenhum arquivo selecionado.")

        ## Add Widgets to Layout
        self.layout.addWidget(self.help_text, 0, 0)
        self.layout.addWidget(self.text_field, 1, 0)
        self.layout.addWidget(self.button, 1, 1)
        self.layout.addWidget(self.info_text, 2, 0)

        self.button.clicked.connect(self.open_file)

    def open_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Selecione o arquivo", "", "Arquivos Excel (*.xlsx)"
        )

        if file_name.endswith(".xlsx"):
            self.text_field.setText(file_name)
            self.info_text.setText(f"Arquivo Carregado com Sucesso!")
            self.file_selected.emit(file_name)
        else:
            self.info_text.setText("Por Favor Selecione um Arquivo Excel (.xlsx)")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FileSelectorWindow()
    window.show()
    sys.exit(app.exec())
