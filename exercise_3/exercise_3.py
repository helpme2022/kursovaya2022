from pydoc import text
from tkinter import *
from math import sqrt, log1p, sin, pow


# Объявление класса калькулятора, который хранит все необходимые данные для работы
class Calculator:
    def __init__(self) -> None:
        self.text_current = "0"
        self.text_history = ""
        self.text_display = "0"
        self.small_mode = True
        self.prev = ""
        self.mcells = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, }
        self.value = 0
        self.history = ""
        self.type = "int"
        self.operation = None


# Нажатие на клавиши с числом
def digit(d: str):
    if calculate.text_current == "0":
        calculate.text_current = d
    else:
        calculate.text_current += d
    calculate.text_display = calculate.text_current
    lbl_current.configure(text=calculate.text_display)


# Ввод негативного числа
def make_negative():
    if calculate.text_display[0] != "0":
        if calculate.text_display[0] == "-":
            calculate.text_display = calculate.text_display[1::]
        else:
            calculate.text_display = "-" + calculate.text_display
        calculate.text_current = calculate.text_display
        lbl_current.configure(text=calculate.text_display)


# Очистка ввода
def click_clear_text():
    calculate.text_current = "0"
    calculate.operation = None
    calculate.text_history = ""
    calculate.text_display = "0"
    lbl_current.configure(text=calculate.text_display)
    lbl_history.configure(text=calculate.text_history)
    text.delete(1.0, END)


#  Сохранение значения в ячейку
def click_ms(memory_slot: int):
    if calculate.text_display[-1] != ".":
        calculate.mcells[memory_slot] = int(calculate.text_display)
        calculate.text_current = "0"
        lbl_current.configure(text=calculate.text_display)
    else:
        calculate.text_current = calculate.text_display
        click_backspace()
        click_memory_plus(memory_slot)


# Вывод значения из ячейки на экран
def click_mr(memory_slot: int):
    calculate.text_display = calculate.mcells[memory_slot]
    calculate.text_current = "0"
    lbl_current.configure(text=calculate.text_display)


# Очистка ячейки памяти
def click_mc(memory_slot: int):
    calculate.mcells[memory_slot] = 0


# Очистка памяти
def click_all_clear():
    click_clear_text()
    text.delete(1.0, END)
    for key in calculate.mcells:
        calculate.mcells[key] = 0


# Очистка ввода
def click_backspace():
    if len(calculate.text_current) > 0:
        if len(calculate.text_current) > 1:
            calculate.text_current = calculate.text_current[0:-1]
        else:
            calculate.text_current = "0"
        if calculate.text_current[0] == "-" and len(calculate.text_current) == 1:
            calculate.text_current = "0"
        if calculate.text_current[-1] == ".":
            calculate.text_current = calculate.text_current[0:-1]
    calculate.text_display = calculate.text_current
    lbl_current.configure(text=calculate.text_display)


# Далее идут функции самих операций, большинство из них сравнительно похожие
# Поэтому все комментарии из нижней функции могут быть распространены на остальные


def click_plus():
    # Проверяем если уже вводили операнд или же вводится ноль
    # calc.prev  записывает значение прошлой нажатой клавиши

    if calculate.operation == "+" and calculate.text_current == "0":
        calculate.text_display = calculate.prev
        pass
    elif calculate.operation != "+":
        calculate.operation = "+"
        calculate.prev = calculate.text_display
        calculate.text_current = "0"
        calculate.text_history = f"{calculate.text_display} + "
        lbl_history.configure(text=calculate.text_history)
    else:

    # Если число не целое то округяем полученное значение

        tmp = round(float(calculate.text_current) + float(calculate.prev), 3)
        if tmp % 1 == 0.0:
            calculate.text_display = str(int(tmp))
        else:
            calculate.text_display = str(tmp)
        calculate.prev = calculate.text_display
        calculate.text_history = f"{calculate.text_display} + "
        calculate.text_current = "0"
        lbl_history.configure(text=calculate.text_history)
        lbl_current.configure(text=calculate.text_display)


