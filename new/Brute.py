import time
import itertools
from time import sleep
import keyboard


class Brute:
    def __init__(self, pw, chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") -> None:
        self.start = None
        self.pw = pw
        self.chars = chars

    def setPw(self, pw):
        self.pw = pw

    def setChars(self, chars):
        self.chars = chars

    def brute(self, a, b):
        self.start = time.time()
        count = 1
        b+=1
        for CharLength in range(a, b):
            print(CharLength, time.time() - self.start)
            password = (itertools.product(self.chars, repeat=CharLength))
            for i in password:
                if count % 10000 == 0:
                    if keyboard.is_pressed("esc"):
                        print("\"esc\" pressed. Program ended.")
                        exit()
                count += 1
                i = "".join(i)
                if i == self.pw:
                    print("Time: ", time.time() - self.start)
                    print("\n-=-=-=-=-=-=\n")
                    print("Password found: " + i)
                    print("\n-=-=-=-=-=-=\n")
                    return i

# pw = input("Password: ")
# a = Brute(pw, chars)
# a.brute()
