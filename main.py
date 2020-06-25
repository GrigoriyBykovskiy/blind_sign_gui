import sys
import math
from PyQt5 import QtWidgets
from qt import MainWindowChaumSignature, SuccessWindowChaumSignature, ErrorWindowChaumSignature


def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def euler(n):
    r = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            r -= r // i
        else:
            i += 1
    if n > 1:
        r -= r // n
    return r


class ChaumSignature:
    def get_e(self):
        return self.e

    def set_e(self, e):
        self.e = e

    def get_d(self):
        return self.d

    def set_d(self, d):
        self.d = d

    def get_n(self):
        return self.n

    def set_n(self, n):
        self.n = n

    def get_r(self):
        return self.r

    def set_r(self, r):
        self.r = r

    # m'
    def get_hidden_message(self, message_to_hide):
        buf = pow(self.r, self.e)
        hidden_message = (message_to_hide * buf) % self.n
        # hidden_message = (message * (self.r ** self.e)) % self.n
        return hidden_message

    # s'
    def get_sign_message(self, message_to_sign):
        sign_message = pow(message_to_sign, self.d, self.n)
        return sign_message

    # s
    def get_sign(self, message_test, euler_n):
        reverse_r = 0
        gcd, x, y = gcdExtended(self.r, self.n)
        if gcd == 1:
            reverse_r = (x % euler_n + euler_n) % euler_n
            print(reverse_r)
        else:
            return (-1)
        sign = (message_test * reverse_r) % self.n
        return sign

    def check_sign(self, message_to_check):
        decrypt_message = pow(message_to_check, self.e, self.n)
        return decrypt_message

    def salting_message(self, message_to_salt, salt):
        return message_to_salt ^ salt

    def __init__(self):
        self.e = 0
        self.d = 0
        self.n = 0
        self.r = 0

class ChaumSignatureAppMain(QtWidgets.QMainWindow, MainWindowChaumSignature.Ui_MainWindow):
    def main(self):
        try:
            n = self.get_input_n()
            print(f"n is {n} \n")
            d = self.get_input_d()
            print(f"d is {d} \n")
            message = self.get_input_number()
            print(f"message is {message} \n")
            salt = self.get_input_salt()
            print(f"salt is {salt} \n")
            if n is None or d is None or message is None or salt is None:
                print("ANTA BAKA?! CHECK USER INPUT")
            else:
                euler_n = euler(n)
                e = 0
                r = 17
                gcd, x, y = gcdExtended(d, euler_n)
                if gcd == 1:
                    e = (x % euler_n + euler_n) % euler_n
                    print(f"Public key e is  {e} \n")
                    chaum = ChaumSignature()
                    chaum.set_e(e)
                    chaum.set_d(d)
                    chaum.set_n(n)
                    chaum.set_r(r)
                    self.successWindow.update_text(f"Исходное сообщение: {message} \n")
                    salting_message = chaum.salting_message(message, salt)  # message with salt
                    self.successWindow.update_text(f"Засоленное сообщение: {salting_message} \n")
                    hide_message = chaum.get_hidden_message(salting_message)  # message with salt and public key
                    self.successWindow.update_text(f"Засоленное сообщение после использования маскирующего множителя и открытого ключа: {hide_message} \n")
                    sign_message = chaum.get_sign_message(hide_message)  # sign message
                    self.successWindow.update_text(f"Подписанное сообщение: {sign_message} \n")
                    delete_hide_message = chaum.get_sign(sign_message, euler_n)  # reverse sign message
                    self.successWindow.update_text(f"Подпись: {delete_hide_message} \n")
                    check_sign = chaum.check_sign(delete_hide_message) ^ salt
                    self.successWindow.update_text(f"Проверка подписи, значение после проверки: {check_sign}\n")
                    if (check_sign == message):
                        self.successWindow.update_text("Подпись корректна")
                        self.successWindow.show()
                    else:
                        self.successWindow.update_text("Подпись не прошла проверку")
                        self.successWindow.show()
                else:
                    self.errorWindow.update_text("Что-то пошло не так ...")
                    self.errorWindow.show()
        except:
            self.errorWindow.update_text("Что-то пошло не так ...")
            self.errorWindow.show()


    def get_input_salt(self):
        try:
            text = self.plainTextEdit_5.toPlainText()
            return int(text)
        except:
            self.errorWindow.update_text("Неправильно введено значение соли")
            self.errorWindow.show()

    def get_input_number(self):
        try:
            text = self.plainTextEdit_4.toPlainText()
            return int(text)
        except:
            self.errorWindow.update_text("Неправильно введено числовое сообщение")
            self.errorWindow.show()

    def get_input_d(self):
        try:
            text = self.plainTextEdit_3.toPlainText()
            return int(text)
        except:
            self.errorWindow.update_text("Неправильно введено число d")
            self.errorWindow.show()

    def get_input_n(self):
        try:
            text = self.plainTextEdit_2.toPlainText()
            return int(text)
        except:
            self.errorWindow.update_text("Неправильно введено число n")
            self.errorWindow.show()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.errorWindow = ChaumSignatureError()
        self.successWindow = ChaumSignatureSuccess()
        self.pushButton.clicked.connect(self.main)


class ChaumSignatureSuccess(QtWidgets.QMainWindow, SuccessWindowChaumSignature.Ui_MainWindow):
    def exit(self):
        self.close()

    def update_text(self, text):
        self.plainTextEdit_5.appendPlainText(text)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.plainTextEdit_5.setReadOnly(True)
        self.pushButton.clicked.connect(self.exit)


class ChaumSignatureError(QtWidgets.QMainWindow, ErrorWindowChaumSignature.Ui_MainWindow):
    def exit(self):
        self.close()

    def update_text(self, text):
        #self.plainTextEdit_5.clear()
        self.plainTextEdit_5.appendPlainText(text)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.exit)


app = QtWidgets.QApplication(sys.argv)
app_main = ChaumSignatureAppMain()
app_main.show()
app.exec()


