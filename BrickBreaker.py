import tkinter as tk
import random

class GameObject:
    """Parent Class untuk semua objek di dalam Canvas (OOP: Inheritance)"""
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class BackgroundStar(GameObject):
    """Kelas untuk Bintang/Partikel Latar Belakang yang Berjalan Terus ke Bawah"""
    def __init__(self, canvas, x, y, speed, size):
        self.speed = speed
        item = canvas.create_oval(x, y, x + size, y + size, fill="#E0F7FA", outline="")
        super().__init__(canvas, item)

    def update(self, height):
        self.move(0, self.speed)
        coords = self.get_position()
        # Jika keluar layar bawah, pindahkan kembali ke atas secara acak
        if coords[1] > height:
            self.canvas.coords(self.item, coords[0], -10, coords[0] + (coords[2]-coords[0]), -10 + (coords[3]-coords[1]))


class Ball(GameObject):
    """Child Class Bola"""
    def __init__(self, canvas, x, y, speed=5):
        self.radius = 9
        self.direction = [random.choice([-1, 1]), -1]
        self.speed = speed
        item = canvas.create_oval(
            x - self.radius, y - self.radius,
            x + self.radius, y + self.radius,
            fill="#FF80AB", outline="#FFFFFF", width=2
        )
        super().__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()

        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1

        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)


class Paddle(GameObject):
    """Child Class Papan Pemantul"""
    def __init__(self, canvas, x, y):
        self.width = 110
        self.height = 15
        item = canvas.create_rectangle(
            x - self.width / 2, y - self.height / 2,
            x + self.width / 2, y + self.height / 2,
            fill="#4DD0E1", outline="#FFFFFF", width=2
        )
        super().__init__(canvas, item)

    def move(self, offset, max_width):
        coords = self.get_position()
        if coords[0] + offset >= 0 and coords[2] + offset <= max_width:
            super().move(offset, 0)

    def expand(self):
        coords = self.get_position()
        if (coords[2] - coords[0]) < 170:
            self.canvas.coords(self.item, coords[0] - 15, coords[1], coords[2] + 15, coords[3])

class Brick(GameObject):
    """Child Class Balok Multi-Hit dengan Nuansa Petualangan"""
    COLORS = {1: "#80DEEA", 2: "#F48FB1", 3: "#CE93D8"}

    def __init__(self, canvas, x, y, hits, callback):
        self.width = 75
        self.height = 24
        self.hits = hits
        self.max_hits = hits
        self.callback = callback
        item = canvas.create_rectangle(
            x - self.width / 2, y - self.height / 2,
            x + self.width / 2, y + self.height / 2,
            fill=Brick.COLORS[hits], outline="#0D1B2A", width=1, tags="brick"
        )
        super().__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if self.hits <= 0:
            coords = self.get_position()
            self.delete()
            if self.callback:
                self.callback(self.max_hits * 10, (coords[0] + coords[2]) / 2, coords[3])
        else:
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])


class PowerUp(GameObject):
    """Item Bonus Unik yang Jatuh"""
    def __init__(self, canvas, x, y, kind):
        self.kind = kind
        colors = {"multi": "#FFD54F", "life": "#81C784", "laser": "#FF4081"}
        item = canvas.create_oval(x - 9, y - 9, x + 9, y + 9, fill=colors[kind], outline="white", width=2)
        super().__init__(canvas, item)

    def update(self):
        self.move(0, 3.5)

class Laser(GameObject):
    """Peluru Laser yang ditembakkan Paddle"""
    def __init__(self, canvas, x, y):
        item = canvas.create_rectangle(x - 2, y - 10, x + 2, y, fill="#FF4081", outline="")
        super().__init__(canvas, item)

    def update(self):
        self.move(0, -7)