def click_minus():
    if calculate.operation == "-" and calculate.text_current == "0":
        calculate.text_display = calculate.prev
        pass
    elif calculate.operation != "-":
        calculate.operation = "-"
        calculate.prev = calculate.text_display
        calculate.text_current = "0"
        calculate.text_history = f"{calculate.text_display} - "
        lbl_history.configure(text=calculate.text_history)
    else:
        tmp = round(float(calculate.prev) - float(calculate.text_current), 3)
        if tmp % 1 == 0.0:
            calculate.text_display = str(int(tmp))
        else:
            calculate.text_display = str(tmp)
        calculate.prev = calculate.text_display
        calculate.text_history = f"{calculate.text_display} - "
        calculate.text_current = "0"
        lbl_history.configure(text=calculate.text_history)
        lbl_current.configure(text=calculate.text_display)


def clicked_multiply():
    if calculate.operation != "*":
        calculate.operation = "*"
        calculate.prev = calculate.text_display
        calculate.text_current = "0"
        calculate.text_history = f"{calculate.text_display} * "
        lbl_history.configure(text=calculate.text_history)
    else:
        tmp = round(float(calculate.prev) * float(calculate.text_current), 3)
        if tmp % 1 == 0.0:
            calculate.text_display = str(int(tmp))
        else:
            calculate.text_display = str(tmp)
        calculate.prev = calculate.text_display
        calculate.text_current = "0"
        calculate.text_history = f"{calculate.text_display} * "
        lbl_history.configure(text=calculate.text_history)
        lbl_current.configure(text=calculate.text_display)


def click_div():
    if calculate.operation == "/" and calculate.text_current == "0":
        calculate.text_display = calculate.prev
        lbl_current.configure(text="You can't divide by zero")

    elif calculate.operation != "/":
        calculate.operation = "/"
        calculate.prev = calculate.text_display
        calculate.text_current = "0"
        calculate.text_history = f"{calculate.text_display} / "
        lbl_history.configure(text=calculate.text_history)
    else:
        tmp = round(float(calculate.prev) / float(calculate.text_current), 3)
        if tmp % 1 == 0.0:
            calculate.text_display = str(int(tmp))
        else:
            calculate.text_display = str(tmp)
        calculate.prev = calculate.text_display
        calculate.text_current = "0"
        calculate.text_history = f"{calculate.text_display} / "
        lbl_history.configure(text=calculate.text_history)
        lbl_current.configure(text=calculate.text_display)


def click_mod():
    if calculate.operation == "%" and calculate.text_current == "0":
        calculate.text_display = calculate.prev
    elif calculate.operation != "%":
        calculate.operation = "%"
        calculate.prev = calculate.text_display
        calculate.text_current = "0"
        calculate.text_history = f"{calculate.text_display} % "
        lbl_history.configure(text=calculate.text_history)
    else:
        tmp = round(float(calculate.prev) % float(calculate.text_current), 3)
        if tmp % 1 == 0.0:
            calculate.text_display = str(int(tmp))
        else:
            calculate.text_display = str(tmp)
        calculate.prev = calculate.text_display
        calculate.text_current = "0"
        calculate.text_history = f"{calculate.text_display} % "
        lbl_history.configure(text=calculate.text_history)
        lbl_current.configure(text=calculate.text_display)


def click_pow():
    calculate.text_history += f"sqr{calculate.text_display}"
    tmp = round(float(calculate.text_display) ** 2, 3)
    if tmp % 1 == 0.0:
        calculate.text_display = str(int(tmp))
    else:
        calculate.text_display = str(tmp)
    calculate.text_current = calculate.text_display
    lbl_history.configure(text=calculate.text_history)
    lbl_current.configure(text=calculate.text_display)


def click_sqrt():
    calculate.text_history += f"sqrt{calculate.text_display}"
    tmp = round(sqrt(float(calculate.text_display)), 3)
    if tmp % 1 == 0.0:
        calculate.text_display = str(int(tmp))
    else:
        calculate.text_display = str(tmp)
    calculate.text_current = calculate.text_display
    lbl_history.configure(text=calculate.text_history)
    lbl_current.configure(text=calculate.text_display)


