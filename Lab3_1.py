# Семинар 1. №17

MODE_LIST = [
    ('Арифметические операции', 'operation'),
    ('Преобразовать в обратную матрицу', 'inverse'),
    ('Транспонировать матрицу', 'transpose'),
    ('Информация о матрице', 'inform'),
    ('Заменить матрицу', 'replace'),
    ('Выход', 'exit'),
]

OPERATION_LIST = [
    ('Сложение', 'add'),
    ('Вычитание', 'sub'),
    ('Умножение', 'multi'),
    ('Деление', 'div'),
    ('Сравнение', 'eq'),
    ('Возведение в степень', 'power'),
]

SETTING_LIST = [
    ('Матрица', 'matrix'),
    ('Число', 'num'),
]


def status(value):
    if value:
        return '✔'
    return '❌'


class Matrix:
    def __init__(self, start_data=()):
        if start_data:
            self.data = start_data
        else:
            self.data = []
            while True:
                try:
                    size = tuple(map(int, input("Введите размеры матрицы: ").split()))
                    if len(size) == 2 and size[0] > 0 and size[1] > 0:
                        break
                except ValueError:
                    print("Ошибка при вводе")
            rows, columns = size
            m = 0

            print("Введите матрицу: ")
            while m < rows:
                try:
                    row = tuple(map(float, input().split()))
                    if len(row) == columns:
                        self.data.append(row)
                        m += 1
                    else:
                        print("В строке должно быть {} элементов".format(columns))
                except ValueError:
                    print("Значения должны быть числами")
            self.data = tuple(self.data)

    def __str__(self):
        result = ''
        for row in self.data:
            for cell in row:
                result += '%.2f' % cell + ' '
            result += '\n'
        return result

    def is_square(self, matrix=()):
        if not matrix:
            matrix = self.data
        return len(matrix) == len(matrix[0])

    def is_null(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j]:
                    return False
        return True

    def is_identity(self):
        if not self.is_square():
            return False
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if i == j:
                    if self.data[i][j] != 1:
                        return False
                elif self.data[i][j]:
                    return False
        return True

    def is_diagonal(self):
        if not self.is_square():
            return False
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if i == j:
                    continue
                if self.data[i][j]:
                    return False
        return True

    def is_symmetric(self):
        matrix_t = self.transpose()
        return self.data == matrix_t.data

    def is_lower_triangular(self):
        if not self.is_square():
            return False
        for i in range(len(self.data)):
            for j in range(i + 1, len(self.data[0])):
                if self.data[i][j]:
                    return False
        return True

    def is_upper_triangular(self):
        if not self.is_square():
            return False
        for i in range(len(self.data)):
            for j in range(i):
                if self.data[i][j]:
                    return False
        return True

    def det(self, matrix=()):
        if not matrix:
            matrix = self.data
        if not self.is_square(matrix):
            print('Матрица должны быть квадратной')
            return
        if len(matrix) == 1:
            return matrix[0][0]
        result = 0
        for k in range(len(matrix)):
            new_matrix = []
            for i in range(1, len(matrix)):
                row = []
                for j in range(len(matrix)):
                    if j == k:
                        continue
                    row.append(matrix[i][j])
                new_matrix.append(tuple(row))
            new_matrix = tuple(new_matrix)
            if k % 2:
                result -= matrix[0][k] * self.det(new_matrix)
            else:
                result += matrix[0][k] * self.det(new_matrix)
        return result

    def transpose(self):
        new_matrix = []
        for j in range(len(self.data[0])):
            new_row = []
            for i in range(len(self.data)):
                new_row.append(self.data[i][j])
            new_matrix.append(tuple(new_row))
        return Matrix(tuple(new_matrix))

    def inverse(self):
        det_matrix = self.det()
        if det_matrix is None:
            print('Определитель не определен. Обратная матрица не существует')
            return
        if not det_matrix:
            print('Определитель равен нулю. Обратная матрица не существует')
            return
        new_matrix = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data)):
                minor = []
                minor_row = []
                for k in range(len(self.data) ** 2):
                    i_m = k // len(self.data)
                    j_m = k % len(self.data)
                    if i_m == i or j_m == j:
                        continue
                    minor_row.append(self.data[i_m][j_m])
                    if len(minor_row) == len(self.data) - 1:
                        minor.append(tuple(minor_row))
                        minor_row = []
                minor = self.det(tuple(minor)) / det_matrix
                if (i + j) % 2:
                    minor *= -1
                row.append(minor)
            new_matrix.append(tuple(row))
        return Matrix(tuple(new_matrix)).transpose()

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return self.data == other.data
        return False

    def __add__(self, other):
        new_matrix = []
        if isinstance(other, Matrix):
            rows, columns = max(len(self.data), len(other.data)), max(len(self.data[0]), len(other.data[0]))
            for i in range(rows):
                new_row = []
                for j in range(columns):
                    new_cell = 0
                    if i < len(self.data) and j < len(self.data[0]):
                        new_cell += self.data[i][j]
                    if i < len(other.data) and j < len(other.data[0]):
                        new_cell += other.data[i][j]
                    new_row.append(new_cell)
                new_matrix.append(tuple(new_row))
        elif isinstance(other, int) or isinstance(other, float):
            diag = min(len(self.data), len(self.data[0]))
            for i in range(len(self.data)):
                new_row = []
                for j in range(len(self.data[0])):
                    new_cell = self.data[i][j]
                    if diag > i == j < diag:
                        new_cell += other
                    new_row.append(new_cell)
                new_matrix.append(tuple(new_row))
        else:
            new_matrix = self.data
        return Matrix(tuple(new_matrix))

    def __sub__(self, other):
        new_matrix = []
        if isinstance(other, Matrix):
            rows, columns = max(len(self.data), len(other.data)), max(len(self.data[0]), len(other.data[0]))
            for i in range(rows):
                new_row = []
                for j in range(columns):
                    new_cell = 0
                    if i < len(self.data) and j < len(self.data[0]):
                        new_cell += self.data[i][j]
                    if i < len(other.data) and j < len(other.data[0]):
                        new_cell -= other.data[i][j]
                    new_row.append(new_cell)
                new_matrix.append(tuple(new_row))
        elif isinstance(other, int) or isinstance(other, float):
            diag = min(len(self.data), len(self.data[0]))
            for i in range(len(self.data)):
                new_row = []
                for j in range(len(self.data[0])):
                    new_cell = self.data[i][j]
                    if diag > i == j < diag:
                        new_cell -= other
                    new_row.append(new_cell)
                new_matrix.append(tuple(new_row))
        else:
            new_matrix = self.data
        return Matrix(tuple(new_matrix))

    def __mul__(self, other):
        new_matrix = []
        if isinstance(other, Matrix):
            if len(self.data[0]) != len(other.data):
                print('Умножение невозможно. Размер строки первой матрицы должен совпадать с размером столбца второй')
                return
            for i in range(len(self.data)):
                new_row = []
                for j in range(len(other.data[0])):
                    new_cell = 0
                    for k in range(len(other.data)):
                        new_cell += self.data[i][k] * other.data[k][j]
                    new_row.append(new_cell)
                new_matrix.append(tuple(new_row))
        elif isinstance(other, int) or isinstance(other, float):
            diag = min(len(self.data), len(self.data[0]))
            for i in range(len(self.data)):
                new_row = []
                for j in range(len(self.data[0])):
                    new_cell = self.data[i][j] * other
                    new_row.append(new_cell)
                new_matrix.append(tuple(new_row))
        else:
            new_matrix = self.data
        return Matrix(tuple(new_matrix))

    def __truediv__(self, other):
        new_matrix = []
        if isinstance(other, Matrix):
            inverse_other = other.inverse()
            if not inverse_other:
                print('Деление невозможно')
                return
            return self * inverse_other
        elif isinstance(other, int) or isinstance(other, float):
            if other == 0:
                print('Деление на 0 невозможно')
                return
            for i in range(len(self.data)):
                new_row = []
                for j in range(len(self.data[0])):
                    new_cell = self.data[i][j] / other
                    new_row.append(new_cell)
                new_matrix.append(tuple(new_row))
        else:
            new_matrix = self.data
        return Matrix(tuple(new_matrix))

    def __pow__(self, power, modulo=None):
        if not self.is_square():
            print('Возведение в степень невозможно. Матрица должна быть квадратной\n')
            return None
        if power == 0:
            return Matrix(((1)))
        temp_matrix = Matrix(self.data)
        new_matrix = Matrix(temp_matrix.data)
        power -= 1
        while power:
            if power % 2:
                new_matrix *= temp_matrix
                power -= 1
            else:
                temp_matrix *= temp_matrix
                power //= 2
        return new_matrix

    def m_norm(self):
        result = None
        for i in range(len(self.data)):
            sum_row = 0
            for j in range(len(self.data[0])):
                sum_row += abs(self.data[i][j])
            if result is None or result < sum_row:
                result = sum_row
        return result

    def l_norm(self):
        result = None
        for j in range(len(self.data[0])):
            sum_row = 0
            for i in range(len(self.data)):
                sum_row += abs(self.data[i][j])
            if result is None or result < sum_row:
                result = sum_row
        return result

    def k_norm(self):
        result = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                result += self.data[i][j] ** 2
        return result ** 0.5


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
    def select_operator():
        print('Какой арифметический оператор выберете?')
        for index, el in enumerate(OPERATION_LIST):
            print("{}. {}".format(index + 1, el[0]))
        index = Menu.select_item(len(OPERATION_LIST), 'оператор')
        return OPERATION_LIST[index]

    @staticmethod
    def input_second_arg(type_arg=''):
        if not type_arg:
            print('Какой тип у второго аргумента?')
            for index, el in enumerate(SETTING_LIST):
                print("{}. {}".format(index + 1, el[0]))
            type_arg = SETTING_LIST[Menu.select_item(len(SETTING_LIST), 'тип')][1]
        if type_arg == 'matrix':
            return Matrix()
        else:
            while True:
                try:
                    return int(input(f"Введите число: "))
                except ValueError:
                    print("Ошибка при вводе числа")

    @staticmethod
    def select(curr):
        print(64 * "-")
        print('Текущая матрица:')
        print(curr)
        for index, el in enumerate(MODE_LIST):
            print("{}. {}".format(index + 1, el[0]))
        print(64 * "-")
        return MODE_LIST[Menu.select_item(len(MODE_LIST))][1]


