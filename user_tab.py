from PySide6 import QtCore, QtWidgets
from datetime import datetime
from functools import partial
from urllib.parse import quote
from extras import buscar_nome_telefone

# Import a Browser to open the WhatsApp Web
import webbrowser


class UsersTab(QtWidgets.QWidget):
    def __init__(self, arquivo, message):
        super().__init__()
        tupla_nomes_telefones = buscar_nome_telefone(arquivo)
        self.mensagem = message
        self.users_checkboxes = []

        # Cria um QVBoxLayout para o widget principal
        main_layout = QtWidgets.QVBoxLayout(self)

        self.text = QtWidgets.QLabel(
            f"Aniversariantes do Dia de Hoje: {datetime.today().day}/{datetime.today().month}",
            alignment=QtCore.Qt.AlignLeft,
        )
        main_layout.addWidget(self.text)

        # Cria um widget para conter os usuários e botões
        users_widget = QtWidgets.QWidget()
        users_layout = QtWidgets.QVBoxLayout(users_widget)
        self._gerar_campos_usuarios(tupla_nomes_telefones, users_layout)

        # Cria uma QScrollArea e adiciona o widget de usuários a ela
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(users_widget)

        # Adiciona a QScrollArea ao layout principal
        main_layout.addWidget(scroll_area)

        # Cria um botão para gerar o relatório
        report_button = QtWidgets.QPushButton("Gerar Relatório")
        report_button.clicked.connect(self.gerar_relatorio)

        # Adiciona o botão ao layout principal
        main_layout.addWidget(report_button)

    def _gerar_campos_usuarios(self, users, layout):
        for dia, nome, primeiro_nome, telefone in users:
            if dia != datetime.today().day:
                continue
            # Cria um QHBoxLayout para cada usuário
            user_layout = QtWidgets.QHBoxLayout()

            # Adiciona o nome do usuário ao layout
            user_layout.addWidget(QtWidgets.QLabel(nome))

            # Cria um botão para o usuário
            user_button = QtWidgets.QPushButton("Enviar Mensagem")
            # Cria um checkbox para o usuário
            user_chkbox = QtWidgets.QCheckBox()
            user_chkbox.setDisabled(True)

            # Conecta o botão a função de enviar mensagem
            user_button.clicked.connect(
                partial(
                    self.enviar_mensagem, telefone, nome, primeiro_nome, user_chkbox
                )
            )

            # Adiciona um espaço ao final do layout
            user_layout.addStretch()

            # Adiciona o botão ao layout
            user_layout.addWidget(user_button)

            # Adiciona o checkbox ao layout
            user_layout.addWidget(user_chkbox)

            # Adiciona o layout do usuário ao layout principal
            layout.addLayout(user_layout)

            # Adiciona o nome e a checkbox à lista
            self.users_checkboxes.append((nome, user_chkbox))

    def enviar_mensagem(self, telefone, nome, primeiro_nome, checkbox):
        # Envia a mensagem para o usuário
        texto = self.mensagem
        # Marca a checkbox
        checkbox.setChecked(True)
        if texto:
            texto = texto.replace("NOMEPESSOA", primeiro_nome)

        texto = quote(texto)

        url = f"https://web.whatsapp.com/send/?phone={telefone}&text={texto}"
        webbrowser.open(url)

    def gerar_relatorio(self):
        # Cria um relatório com o nome e o estado de cada checkbox
        report = [
            (nome, checkbox.isChecked()) for nome, checkbox in self.users_checkboxes
        ]

        # Imprime o relatório
        for nome, is_checked in report:
            print(f"{nome}: {'Enviado' if is_checked else 'Não enviado'}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = UsersTab("Olá, NOMEPESSOA Eu sou o Goku")
    window.setFixedSize(600, 400)
    window.show()
    app.exec()