def click_equal():
    if calculate.operation is not None:
        template = calculate.text_current
        if calculate.operation == "+":
            click_plus()
        if calculate.operation == "-":
            click_minus()
        if calculate.operation == "*":
            clicked_multiply()
        if calculate.operation == "/":
            if calculate.text_current == "0":
                calculate.text_display = calculate.prev
                lbl_current.configure(text="You can't divide by zero")
                return
            else:
                click_div()
        if calculate.operation == "%":
            click_mod()
        if calculate.operation == "**":
            clicked_x_pow_y()

    # Проверка чтобы число выводилось корректно, не было результата подобному 0123

        if calculate.text_history[-1:-3:-1] != "0 ":
            calculate.text_history += f"{template}"
        calculate.text_current = template
        calculate.prev = calculate.text_display
        lbl_history.configure(text=calculate.text_history)
        lbl_current.configure(text=calculate.text_display)
    else:
        pass

    # Ячейки памяти являются элементами массива, с которыми и проходит работа
def click_memory_plus(m_slot: int):
    calculate.operation = "+"
    calculate.prev = calculate.text_display
    calculate.text_current = calculate.mcells[m_slot]
    click_plus()


def click_memory_min(m_slot: int):
    calculate.operation = "-"
    calculate.prev = calculate.text_display
    calculate.text_current = calculate.mcells[m_slot]
    click_minus()

# Для расширенного режима калькулятора мы расширяем окно
def click_extra():
    if calculate.small_mode:
        display.geometry("680x650")
        calculate.small_mode = False
    else:
        display.geometry("322x500")
        calculate.small_mode = True


def clicked_pow_three():
    calculate.text_history += f"{calculate.text_display}^3"
    tmp = round(float(calculate.text_display) ** 3, 3)
    if tmp % 1 == 0.0:
        calculate.text_display = str(int(tmp))
    else:
        calculate.text_display = str(tmp)
    calculate.text_current = calculate.text_display
    lbl_history.configure(text=calculate.text_history)
    lbl_current.configure(text=calculate.text_display)


def clicked_x_pow_y():
    if calculate.operation == "**" and calculate.text_current == "0":
        calculate.text_display = calculate.prev
        pass
    elif calculate.operation != "**":
        calculate.operation = "**"
        calculate.prev = calculate.text_display
        calculate.text_current = "0"
        calculate.text_history = f"{calculate.text_display} ** "
        lbl_history.configure(text=calculate.text_history)
    else:
        tmp = round(pow(float(calculate.prev), float(calculate.text_current)), 3)
        if tmp % 1 == 0.0:
            calculate.text_display = str(int(tmp))
        else:
            calculate.text_display = str(tmp)
        calculate.prev = calculate.text_display
        calculate.text_history = f"{calculate.text_display} ** "
        calculate.text_current = "0"
        lbl_history.configure(text=calculate.text_history)
        lbl_current.configure(text=calculate.text_display)


def clicked_ln():
    calculate.text_history += f"Ln{calculate.text_display}"
    tmp = round(log1p(float(calculate.text_display)), 3)
    if tmp % 1 == 0.0:
        calculate.text_display = str(int(tmp))
    else:
        calculate.text_display = str(tmp)
    calculate.text_current = calculate.text_display
    lbl_history.configure(text=calculate.text_history)
    lbl_current.configure(text=calculate.text_display)


def clicked_sin():
    calculate.text_history += f"sin{calculate.text_display}"
    tmp = round(sin(float(calculate.text_display)), 3)
    if tmp % 1 == 0.0:
        calculate.text_display = str(int(tmp))
    else:
        calculate.text_display = str(tmp)
    calculate.text_current = calculate.text_display
    lbl_history.configure(text=calculate.text_history)
    lbl_current.configure(text=calculate.text_display)


