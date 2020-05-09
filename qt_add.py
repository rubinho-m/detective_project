import sys

from random import shuffle
from PyQt5.QtWidgets import QApplication, QMainWindow
from qt_stories import Ui_MainWindow


END_STRING = '---'
FILENAME = "static/loaded/qt_detective.txt"


class Qt_stories(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.add.clicked.connect(self.add_to_file)
        self.deleteButton.clicked.connect(self.delete_dir)

    def add_to_file(self):
        try:
            title = self.textTitle.toPlainText()
            text = self.text.toPlainText()
            right_ans = self.textAnswer.toPlainText()
            spectator = self.textSpectator.toPlainText()
            opinion = self.textOpinion.toPlainText()
            api = self.textApi.toPlainText()
            proof = self.textProof.toPlainText()
            api_message = self.textApiMessage.toPlainText()
            variants = [right_ans, self.Ans1.toPlainText(), self.Ans2.toPlainText(),
                        self.Ans3.toPlainText(), self.Ans4.toPlainText()]

            if not api_message:
                api_message = 'None'

            shuffle(variants)
            variants = '_'.join(variants)

            file = '\n'.join([title, text, right_ans, spectator, opinion, api,
                    proof, api_message, variants, END_STRING])

            f = open(FILENAME, 'a+', encoding='utf-8')

            if f.tell() != 0:
                f.write('\n')

            f.write(file)
            f.close()
            print('История добавлена')

            f = open(FILENAME, 'r', encoding='utf-8')
            print(f.readlines()[-10:])
            f.close()

            self.textTitle.clear()
            self.text.clear()
            self.textAnswer.clear()
            self.textSpectator.clear()
            self.textOpinion.clear()
            self.textApi.clear()
            self.textProof.clear()
            self.textApiMessage.clear()
            self.Ans1.clear()
            self.Ans2.clear()
            self.Ans3.clear()
            self.Ans4.clear()
        except Exception as e:
            print(e)


    def delete_dir(self):
        f = open(FILENAME, 'w', encoding='utf-8')
        f.close()

        print('Содержимое удалено')


app = QApplication(sys.argv)
ex = Qt_stories()
ex.show()
sys.exit(app.exec_())