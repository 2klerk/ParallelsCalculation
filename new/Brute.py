import time
import itertools
from time import sleep
import keyboard


class Brute:
    def __init__(self, pw, chars="123") -> None:
        self.start = time.time()
        self.pw = pw
        self.chars = chars

    def setPw(self, pw):
        self.pw = pw

    def setChars(self, chars):
        self.chars = chars

    def brute(self):
        count = 1
        for CharLength in range(1, 25):
            password = (itertools.product(self.chars, repeat=CharLength))
            for i in password:
                if count % 10000 == 0:
                    if keyboard.is_pressed("esc"):
                        print("\"esc\" pressed. Program ended.")
                        exit()
                count += 1
                i = "".join(i)
                # print(i)
                if i == self.pw:
                    print("Time: ", time.time() - self.start)
                    print("\n-=-=-=-=-=-=\n")
                    print("Password found: " + i)
                    print("\n-=-=-=-=-=-=\n")
                    exit()


# pw = input("Password: ")
# chars = ("abcdefghijklmnopqrstuvwxyz1234567890")
# a = Brute(pw, chars)
# a.brute()
