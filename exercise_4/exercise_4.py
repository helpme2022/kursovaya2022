import random
from collections import defaultdict
from tkinter import Tk, Entry, Button, Canvas, messagebox, Label
from copy import deepcopy
from enum import Enum
import time

# Объявление констант
ANIMATION_TOTAL_MOVES = 1
ANIMATION_DURATION_LENGTH = 60
RISING_UP_Y = 200
DISK_HEIGHT = 10
DISPLAY_EVERY_N_SEC = 1
CHECK_EVERY = 5e5
PIVOT_X = 125
PIVOT_Y = 500


class TKState:
    def __init__(self):
        pass


tkState = TKState()

# Состояние анимации
class AnimationState(Enum):
    GO_UP = 0
    GO_SIDEWAYS = 1
    GO_DOWN = 2


# Сглаживание анимации
def linear(a, b, percent):
    return a + (b - a) * percent


#
class Animation:
    def __init__(self, disk, x, y, dx, dy):
        self.stage = AnimationState.GO_UP
        self.progress = 0
        self.partial = False
        self.disk = disk
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def tick(self):
        self.progress += 1
        if (
            self.partial
            and self.stage == AnimationState.GO_SIDEWAYS
            and self.progress >= ANIMATION_DURATION_LENGTH / 2
        ):
            return True
        if self.progress >= ANIMATION_DURATION_LENGTH:
            self.progress = 0
            if self.stage == AnimationState.GO_DOWN:
                return True
            self.stage = AnimationState(self.stage.value + 1)
        return False

    def percent(self):
        return self.progress / ANIMATION_DURATION_LENGTH

    def get_current_placement(self):
        if self.stage == AnimationState.GO_SIDEWAYS:
            x = linear(self.x, self.dx, self.percent())
        elif self.stage == AnimationState.GO_UP:
            x = self.x
        else:
            x = self.dx
        if self.stage == AnimationState.GO_UP:
            y = linear(self.y, RISING_UP_Y, self.percent())
        elif self.stage == AnimationState.GO_SIDEWAYS:
            y = RISING_UP_Y
        else:
            y = linear(RISING_UP_Y, self.dy, self.percent())
        return x, y

    def draw(self, canvas):
        x, y = self.get_current_placement()
        self.disk.draw(canvas, x, y)


class Disk:
    def __init__(self):
        self.size = 0
        self.color = ""

    def add_size(self, m: int, n: int):
        self.size = m * 10 + n

    def color_gen(self, used_colors: defaultdict):
        self.color = generate_colors(used_colors)

    def draw(self, canvas, x, y):
        canvas.create_rectangle(
            x - self.size / 2,
            y,
            x + self.size / 2,
            y + DISK_HEIGHT,
            outline="",
            fill=self.color,
        )
        canvas.create_text(x, y + 6, text=str(self.size))


class Step:
    def __init__(self) -> None:
        self.count = 0


def turn_to_hex(a: int):
    result = ""
    arr = ["a", "b", "c", "d", "e", "f"]
    while a // 16 + a % 16 != 0:
        tmp = a % 16
        a //= 16
        if tmp < 10:
            result = str(tmp) + result
        else:
            tmp -= 10
            result = arr[tmp] + result
    if len(result) == 1:
        result = "0" + result
    return result


def generate_colors(colors: defaultdict):
    r = random.randint(3, 255)
    g = random.randint(3, 255)
    b = random.randint(3, 255)
    color = "#" + turn_to_hex(r) + turn_to_hex(g) + turn_to_hex(b)
    if color in colors:
        return generate_colors(colors)
    else:
        colors[color]
        return color


def id_parsing(id: str):
    return list(map(int, id))[::-1]


def Tower(id):
    towers = [[] for _ in range(9)]
    disk_array = id_parsing(id)
    used_colors = defaultdict(int)

    for i in range(8, 0, -1):
        for j in range(disk_array[i - 1]):
            tmp = Disk()
            tmp.color_gen(used_colors)
            tmp.add_size(9 - i, j + 1)
            towers[i].append(tmp)
        towers[i] = towers[i][::-1]
    return towers


# Отрисовка текущего состояния башен
def draw_frame(canvas, tower, animation):
    canvas.delete("all")
    # Отрисовка основания башен
    canvas.create_line(PIVOT_X, PIVOT_Y - 5, PIVOT_X + 800, PIVOT_Y - 5, width=20)
    canvas.create_line(PIVOT_X + 50, PIVOT_Y, PIVOT_X + 50, PIVOT_Y - 350, width=3)
    canvas.create_line(PIVOT_X + 150, PIVOT_Y, PIVOT_X + 150, PIVOT_Y - 350, width=3)
    canvas.create_line(PIVOT_X + 250, PIVOT_Y, PIVOT_X + 250, PIVOT_Y - 350, width=3)
    canvas.create_line(PIVOT_X + 350, PIVOT_Y, PIVOT_X + 350, PIVOT_Y - 350, width=3)
    canvas.create_line(PIVOT_X + 450, PIVOT_Y, PIVOT_X + 450, PIVOT_Y - 350, width=3)
    canvas.create_line(PIVOT_X + 550, PIVOT_Y, PIVOT_X + 550, PIVOT_Y - 350, width=3)
    canvas.create_line(PIVOT_X + 650, PIVOT_Y, PIVOT_X + 650, PIVOT_Y - 350, width=3)
    canvas.create_line(PIVOT_X + 750, PIVOT_Y, PIVOT_X + 750, PIVOT_Y - 350, width=3)

    # Отрисовка дисков
    for i in range(8, 0, -1):
        cnt = 0
        y = PIVOT_Y - 15
        for j in tower[i]:
            j.draw(canvas, PIVOT_X + 50 + 100 * (8 - i), y - DISK_HEIGHT * (cnt + 1))
            cnt += 1

    if animation is not None:
        animation.draw(canvas)
    canvas.update()


