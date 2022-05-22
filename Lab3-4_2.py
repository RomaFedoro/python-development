# Семинар 2. №17-18

from math import acos, degrees
from pylab import show, scatter, plot

MODE_LIST = [('Добавить фигуру', 'add'),
             ('Удалить фигуру', 'del'),
             ('Переместить фигуру', 'move'),
             ('Проверить пересечение фигур', 'intersect'),
             ('Проверить включение фигур', 'include'),
             ('Показать фигуру', 'show'),
             ('Выйти', 'exit')
             ]
figures = []
BLUE_COLOR = '#4169e1'
RED_COLOR = '#E32636'


def area(vec1, vec2, vec3):
    return (vec2[0] - vec1[0]) * (vec3[1] - vec1[1]) - (vec2[1] - vec1[1]) * (vec3[0] - vec1[0])


def intersect_1(a, b, c, d):
    if a > b:
        a, b = b, a
    if c > d:
        c, d = d, c
    return max(a, c) <= min(b, d)


def intersect(pt1, pt2, pt3, pt4):
    return intersect_1(pt1[0], pt2[0], pt3[0], pt4[0]) \
           and intersect_1(pt1[1], pt2[1], pt3[1], pt4[1]) \
           and area(pt1, pt2, pt3) * area(pt1, pt2, pt4) <= 0 \
           and area(pt3, pt4, pt1) * area(pt3, pt4, pt2) <= 0


class Factory:
    @staticmethod
    def add_figure():
        print("1. Трехугольник")
        print("2. Четырехугольник")

        item = Menu.select_item(2)
        new_figure = None
        if item == 0:
            new_figure = Triangle()
        elif item == 1:
            new_figure = Tetragon()
        figures.append(new_figure)
        print("Фигура добавлена")

    @staticmethod
    def output_figures(*args):
        for i, fig in enumerate(figures):
            print("{}. {}".format(i + 1, fig))
        return Menu.select_item(len(figures), *args)

    def del_figure(self):
        if len(figures):
            print("Какую фигуру удалить?")
            del figures[self.output_figures()]
            print("Фигура удалена")
        else:
            print("Нет элементов")

    def move_figure(self):
        if len(figures):
            print("Какую фигуру переместить?")
            fig = figures[self.output_figures()]
            fig.draw(BLUE_COLOR)
            while True:
                try:
                    coord = tuple(map(float, input('Введите координаты перемещения: ').split()))
                    if len(coord) == 2:
                        break
                except ValueError:
                    print("Ошибка при вводе")
            fig.move(*coord)
            fig.draw(RED_COLOR)
            show()
            print("Фигура перемещена на {}".format(coord))
        else:
            print("Нет элементов")

    def is_intersect(self):
        if len(figures):
            print("Проверка пересечения двух фигур:")
            fig1 = figures[self.output_figures('первую фигуру')]
            coords1 = fig1.get_coords()
            fig2 = figures[self.output_figures('вторую фигуру')]
            coords2 = fig2.get_coords()
            fig1.draw(BLUE_COLOR)
            fig2.draw(RED_COLOR)
            show()
            for i in range(len(coords1)):
                point1 = coords1[i % len(coords1)]
                point2 = coords1[(i + 1) % len(coords1)]
                for j in range(len(coords2)):
                    point3 = coords2[j % len(coords2)]
                    point4 = coords2[(j + 1) % len(coords2)]
                    if intersect(point1, point2, point3, point4):
                        print('{} пересекается с {}'.format(fig2, fig1))
                        return True
            print('{} не пересекается с {}'.format(fig2, fig1))
            return False

        else:
            print("Нет элементов")

    def is_include(self):
        if len(figures):
            print("Проверка включения второй фигуры в первую:")
            fig1 = figures[self.output_figures('первую фигуру')]
            fig2 = figures[self.output_figures('вторую фигуру')]
            fig1.draw(BLUE_COLOR)
            fig2.draw(RED_COLOR)
            show()
            for coord in fig2.get_coords():
                if not fig1.is_inside(*coord):
                    print('{} не включен в {}'.format(fig2, fig1))
                    return False
            print('{} включен в {}'.format(fig2, fig1))
            return True
        else:
            print("Нет элементов")

    def show_figure(self):
        if len(figures):
            print("Какую фигуру показать?")
            figures[self.output_figures()].draw()
            show()
        else:
            print("Нет элементов")