# Здесь идет обработка подсчет операций введенных в текстовом окне
# Именно здесь алгоритм схож с тем что был во втором задании
def clicked_display_result():
    ctext_window = str(text.get(1.0, END))
    text_el = ctext_window.split("\n")
    for i in range(0, len(text_el)):
        text_el[i] += f" {i}"
    delta = 1.1
    calculate.operation = None
    calculate.prev = 0
    for character in text_el:
        tmp = character.split(" ")
        if len(tmp) == 4:
            if tmp[1] == "+":
                calculate.prev = round(float(tmp[0]) + float(tmp[2]), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)
            elif tmp[1] == "-":
                calculate.prev = round(float(tmp[0]) - float(tmp[2]), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)
            elif tmp[1] == "/":
                if tmp[2] != "0":
                    calculate.prev = round(float(tmp[0]) / float(tmp[2]), 3)
                    if calculate.prev % 1 == 0.0:
                        calculate.prev = str(int(calculate.prev))
                    else:
                        calculate.prev = str(calculate.prev)
                else:
                    calculate.prev = "You can't divide by zero"

            elif tmp[1] == "%":
                calculate.prev = round(float(tmp[0]) % float(tmp[2]), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)
            elif tmp[1] == "**":
                calculate.prev = round(pow(float(tmp[0]), float(tmp[2])), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)
            elif tmp[1] == "^":
                calculate.prev = round(pow(float(tmp[0]), float(tmp[2])), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)
            elif tmp[1] == "*":
                calculate.prev = round(float(tmp[0]) * float(tmp[2]), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)

        elif len(tmp) == 3:
            if tmp[0] == "sqrt":
                calculate.prev = round(sqrt(float(tmp[1])), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)
            if tmp[0] == "Ln":
                calculate.prev = round(log1p(float(tmp[1])), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)
            if tmp[0] == "sin":
                calculate.prev = round(sin(float(tmp[1])), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)
            if tmp[0] == "sqr":
                calculate.prev = round(pow(float(tmp[1]), 2), 3)
                if calculate.prev % 1 == 0.0:
                    calculate.prev = str(int(calculate.prev))
                else:
                    calculate.prev = str(calculate.prev)
            if tmp[0] == "DMS":
                d = float(tmp[1])
                if d < 0:
                    calculate.prev = "input must be positive"
                else:
                    m = d % 1 * 60
                    ctext_window = m % 1 * 60
                    d = int(d)
                    ctext_window = int(ctext_window)
                    m = int(m)
                    calculate.prev = f"{d}°{m}'{ctext_window}\""

        elif tmp[0] == "=":
            calculate.prev = "\n" + calculate.prev + "\n"
            text.insert(int(tmp[1]) + delta, calculate.prev)
            calculate.prev = "0"
            calculate.text_show = "0"
            calculate.text_cur = "0"
            delta += 2.0
            pass


def clicked_dms():
    d = float(calculate.text_display)
    if d < 0:
        calculate.text_history = "input must be positive"
    else:
        calculate.text_history += f"DMS{calculate.text_display}"
        m = d % 1 * 60
        s = m % 1 * 60
        d = int(d)
        s = int(s)
        m = int(m)
        calculate.text_current = f"{d}°{m}'{s}\""
        lbl_history.configure(text=calculate.text_history)
        lbl_current.configure(text=f"{d}°{m}'{s}\"")
        calculate.text_current = "0"
        calculate.operation = None
        calculate.text_history = ""
        calculate.text_display = "0"

# Интерфейс калькулятора прописан здесь
calculate = Calculator()
display = Tk()
display.resizable(False, False)
display.title("Calculator")
display.geometry("322x500")

lbl_current = Label(
    display, width=24, text="0", anchor=E, font=("Arial", 18), foreground="black"
)
lbl_current.place(x=-25, y=55)
lbl_history = Label(
    display, width=24, text="", anchor=E, font=("Arial", 10), foreground="gray"
)
lbl_history.place(x=120, y=10)