display_number = 0
last_display_time = 0

# Функция simple_towers реализует алгоритм Ханойских башен
# n - количество дисков, start - начальный стержень, finish - конечный стержень, sum_rods - сумма номеров стержней
# tower - список стержней, cnt - объект класса Cnt для подсчета количества ходов
# canvas - объект Canvas для отрисовки графики, stop - список точек останова для записи результатов
# results - словарь для сохранения результатов на определенных шагах, если record_iterations=True
def simple_towers(
    n: int,
    start: int,
    finish: int,
    sum_rods: int,
    tower: list,
    step: Step,
    canvas,
    stop,
    results,
):
    global display_number, last_display_time
    # Если количество дисков меньше или равно 0, то выходим из функции
    if n <= 0:
        return
    # Определяем промежуточный стержень
    middle = sum_rods - start - finish

    # Вызываем рекурсию для n-1 диска и перемещаем его на промежуточный стержень
    simple_towers(n - 1, start, middle, sum_rods, tower, step, canvas, stop, results)
    # Увеличиваем счетчик ходов
    step.count += 1
    # Перемещаем верхний диск со стартового стержня на конечный стержень
    tower[finish].append(tower[start][-1])
    tower[start].pop(-1)
    # Увеличиваем счетчик отображения результатов
    display_number += 1
    # Если достигнуто CHECK_EVERY ходов, то отображаем результаты на экране
    if display_number >= CHECK_EVERY:
        if time.time() - last_display_time >= DISPLAY_EVERY_N_SEC:
            draw_frame(canvas, tower, None)
            last_display_time = time.time()
        display_number = 0

    # Если record_iterations=True и текущий ход находится в списке точек остановки,
    # то сохраняем результаты в словарь results
    for stopPoint in stop:
        if stopPoint - ANIMATION_TOTAL_MOVES <= step.count <= stopPoint:
            results[stopPoint].append(
                (deepcopy(tower), start, finish, tower[finish][-1])
            )
    # Вызываем рекурсию для прошлого диска и перемещаем его с промежуточного стержня на конечный стержень
    simple_towers(n - 1, middle, finish, sum_rods, tower, step, canvas, stop, results)


# Функция start_hanoi запускает алгоритм программы для каждого стержня
# theight - список стержней, cnt - объект класса Cnt для подсчета количества ходов,
# canvas - объект Canvas для отрисовки графики,
# record_iterations - флаг для сохранения результатов на определенных шагах в словарь results


def start_hanoi(theight: list, cnt, canvas, record_iterations):
    stop = []
    results = None
    # Если record_iterations=True, то определяем список точек останова и создаем пустой словарь c результатами
    # для записи в последующих рекурсиях
    if record_iterations:
        stop = tkState.stop
        results = defaultdict(list)
    # Запускаем алгоритм Ханойских башен для самого высокого стержня (8)
    length = len(theight[8])
    simple_towers(length, 8, 7, 21, theight, cnt, canvas, stop, results)
    # Запускаем алгоритм Ханойских башен для оставшихся стержней в порядке убывания (7-3)
    for i in range(7, 2, -1):
        length = len(theight[i])
        simple_towers(length, i, i - 1, 3 * i, theight, cnt, canvas, stop, results)
    length = len(theight[2])
    # Запускаем алгоритм Ханойских башен для промежуточного стержня (2)
    simple_towers(length, 2, 1, 6, theight, cnt, canvas, stop, results)
    # Отображаем результаты на экране и возвращаем словарь results (если он был создан)
    draw_frame(canvas, theight, None)

    return results

    # Функция для отрисовки текущего состояния башен Ханойского города
    # и анимации перемещения дисков
    # canvas - объект canvas, на котором происходит отрисовка
    # towerlist - словарь, содержащий списки дисков на каждой башне
    # partial_anim - проверяет нужно ли отрисовывать только часть анимации


