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


