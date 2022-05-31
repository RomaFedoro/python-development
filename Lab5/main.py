from engine import Game, get_name_image


def main():
    print('Игра Мозаика')
    size = int(input("Введите размер поля: "))
    mosaic = Game(get_name_image(), size, 600 // size)
    mosaic.start()


if __name__ == '__main__':
    main()
