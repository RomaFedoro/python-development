history = []


def f(x):
    return x**3-4*x**2+x-8


def integral_f(a, b, precision):
    if precision <= 0:
        return None
    n = 2
    h = (b - a)/2
    last_summ = (f(b) + (f(a) + f(b))/2) * (b - a)
    summ = last_summ/2 + f(a+h)*h
    while abs(summ - last_summ) >= precision:
        n *= 2
        h /= 2
        last_summ, summ = summ, (f(a) + f(b))/2*h
        for i in range(1, n+1):
            summ += f(a + i*h)*h
    return summ


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def integral_search():
    a, b, exp = '', '', ''
    while not isfloat(a):
        a = input('\nВведите нижний предел: ')
        if isfloat(a):
            a = float(a)
        else:
            print('Нижний предел должен быть числом')

    while not isfloat(b):
        b = input('Введите верхний предел: ')
        if isfloat(b):
            b = float(b)
        else:
            print('Верхний предел должен быть числом')

    while not isfloat(exp):
        exp = input('Введите точность: ')
        if isfloat(exp):
            exp = float(exp)
            if exp <= 0:
                print('Точность должена быть больше 0')
                exp = ''
        else:
            print('Точность должена быть числом')

    w = integral_f(a, b, exp)
    history.append([a, b, exp, w])
    print_integral(a, b, exp, w)

def print_integral(a, b, exp, w):
    if a <= b:
        print('Значение интеграла f(x) на отрезке [{}; {}] с точностью {}: {}'.format(a, b, exp, w))
    else:
        print('Значение отрицательного интеграла f(x) на отрезке [{}; {}] с точностью {}: {}'.format(b, a, exp, w))

def view_history():
    print("\nИстория вычислений:")
    if not history:
        print("Нет записей")
        return None
    for record in history:
        print_integral(*record)


def main():
    print('Вычисление интеграла f(x) с заданой точностью')
    while True:
        print('\n1 - вычислить интеграл f(x)')
        print('2 - показать историю вычислений')
        print('3 - выйти из программы')
        choice = input('Введите значения: ')
        if not choice.isdigit():
            print('Неверное значение')
        elif int(choice) == 1:
            integral_search()
        elif int(choice) == 2:
            view_history()
        elif int(choice) == 3:
            break
        else:
            print('Неверное значение')




if __name__ == "__main__":
    main()

