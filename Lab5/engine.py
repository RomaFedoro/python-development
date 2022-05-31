from random import shuffle
from tkinter import Canvas, Tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename


def get_name_image():
    dialog = Tk()
    filename = askopenfilename(filetypes=[("JPG", ".jpg"), ("PNG", ".png")])
    dialog.destroy()
    return filename


class MosaicPhoto:
    def __init__(self, filename, size):
        image = Image.open(filename)
        factor = size / min(image.height, image.width)
        image = image.resize((int(image.width * factor), int(image.height * factor)), Image.Resampling.LANCZOS)
        start_x = (image.width - size) / 2
        start_y = (image.height - size) / 2
        self.photo = image.crop((start_x, start_y, start_x + size, start_y + size))
        self.background = self.photo.copy()
        alpha = Image.new('L', self.background.size, 25)
        self.background.putalpha(alpha)


class Square:
    def __init__(self, mosaic, index, size, field_size, root):
        row = index // field_size
        column = index % field_size
        cropped = mosaic.photo.crop((column * size, row * size, (column + 1) * size, (row + 1) * size))
        self.image = ImageTk.PhotoImage(cropped, master=root)
        self.index = index


class Game:
    def __init__(self, file_image, field_size, square_size=80):
        self.FIELD_SIZE = field_size
        self.SQUARE_SIZE = square_size
        self.SIZE = field_size * square_size
        self.image = MosaicPhoto(file_image, self.SIZE)
        self.progress = []
        self.finish_state = []
        self.empty_square = None
        self.is_win = False

        self.root = Tk()
        self.root.title("Мозаика")
        self.root.resizable(width=False, height=False)
        self.canvas = Canvas(self.root, width=self.SIZE, height=self.SIZE, background='#747678')

    def draw_board(self):
        self.canvas.delete('all')
        tk_im = ImageTk.PhotoImage(self.image.background, master=self.root)
        self.canvas.image = tk_im
        self.canvas.create_image(self.SIZE / 2, self.SIZE / 2, image=tk_im)

        for i in range(self.FIELD_SIZE ** 2):
            row = i // self.FIELD_SIZE
            column = i % self.FIELD_SIZE
            if i != self.progress.index(self.empty_square) or self.is_win:
                self.canvas.create_image((column + 0.5) * self.SQUARE_SIZE, (row + 0.5) * self.SQUARE_SIZE,
                                         image=self.progress[i].image)

    def start(self):
        self.canvas.delete('all')
        self.progress = []
        self.is_win = False
        for index in range(self.FIELD_SIZE ** 2):
            self.progress.append(Square(self.image, index, self.SQUARE_SIZE, self.FIELD_SIZE, self.root))
        self.empty_square = self.progress[-1]
        self.finish_state = self.progress[:]

        self.canvas.bind('<Button-1>', self.click)

        shuffle(self.progress)
        while not self.is_solvable():
            shuffle(self.progress)

        self.draw_board()
        self.canvas.pack()
        self.root.mainloop()

    def get_inv_count(self):
        inversions = 0
        inversion_board = self.progress[:]
        inversion_board.remove(self.empty_square)
        for i in range(len(inversion_board)):
            first_item = inversion_board[i]
            for j in range(i + 1, len(inversion_board)):
                second_item = inversion_board[j]
                if first_item.index > second_item.index:
                    inversions += 1
        return inversions

    def is_solvable(self):
        num_inversions = self.get_inv_count()
        if self.FIELD_SIZE % 2 != 0:
            return num_inversions % 2 == 0
        else:
            empty_square_row = self.FIELD_SIZE - (self.progress.index(self.empty_square) // self.FIELD_SIZE)
            if empty_square_row % 2 == 0:
                return num_inversions % 2 != 0
            else:
                return num_inversions % 2 == 0

    def get_empty_neighbor(self, index):
        empty_index = self.progress.index(self.empty_square)
        abs_value = abs(empty_index - index)
        if abs_value == self.FIELD_SIZE:
            return empty_index
        elif abs_value == 1:
            max_index = max(index, empty_index)
            if max_index % self.FIELD_SIZE != 0:
                return empty_index
        return index

    def click(self, event):
        x, y = event.x, event.y
        x = x // self.SQUARE_SIZE
        y = y // self.SQUARE_SIZE
        board_index = x + (y * self.FIELD_SIZE)
        empty_index = self.get_empty_neighbor(board_index)
        self.progress[board_index], self.progress[empty_index] = self.progress[empty_index], self.progress[board_index]
        if self.is_win:
            return self.start()
        if self.progress == self.finish_state:
            self.is_win = True
        self.draw_board()
