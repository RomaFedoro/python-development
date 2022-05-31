# Семинар 1. №14

MODE_LIST = [('Посмотртеть библиотеку', 'output'),
             ('Добавить книгу', 'add'),
             ('Удалить книгу', 'del'),
             ('Найти книги', 'search'),
             ('Сортировать библиотеку', 'sort'),
             ('Выйти', 'exit'),
             ]

PROPS_LIST = [('По названию', 'name'), ('По автору', 'author'), ('По году издания', 'year')]


class HomeLibrary:
    def __init__(self, list_books=()):
        self.books = [el for el in list_books]

    def __str__(self):
        return 'Всего книг: {}\n{}'.format(len(self.books), "\n".join(map(str, self.books)))

    def search_books(self, request, filter_r):
        request = request.lower()
        result = []
        for book in self.books:
            if filter_r is None or filter_r == 'name':
                if request in book.name.lower():
                    result.append(book)
                    continue
            elif filter_r is None or filter_r == 'author':
                if request in book.author.lower():
                    result.append(book)
                    continue
            elif filter_r is None or filter_r == 'year':
                if request.isdigit() and book.year == int(request):
                    result.append(book)
        return result

    def add_books(self, books):
        if isinstance(books, Book):
            self.books.append(books)
        elif isinstance(books, list):
            self.books.extend(books)

    def del_books(self, index=None):
        if len(self.books):
            if index is None:
                index = Menu.output_book(self.books)
            if 0 <= index < len(self.books):
                del self.books[index]

    def sort_books(self, filter_r):
        if filter_r is None or filter_r == 'name':
            self.books.sort(key=lambda book: book.name)
        elif filter_r == 'author':
            self.books.sort(key=lambda book: book.author)
        elif filter_r == 'year':
            self.books.sort(key=lambda book: book.year)


class Book:
    def __init__(self):
        while True:
            self.name = input('Введите название: ')
            if self.name:
                break
        while True:
            self.author = input('Введите автора: ')
            if self.author:
                break
        while True:
            try:
                self.year = int(input('Введите год издания: '))
                print()
                break
            except ValueError:
                print("Ошибка при вводе числа")

    def __str__(self):
        return '"{}", {}. {} г.'.format(self.name, self.author, self.year)


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

    @staticmethod
    def select_props(title=''):
        print(title)
        for index, el in enumerate(PROPS_LIST):
            print("{}. {}".format(index + 1, el[0]))
        return Menu.select_item(len(PROPS_LIST))

    @staticmethod
    def output_book(books):
        for i, book in enumerate(books):
            print("{}. {}".format(i + 1, book))
        return Menu.select_item(len(books), 'книгу')


def main():
    home_lib = HomeLibrary()
    mode = Menu.select()
    while mode != 'exit':
        if mode == 'output':
            print(home_lib)
        elif mode == 'add':
            new_book = Book()
            home_lib.add_books(new_book)
        elif mode == 'del':
            print("Какую книгу удалить?")
            home_lib.del_books()
        elif mode == 'search':
            name_filter, filter_r = PROPS_LIST[Menu.select_props('Поиск в библиотеке:')]
            print('Поиск', name_filter.lower())
            request = input('Введите значение: ')
            result = home_lib.search_books(request, filter_r)
            print('\nВсего найдено книг: {}'.format(len(result)))
            for el in result:
                print(el)
        elif mode == 'sort':
            name_filter, filter_r = PROPS_LIST[Menu.select_props('Сортировка в библиотеке:')]
            home_lib.sort_books(filter_r)
            print('Сортировка', name_filter.lower(), 'выполнена\n')
            print(home_lib)
        mode = Menu.select()


if __name__ == '__main__':
    main()