def draw_animation(canvas, towerList, partial_anim):
    for i in range(0, len(towerList)):
        curTower, start, finish, disk = towerList[i]
        curTower = deepcopy(curTower)
        curTower[finish].pop(-1)
        if partial_anim and i + 1 == len(towerList):
            animation = Animation(
                disk,
                PIVOT_X + 50 * (8 - start),
                PIVOT_Y - DISK_HEIGHT * (len(curTower[start]) + 1),
                PIVOT_X + 50 + 100 * (8 - finish),
                PIVOT_Y - DISK_HEIGHT * (len(curTower[finish]) + 1),
            )
            animation.partial = True
        else:
            animation = Animation(
                disk,
                PIVOT_X + 50 + 100 * (8 - start),
                PIVOT_Y - DISK_HEIGHT * (len(curTower[start]) + 1),
                PIVOT_X + 50 + 100 * (8 - finish),
                PIVOT_Y - DISK_HEIGHT * (len(curTower[finish]) + 1),
            )
        while True:
            # Отрисовываем все кадры анимации
            draw_frame(canvas, curTower, animation)
            if animation.tick():
                curTower[finish].append(disk)
                if not animation.partial:
                    draw_frame(canvas, curTower, None)
                break


def setup_tk():
    def tk_start():
        student_id = ""
        for elements in full_id:
            student_id += elements.get()
        if not student_id.isnumeric() or len(student_id) != 8:
            messagebox.showerror("Error", "id введен неправильно")
            return

        tkState.stop = []
        tkState.isPartial = []

        tkState.percentage = []
        for elements in full_id:
            text = elements.get()
            if len(text) != 2:
                messagebox.showerror("Error", "Не верное значение в ячейке")
                return
            tkState.percentage.append(int(text))

        btn_start["state"] = "disabled"
        for elements in full_id:
            elements["state"] = "disabled"

        tkState.tower = Tower(student_id)
        tkState.cnt = Step()
        start_hanoi(deepcopy(tkState.tower), tkState.cnt, canvas, False)

        for p in tkState.percentage:
            isPartial = not (tkState.cnt.count / 100 * p).is_integer()
            it = tkState.cnt.count // 100 * p + isPartial
            tkState.stop.append(it)
            tkState.isPartial.append(isPartial)
        tkState.stop.append(tkState.cnt.count)
        tkState.isPartial.append(False)

        tkState.results = start_hanoi(deepcopy(tkState.tower), Step(), canvas, True)
        iteration_count["text"] = str(tkState.cnt.count) + " итераций"

        for button in sbuttons:
            button["state"] = "normal"

    def tk_draw_animation(stop_index):
        if stop_index >= len(tkState.percentage):
            iteration_count["text"] = str(tkState.cnt.count) + " итераций"
        else:
            p = tkState.percentage[stop_index]
            iteration_count["text"] = (
                str(round(tkState.cnt.count / 100 * p, 3)) + " итераций"
            )

        for button in sbuttons:
            button["state"] = "disabled"
        draw_animation(
            canvas,
            tkState.results[tkState.stop[stop_index]],
            tkState.isPartial[stop_index],
        )
        for button in sbuttons:
            button["state"] = "normal"

    window = Tk()
    window.title("Ханойские Башни")
    window.geometry("1280x800")
    window.resizable(False, False)

    btn_start = Button(window, text="Начало", command=tk_start)
    btn_start.place(x=PIVOT_X + 80, y=PIVOT_Y + 200)

    btn_p1 = Button(
        window, text="Итерация 1", command=lambda: tk_draw_animation(0)
    )
    btn_p1.place(x=PIVOT_X + 250, y=PIVOT_Y + 200)
    btn_p1["state"] = "disabled"
    btn_p2 = Button(
        window, text="Итерация 2", command=lambda: tk_draw_animation(1)
    )
    btn_p2.place(x=PIVOT_X + 420, y=PIVOT_Y + 200)
    btn_p2["state"] = "disabled"
    btn_p3 = Button(
        window, text="Итерация 3", command=lambda: tk_draw_animation(2)
    )
    btn_p3.place(x=PIVOT_X + 590, y=PIVOT_Y + 200)
    btn_p3["state"] = "disabled"
    btn_p4 = Button(
        window, text="Промежуточная итерация 4", command=lambda: tk_draw_animation(3)
    )
    btn_p4.place(x=PIVOT_X + 760, y=PIVOT_Y + 200)
    btn_p4["state"] = "disabled"

    btn_end = Button(window, text="Окончание", command=lambda: tk_draw_animation(4))
    btn_end.place(x=PIVOT_X + 160, y=PIVOT_Y + 200)
    btn_end["state"] = "disabled"

    sbuttons = [btn_p1, btn_p2, btn_p3, btn_p4, btn_end]

    iteration_count = Label(window)
    iteration_count.place(x=640, y=760)

    text1 = Entry(window)
    text1.place(x=PIVOT_X + 105, y=PIVOT_Y + 170, width=20)
    text2 = Entry(window)
    text2.place(x=PIVOT_X + 130, y=PIVOT_Y + 170, width=20)
    text3 = Entry(window)
    text3.place(x=PIVOT_X + 155, y=PIVOT_Y + 170, width=20)
    text4 = Entry(window)
    text4.place(x=PIVOT_X + 180, y=PIVOT_Y + 170, width=20)
    full_id = [text1, text2, text3, text4]
    canvas = Canvas(window, height=500, width=1000)
    canvas.pack()
    return window


window = setup_tk()

window.mainloop()