def main():
    curr_matrix = Matrix()
    mode = Menu.select(curr_matrix)
    while mode != 'exit':
        if mode == 'inverse':
            temp_matrix = curr_matrix.inverse()
            if temp_matrix:
                curr_matrix = temp_matrix
            print('Матрица преобразована в обратную')
        elif mode == 'transpose':
            curr_matrix = curr_matrix.transpose()
            print('Матрица транспорнирована')
        elif mode == 'replace':
            curr_matrix = Matrix()
            print('\nМатрица заменена')
        elif mode == 'inform':
            print('ИНФОРМАЦИЯ О МАТРИЦЕ\n')
            print(curr_matrix)

            print('Определитель:', end=' ')
            det_matrix = curr_matrix.det()
            if det_matrix is not None:
                print(det_matrix)
            else:
                print('не существует')

            print('\nОбратная матрица:')
            in_matrix = curr_matrix.inverse()
            if in_matrix:
                print(in_matrix)

            print('\nL-норма:', curr_matrix.l_norm())
            print('M-норма:', curr_matrix.m_norm())
            print('K-норма:', '%.3f' % curr_matrix.k_norm())

            print('\nСвойства матрицы')
            print('Кадратная матрица:', status(curr_matrix.is_square()))
            print('Диагональная матрица:', status(curr_matrix.is_diagonal()))
            print('Нулевая матрица:', status(curr_matrix.is_null()))
            print('Единичная матрица:', status(curr_matrix.is_identity()))
            print('Симметричная матрица:', status(curr_matrix.is_symmetric()))
            print('Верхнетреугольная матрица:', status(curr_matrix.is_upper_triangular()))
            print('Нижнетреугольная матрица:', status(curr_matrix.is_lower_triangular()))
        elif mode == 'operation':
            operation = Menu.select_operator()
            if operation[1] == 'power':
                second_arg = Menu.input_second_arg('num')
            elif operation[1] == 'eq':
                second_arg = Menu.input_second_arg('matrix')
            else:
                second_arg = Menu.input_second_arg()

            print(64 * "-")
            print(operation[0].upper())
            print('\nПервый аргумент: ')
            print(curr_matrix)
            print('Второй аргумент: ')
            print(second_arg)
            print('\nРезультат: ')
            operation = operation[1]
            if operation == 'add':
                curr_matrix += second_arg
                print(curr_matrix)
            elif operation == 'sub':
                curr_matrix -= second_arg
                print(curr_matrix)
            elif operation == 'multi':
                temp_matrix = Matrix(curr_matrix.data)
                temp_matrix *= second_arg
                if temp_matrix:
                    curr_matrix = temp_matrix
                    print(curr_matrix)
            elif operation == 'div':
                temp_matrix = Matrix(curr_matrix.data)
                temp_matrix /= second_arg
                if temp_matrix:
                    curr_matrix = temp_matrix
                    print(curr_matrix)
            elif operation == 'eq':
                if curr_matrix == second_arg:
                    print('Матрицы равны')
                else:
                    print('Аргументы не равны')
            elif operation == 'power':
                temp_matrix = Matrix(curr_matrix.data)
                temp_matrix **= second_arg
                if temp_matrix:
                    curr_matrix = temp_matrix
                    print(curr_matrix)
        mode = Menu.select(curr_matrix)


if __name__ == '__main__':
    main()
