import pyautogui
import time
import numpy as np

# Запуск программы
pyautogui.hotkey('win', 'r')
pyautogui.typewrite('D:\study\master\sem_3\\tangent_bug\obstacle_generator\ATP_generator.exe\n')

# Переход к полю ввода
# pyautogui.click(x=400, y=300)  # Координаты текстового поля
# pyautogui.typewrite('Hello World')
# pyautogui.press('enter')  # Нажимаем Enter


while 1:
    time.sleep(1)
    print(pyautogui.position())