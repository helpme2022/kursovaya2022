from collections import defaultdict
from tkinter import Tk, Button, scrolledtext


# Создание класса необходимого для основного функционала программы
class Bank:
    def __init__(self):
        self.clientsdict = defaultdict(int)

    # Функционал всех команд прописан именно здесь
    def deposit(self, name: str, money: int):
        self.clientsdict[name] += money

    def withdraw(self, name: str, money: int):
        self.clientsdict[name] -= money

    def balance(self, name: str):
        if name != "":
            return self.clientsdict.get(name, "NO CLIENT")
        else:
            return self.clientsdict.items()

    def transfer(self, name1: str, name2: str, money: int):
        self.clientsdict[name1] -= money
        self.clientsdict[name2] += money

    def income(self, p: int):
        for name in self.clientsdict:
            if self.clientsdict[name] > 0:
                self.clientsdict[name] = int(self.clientsdict[name] * (1 + p / 100))


bank_app = Bank()
student_id = 70167927
bank_app.deposit("Kolyadin", student_id)


def setup_tk():
    # В функции для обработки нажатия кнопки Calculate происходит проверка введенных команд
    def clicked_calculate():
        input_text = str(text.get(1.0, "end"))
        lbl_text = ""

        # Сначала из поля ввода текст делится на строки, после чего на отдельные слова
        for line in input_text.split('\n'):

            words = line.split(' ')

            if words[0] == "DEPOSIT":
                bank_app.deposit(words[1], int(words[2]))
            elif words[0] == "WITHDRAW":
                bank_app.withdraw(words[1], int(words[2]))

            elif words[0] == "BALANCE":
                # Проверка на ввод конкретного пользователя, либо отображаем баланс всех пользователей
                if len(words) > 1 and words[1] != '':
                    output_text = bank_app.balance(words[1])
                    lbl_text += words[1] + ' ' + str(output_text) + '\n'
                else:
                    data = bank_app.balance("")
                    output_text = ""
                    for key, value in data:
                        output_text += key + ' ' + str(value) + '\n'
                    lbl_text += output_text

            elif words[0] == "TRANSFER":
                bank_app.transfer(words[1], words[2], int(words[3]))
            elif words[0] == "INCOME":
                bank_app.income(int(words[1]))

        text_label.configure(state='normal')
        text_label.insert(1.0, lbl_text)
        text_label.configure(state='disabled')

    # Функция для кнопки Clear (очистка полей)
    def clicked_clear():
        text.delete(1.0, "end")

        text_label.configure(state='normal')
        text_label.delete(1.0, "end")
        text_label.configure(state='disabled')

    # Интерфейс Tkinter
    window = Tk()
    window.resizable(False, False)
    window.title("Exercise_2")
    window.geometry("640x320")

    text = scrolledtext.ScrolledText(window, width=35, height=10, borderwidth=1, relief="solid")
    text.place(x=15, y=20)
    text_label = scrolledtext.ScrolledText(window, width=35, height=10, borderwidth=1, relief="solid", state='disabled')
    text_label.place(x=330, y=20)

    calculate_btn = Button(window, text="Calculate", width=40, command=clicked_calculate)
    calculate_btn.place(x=170, y=220)
    clear_btn = Button(window, text="Clear", width=40, command=clicked_clear)
    clear_btn.place(x=170, y=260)

    window.mainloop()


setup_tk()