button_negative = Button(
    display,
    text="+/-",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=make_negative,
)
button_negative.place(x=0, y=443)
digit_zero = Button(
    display,
    text="0",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("0"),
)
digit_zero.place(x=81, y=443)
digit_one = Button(
    display,
    text="1",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("1"),
)
digit_one.place(x=0, y=385)
digit_two = Button(
    display,
    text="2",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("2"),
)
digit_two.place(x=81, y=385)
digit_three = Button(
    display,
    text="3",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("3"),
)
digit_three.place(x=162, y=385)
plus_operand = Button(
    display,
    text="+",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_plus,
)
plus_operand.place(x=242, y=385)
digit_four = Button(
    display,
    text="4",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("4"),
)
digit_four.place(x=0, y=327)
digit_five = Button(
    display,
    text="5",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("5"),
)
digit_five.place(x=81, y=327)
digit_six = Button(
    display,
    text="6",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("6"),
)
digit_six.place(x=162, y=327)
btn_min = Button(
    display,
    text="-",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_minus,
)
btn_min.place(x=242, y=327)
digit_seven = Button(
    display,
    text="7",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("7"),
)
digit_seven.place(x=0, y=269)
digit_eight = Button(
    display,
    text="8",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("8"),
)
digit_eight.place(x=81, y=269)
digit_nine = Button(
    display,
    text="9",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("9"),
)
digit_nine.place(x=162, y=269)
button_float = Button(
    display,
    text=".",
    width=8,
    height=3,
    font=("Arial", 12),
    relief=FLAT,
    command=lambda: digit("."),
)
button_float.place(x=162, y=443)
button_equal = Button(
    display,
    text="=",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_equal,
)
button_equal.place(x=242, y=443)
button_multiply = Button(
    display,
    text="x",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=clicked_multiply,
)
button_multiply.place(x=242, y=269)
button_mod = Button(
    display,
    text="%",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_mod,
)
button_mod.place(x=0, y=211)
button_pow = Button(
    display,
    text="x^2",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_pow,
)
button_pow.place(x=81, y=211)
button_sqrt = Button(
    display,
    text="√x",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_sqrt,
)
button_sqrt.place(x=162, y=211)
button_div = Button(
    display,
    text="/",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_div,
)
button_div.place(x=242, y=211)
button_extra = Button(
    display,
    text="≡",
    width=8,
    height=3,
    background="red",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_extra,
)
button_extra.place(x=0, y=153)
button_ce = Button(
    display,
    text="CE",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_clear_text,
)
button_ce.place(x=81, y=153)
button_c = Button(
    display,
    text="C",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_all_clear,
)
button_c.place(x=162, y=153)
button_delete = Button(
    display,
    text="←",
    width=8,
    height=3,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=click_backspace,
)
button_delete.place(x=242, y=153)

button_pow_by_three = Button(
    display,
    text="x^3",
    width=8,
    height=4,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=clicked_pow_three,
)
button_pow_by_three.place(x=0, y=505)
button_x_pow_y = Button(
    display,
    text="x^y",
    width=8,
    height=4,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=clicked_x_pow_y,
)
button_x_pow_y.place(x=81, y=505)
button_ln = Button(
    display,
    text="Ln",
    width=8,
    height=4,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=clicked_ln,
)
button_ln.place(x=162, y=505)
button_sin = Button(
    display,
    text="sin",
    width=8,
    height=4,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=clicked_sin,
)
button_sin.place(x=242, y=505)
btn_display_DMS = Button(
    display,
    text="DMS",
    width=8,
    height=4,
    background="gray",
    foreground="white",
    font=("Arial", 12),
    relief=FLAT,
    command=clicked_dms,
)
btn_display_DMS.place(x=120, y=575)

