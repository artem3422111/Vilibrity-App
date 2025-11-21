import turtle

# Настройка окна turtle
screen = turtle.Screen()
screen.setup(800, 800)
screen.setworldcoordinates(-10, -10, 10, 110)  # x: -10 до 10, y: -10 до 110
screen.bgcolor("white")
screen.title("Парабола y = x²")

# Создаем черепашку для рисования
t = turtle.Turtle()
t.speed(0)  # Максимальная скорость
t.color("blue")
t.pensize(2)

# Рисуем оси координат
t.penup()
t.goto(-10, 0)
t.pendown()
t.goto(10, 0)  # Ось X
t.penup()
t.goto(0, -10)
t.pendown()
t.goto(0, 110)  # Ось Y

# Подписываем оси
t.penup()
t.goto(9.5, -1)
t.write("X", font=("Arial", 12, "normal"))
t.goto(-0.5, 105)
t.write("Y", font=("Arial", 12, "normal"))

# Рисуем параболу y = x²
t.penup()
t.color("red")
t.pensize(3)

# Перебираем точки с шагом 0.01
step = 0.01
x = -10
first_point = True

while x <= 10:
    y = x**2  # Формула параболы
    
    if first_point:
        t.goto(x, y)
        t.pendown()
        first_point = False
    else:
        t.goto(x, y)
    
    x += step

# Подписываем график
t.penup()
t.goto(-3, 90)
t.color("red")
t.write("y = x²", font=("Arial", 16, "bold"))

# Добавляем сетку
grid = turtle.Turtle()
grid.speed(0)
grid.color("lightgray")
grid.pensize(1)

# Вертикальные линии сетки
for i in range(-10, 11, 2):
    grid.penup()
    grid.goto(i, -10)
    grid.pendown()
    grid.goto(i, 110)

# Горизонтальные линии сетки
for i in range(-10, 111, 10):
    grid.penup()
    grid.goto(-10, i)
    grid.pendown()
    grid.goto(10, i)

grid.hideturtle()

# Скрываем черепашку
t.hideturtle()

# Завершаем программу при клике
screen.exitonclick()