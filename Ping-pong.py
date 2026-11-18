import tkinter as tk
import random
from colorsys import hsv_to_rgb  # для красивого следа за мячом


W = 640  # ширина
H = 400  # высота поля
X1 = 40  # границы где стоят ракетки
X2 = W - 40  # линии где стоят ракетки
BOT = H - 40  # граница куда ракетка не заедет
CYAN = "#32ffc1"
PINK = "#ff4d6d"
ball = [W / 2, H / 2]  # координата мяча
vx, vy = 5, 3  # скорость мяча по горизонтали, вертикали
me = H / 2  # положение моей ракетки
ai = H / 2  # противоположная ракетка
move = 0  # куда я сейчас двигаюсь
score = [0, 0]  # счет игроков
trail = []  # список, где хранится след мяча


root = tk.Tk()
root.title("Пинг-понг")
c = tk.Canvas(root, bg="#0f1020", width=W,
              height=H, highlightthickness=0)
c.pack()


def color(i):  # делает перелив для хвоста мячика
    h = 0.5 + 0.3 * i / 12
    r, g, b = hsv_to_rgb(h, .7, 255)
    return "#%02x%02x%02x" % (int(r), int(g), int(b))


KEYS = {"Up": -8, "Down": 8}  # клавиши вверх и вниз


def press(e):  # запоминает какая клавиша нажата
    global move
    move = KEYS.get(e.keysym, 0)


def release(e):  # когда клавишу отпустили, останавливает ракетку
    global move
    move = 0


root.bind("<KeyPress>", press)  # подключение функций к клавиатуре
root.bind("<KeyRelease>", release)


def serve():  # функция ставит мяч в центр
    global vx, vy
    ball[0] = W / 2
    ball[1] = H / 2
    vx = random.choice([-5, 5])  # запускает его в случайную сторону
    vy = random.choice([-3, 3])


def circle(x, y, r, col):
    c.create_oval(
        x - r, y - r, x + r, y + r,  # рисует круг
        fill=col, outline="")


def bar(x, y, col):  # рисует ракетку с круглыми краями
    c.create_line(x, y - 40, x, y + 40,
                  fill=col, width=14, capstyle="round")


def label(x, y, t, col):  # пишет число
    c.create_text(x, y, text=t, fill=col, font=("Arial", 36, "bold"))


def draw():
    c.delete("all")  # стираем все
    c.create_line(W / 2, 10, W / 2, H - 10,
                  fill="#2a2d55", width=4, dash=(10, 14))

    for i, (x, y) in enumerate(trail):  # перебирает путь(хвост)
        r = 3 + i * 0.7
        circle(x, y, r, color(i))  # увеличивает след(хвост) от мячика

    x, y = ball
    circle(x, y, 10, "white")
    bar(30, me, CYAN)  # ракетка игрока
    bar(W - 30, ai, PINK)  # ракетка бота
    cx = W / 2
    label(cx - 60, 40, score[0], CYAN)  # счет
    label(cx + 60, 40, score[1], PINK)  # счет2


def hit(py):  # проверяет местоположение мяча рядом с ракеткой
    return abs(ball[1] - py) < 50


def step():  # главная функция, один кадр игры
    global vx, vy, me, ai
    # двигаем ракетку игрока, не дальше границы
    me = max(40, min(BOT, me + move))
    dy = ball[1] - ai  # бот едет за мячом
    ai += max(-5, min(5, dy))  # не быстрее 5 пикселей за кадр

    ball[0] += vx  # координаты мяча
    ball[1] += vy
    trail.append(tuple(ball))  # след

    del trail[:-12]  # храним только последние 12 точек хвоста
    bx, by = ball

    if by < 10 or by > H - 10:  # если мяч коснулся верней/нижней стены
        vy = -vy  # отскакивает
    # если летит влево и попал в мою ракетку
    if vx < 0 and bx < X1 and hit(me):
        # то он летит обратно и становится на 6% быстрее
        vx = min(-vx * 1.06, 12)
        vy = (by - me) / 6
    if vx > 0 and bx > X2 and hit(ai):
        vx = -min(vx * 1.06, 12)
        vy = (by - ai) / 6
    if bx < 0:  # если мяч улетел за левый край
        score[1] += 1  # очко боту
        serve()  # вызов функции, которая ставит мяч в центр
    if bx > W:  # если за правый
        score[0] += 1  # очко мне
        serve()  # вызов функции, которая ставит мяч в центр

    draw()
    root.after(16, step)  # запускаем следующий кадр за 16мс


step()
root.mainloop()