btn_M0_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(0),
)
btn_M0_S.place(x=270, y=124)
btn_M0_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(0),
)
btn_M0_R.place(x=69, y=124)
btn_M0_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(0),
)
btn_M0_plus.place(x=138, y=124)
btn_M0_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(0),
)
btn_M0_min.place(x=210, y=124)
btn_M0_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(0),
)
btn_M0_C.place(x=0, y=124)
text = Text(
    display,
    width=43,
    height=12,
    bg="#2F4F4F",
    background="gray",
    foreground="white",
    borderwidth=3,
    relief="solid",
)
text.place(x=325, y=25)
btn_M1_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(1),
)
btn_M1_S.place(x=325, y=269)
btn_M1_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(1),
)
btn_M1_R.place(x=406, y=269)
btn_M1_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(1),
)
btn_M1_plus.place(x=487, y=269)
btn_M1_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(1),
)
btn_M1_min.place(x=560, y=269)
btn_M1_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(1),
)
btn_M1_C.place(x=640, y=269)
btn_M2_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(2),
)
btn_M2_S.place(x=325, y=308)
btn_M2_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(2),
)
btn_M2_R.place(x=406, y=308)
btn_M2_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(2),
)
btn_M2_plus.place(x=487, y=308)
btn_M2_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(2),
)
btn_M2_min.place(x=560, y=308)
btn_M2_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(2),
)
btn_M2_C.place(x=640, y=308)
btn_M3_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(3),
)
btn_M3_S.place(x=325, y=347)
btn_M3_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(3),
)
btn_M3_R.place(x=406, y=347)
btn_M3_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(3),
)
btn_M3_plus.place(x=487, y=347)
btn_M3_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(3),
)
btn_M3_min.place(x=560, y=347)
btn_M3_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(3),
)
btn_M3_C.place(x=640, y=347)
btn_M4_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(4),
)
btn_M4_S.place(x=325, y=386)
btn_M4_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(4),
)
btn_M4_R.place(x=406, y=386)
btn_M4_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(4),
)
btn_M4_plus.place(x=487, y=386)
btn_M4_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(4),
)
btn_M4_min.place(x=560, y=386)
btn_M4_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(4),
)
btn_M4_C.place(x=640, y=386)

btn_M5_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(5),
)
btn_M5_S.place(x=325, y=425)
btn_M5_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(5),
)
btn_M5_R.place(x=406, y=425)
btn_M5_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(5),
)
btn_M5_plus.place(x=487, y=425)
btn_M5_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(5),
)
btn_M5_min.place(x=560, y=425)
btn_M5_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(5),
)
btn_M5_C.place(x=640, y=425)
btn_M5_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(6),
)
btn_M5_S.place(x=325, y=463)

btn_M6_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(6),
)
btn_M6_R.place(x=406, y=463)
btn_M6_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(6),
)
btn_M6_plus.place(x=487, y=463)
btn_M6_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(6),
)
btn_M6_min.place(x=560, y=463)
btn_M6_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(6),
)
btn_M6_C.place(x=640, y=463)

btn_M7_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(7),
)
btn_M7_S.place(x=325, y=501)
btn_M7_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(7),
)
btn_M7_R.place(x=406, y=501)
btn_M7_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(7),
)
btn_M7_plus.place(x=487, y=501)
btn_M7_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(7),
)
btn_M7_min.place(x=560, y=501)
btn_M7_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(7),
)
btn_M7_C.place(x=640, y=501)

btn_M8_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(8),
)
btn_M8_S.place(x=325, y=539)
btn_M8_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(8),
)
btn_M8_R.place(x=406, y=539)
btn_M8_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(8),
)
btn_M8_plus.place(x=487, y=539)
btn_M8_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(8),
)
btn_M8_min.place(x=560, y=539)
btn_M8_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(8),
)
btn_M8_C.place(x=640, y=539)

btn_M9_S = Button(
    display,
    text="MS",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_ms(9),
)
btn_M9_S.place(x=325, y=577)
btn_M9_R = Button(
    display,
    text="MR",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mr(9),
)
btn_M9_R.place(x=406, y=577)
btn_M9_plus = Button(
    display,
    text="M+",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_plus(9),
)
btn_M9_plus.place(x=487, y=577)
btn_M9_min = Button(
    display,
    text="M-",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_memory_min(9),
)
btn_M9_min.place(x=560, y=577)
btn_M9_C = Button(
    display,
    text="MC",
    width=7,
    height=1,
    font=("Arial", 8),
    relief=FLAT,
    command=lambda: click_mc(9),
)
btn_M9_C.place(x=640, y=577)

btn_display_result = Button(
    display,
    text="Result",
    width=43,
    height=2,
    background="gray",
    foreground="white",
    font=("Arial", 8),
    relief=FLAT,
    command=clicked_display_result,
)
btn_display_result.place(x=375, y=225)

display.mainloop()
