from PySide6 import QtCore, QtWidgets
from datetime import datetime
from functools import partial
from urllib.parse import quote
from extras import buscar_nome_telefone
from openpyxl import load_workbook

# Import a Browser to open the WhatsApp Web
import webbrowser


class UsersTab(QtWidgets.QWidget):
    def __init__(self, arquivo, message):
        super().__init__()
        tupla_nomes_telefones = buscar_nome_telefone(arquivo)
        self.mensagem = message
        self.users_checkboxes = []

        main_layout = QtWidgets.QVBoxLayout(self)

        self.text = QtWidgets.QLabel(
            f"Aniversariantes do Dia de Hoje: {datetime.today().day}/{datetime.today().month}",
            alignment=QtCore.Qt.AlignLeft,
        )
        main_layout.addWidget(self.text)

        users_widget = QtWidgets.QWidget()
        users_layout = QtWidgets.QVBoxLayout(users_widget)

        self._gerar_campos_usuarios(tupla_nomes_telefones, users_layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(users_widget)
        main_layout.addWidget(scroll_area)

        report_button = QtWidgets.QPushButton("Gerar Relatório")
        report_button.clicked.connect(self.gerar_relatorio)
        main_layout.addWidget(report_button)

    def _gerar_campos_usuarios(self, users, layout):
        for dia, nome, primeiro_nome, telefone in users:
            if dia != datetime.today().day:
                continue

            user_layout = QtWidgets.QHBoxLayout()
            user_layout.addWidget(QtWidgets.QLabel(nome))

            user_button = QtWidgets.QPushButton("Enviar Mensagem")
            user_chkbox = QtWidgets.QCheckBox()
            user_chkbox.setDisabled(True)

            user_button.clicked.connect(
                partial(
                    self.enviar_mensagem, telefone, nome, primeiro_nome, user_chkbox
                )
            )

            user_layout.addStretch()
            user_layout.addWidget(user_button)
            user_layout.addWidget(user_chkbox)
            layout.addLayout(user_layout)

            self.users_checkboxes.append((nome, telefone, user_chkbox))

    def enviar_mensagem(self, telefone, nome, primeiro_nome, checkbox):
        texto = (
            self.mensagem.replace("NOMEPESSOA", primeiro_nome) if self.mensagem else ""
        )
        checkbox.setChecked(True)
        texto = quote(texto)
        url = f"https://web.whatsapp.com/send/?phone={telefone}&text={texto}"
        webbrowser.open(url)

    def gerar_relatorio(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Salvar Relatório",
            f"Relatório_Aniversariantes_Dia_{datetime.today().strftime('%d_%m_%Y')}.xlsx",
            "Arquivos Excel (*.xslx)",
        )[0]

        if filename:
            # Load the workbook
            workbook = load_workbook("template.xlsx")

            # Select the active sheet
            sheet = workbook.active

            # Write data to the sheet starting from C3, D3, E3
            row = 3
            for nome, telefone, checkbox in self.users_checkboxes:
                status = "SIM" if checkbox.isChecked() else "NÃO"
                dia = datetime.today().day
                sheet[f"B{row}"] = dia
                sheet[f"C{row}"] = nome
                sheet[f"D{row}"] = telefone
                sheet[f"E{row}"] = status
                sheet[f"G{row}"] = f"{nome[:3]}{telefone[8:11]}{dia}"
                row += 1

            # Save the workbook
            workbook.save(filename)
