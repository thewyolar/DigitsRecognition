import win32gui
import numpy as np
import tkinter as tk
from PIL import ImageGrab
from tensorflow.python.keras.models import load_model

model = load_model('mnist')


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Думаю..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text="Распознать", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Очистить", command=self.clear_all)

        # Сетка окна
        self.canvas.grid(row=0, column=0, pady=2)
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        # self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        im = ImageGrab.grab(rect)

        digit, acc = predict_digit(im)
        self.label.configure(text=str(digit) + ', ' + str(int(acc * 100)) + '%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')


def predict_digit(img):
    img = img.resize((28, 28))
    img = img.convert('L')
    img = np.array(img)
    img = img.reshape(1, 28, 28, 1)
    img = img / 255.0
    res = model.predict([img])[0]

    return np.argmax(res), max(res)