class Vector:
    def __init__(self, start, end):
        self.x = end[0] - start[0]
        self.y = end[1] - start[1]

    def __str__(self):
        return '({} {})'.format(self.x, self.y)

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def angle(self, vec2):
        cos_angle = (self.x * vec2.x + self.y * vec2.y) / (self.length() * vec2.length())
        return degrees(acos(cos_angle))


class Figure:
    def __init__(self, corners):
        self.coordinates = []

        i = 0
        print("Введите координаты вершин последовательно:")
        while i < corners:
            try:
                coord = tuple(map(float, input().split()))
                if len(coord) == 2:
                    self.coordinates.append(coord)
                    i += 1
            except ValueError:
                print("Ошибка при вводе")

    def __str__(self, type_figure="Фигура"):
        return '{} c вершинами {}'.format(
            type_figure, ', '.join(map(str, self.coordinates)))

    def get_coords(self):
        return self.coordinates

    def draw(self, color='#0a0b0c'):
        x, y = [], []
        num_coords = len(self.coordinates)
        for i in range(num_coords + 1):
            x.append(self.coordinates[i % num_coords][0])
            y.append(self.coordinates[i % num_coords][1])
        plot(x, y, '-', color=color)
        scatter(x, y, c=color)

    def move(self, x, y):
        new_coordinates = []
        for coord in self.coordinates:
            new_coord = (coord[0] + x, coord[1] + y)
            new_coordinates.append(new_coord)
        self.coordinates = new_coordinates[:]

    def is_inside(self, x, y):
        sum_angle = 0
        point = (x, y)
        num_vertices = len(self.coordinates)
        for vertice in self.coordinates:
            if vertice == point:
                return True
        for i in range(num_vertices):
            vec1 = self.coordinates[i % num_vertices]
            vec1 = Vector(point, vec1)
            vec2 = self.coordinates[(i + 1) % num_vertices]
            vec2 = Vector(point, vec2)
            sum_angle += vec1.angle(vec2)
        if abs(sum_angle) == 360:
            return True
        return False


class Triangle(Figure):
    def __init__(self):
        Figure.__init__(self, 3)

    def __str__(self, **kwargs):
        return Figure.__str__(self, 'Треугольник')


class Tetragon(Figure):
    def __init__(self):
        Figure.__init__(self, 4)

    def __str__(self, **kwargs):
        return Figure.__str__(self, 'Четырехугольник')


class Menu:
    def __init__(self):
        pass

    @staticmethod
    def select_item(n_item, type_input='команду') -> int:
        while True:
            try:
                item = (input(f"Введите {type_input} от 1 до {n_item}: "))
                if 1 <= int(item) <= n_item:
                    print()
                    return int(item) - 1
                else:
                    print("Неправильное число")
            except ValueError:
                print("Ошибка при вводе числа")

    @staticmethod
    def select():
        print(64 * "-")
        for index, el in enumerate(MODE_LIST):
            print("{}. {}".format(index + 1, el[0]))
        print(64 * "-")
        return MODE_LIST[Menu.select_item(len(MODE_LIST))][1]


def main():
    factory = Factory()
    mode = Menu.select()

    while mode != 'exit':
        if mode == 'add':
            factory.add_figure()
        elif mode == 'del':
            factory.del_figure()
        elif mode == 'move':
            factory.move_figure()
        elif mode == 'intersect':
            factory.is_intersect()
        elif mode == 'include':
            factory.is_include()
        elif mode == 'show':
            factory.show_figure()
        mode = Menu.select()


if __name__ == '__main__':
    main()
