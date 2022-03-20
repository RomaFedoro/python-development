# Словари

School = {
    '1А': 25,
    '2В': 21,
    '3Г': 24,
    '4Б': 28,
    '5В': 19,
}

def print_school():
    for name_class in School:
        print(f'{name_class} класс - {School[name_class]} человек')

def students_in_class(name_class):
    name_class = name_class.upper()
    if name_class in School:
        print(f'В {name_class} классе {School[name_class]} человек')
    else:
        print('Такого класса не существует')


def change_number_students(name_class, count):
    name_class = name_class.upper()
    if name_class in School:
        School[name_class] = count
    else:
        print('Такого класса не существует')

def add_class(name_class, count):
    name_class = name_class.upper()
    if name_class not in School:
        School[name_class] = count
    else:
        print(f'{name_class} класс уже существует')

def delete_class(name_class):
    name_class = name_class.upper()
    if name_class in School:
        School.pop(name_class)

def main():
    print_school()
    print()
    students_in_class('5в')
    students_in_class('1б')
    print()
    change_number_students('1А', 20)
    change_number_students('2В', 25)
    change_number_students('4Б', 29)
    print_school()
    print()
    add_class('6А', 22)
    add_class('7Б', 21)
    print_school()
    print()
    delete_class('7Б')
    print_school()
    print()



if __name__ == "__main__":
    main()
