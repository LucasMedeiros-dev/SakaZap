import sys
from PySide6 import QtWidgets
from user_tab import UsersTab
from message_tab import MessagesTab
from file_selector import FileSelectorWindow


class Aplicativo(QtWidgets.QMainWindow):
    def update_message(self, message):
        # Update the message
        self.message = message

        # Update the UI to reflect the new message
        self.text_box.setText(self.message)

    def __init__(self, arquivo):
        super().__init__()

        self.arquivo = arquivo

        self.setFixedSize(500, 400)
        texto = self._inicializar_storage()

        self.tabWidget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabWidget)

        self.messagesTab = MessagesTab()
        # Set the text in the message tab
        self.messagesTab.text_box.setText(texto)
        # Connect the clicked signal of the save button to the updateUsersTab function
        self.messagesTab.button.clicked.connect(self.updateUsersTab)

        self.usersTab = UsersTab(arquivo, texto)
        users = self.tabWidget.addTab(self.usersTab, "Clientes")
        messages = self.tabWidget.addTab(self.messagesTab, "Mensagem")

    def _inicializar_storage(self):
        try:
            f = open("confs.cfg", "r+", encoding="utf-8")
            return f.read()
        except FileNotFoundError:
            f = open("confs.cfg", "w+", encoding="utf-8")
            return ""

    def updateUsersTab(self):
        # Get the current message
        texto = self.messagesTab.text_box.toPlainText()

        # Remove the current UsersTab
        self.tabWidget.removeTab(0)

        # Create a new UsersTab with the updated message
        self.usersTab = UsersTab(self.arquivo, texto)

        # Add the new UsersTab to the QTabWidget
        self.tabWidget.insertTab(0, self.usersTab, "Clientes")


class MainApp(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.file_selector = FileSelectorWindow()
        self.file_selector.file_selected.connect(self.load_main_app)
        self.file_selector.show()

    def load_main_app(self, file_name):
        try:
            self.file_selector.close()
            self.aplicativo = Aplicativo(file_name)
            self.aplicativo.show()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.file_selector.show()


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec())
