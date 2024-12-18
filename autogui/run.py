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

buttons = {
    "create": [601, 192],
    "add_output": [614, 636],
    "vertex_num": [490, 350],
    "density": [490, 390],
    "size": [490, 440],
    "save": [1232, 662],
    "confirm_save": [1005, 534],
    "output": [517, 643]
}

file_dest = "D:\study\master\sem_3\\tangent_bug\obstacle_outputs\sample.json"

time.sleep(0.3)

density = [i for i in range(1,50)]
sample_num = [i for i in range(0, 10)]

for den in density:
    pyautogui.click(x=buttons["density"][0], y=buttons["density"][1])
    pyautogui.press("right", presses=1)

    for sample in sample_num:
        file_dest = f"D:\study\master\sem_3\\tangent_bug\obstacle_outputs\density_{den}_sample_{sample}.json"
        pyautogui.click(x=buttons["vertex_num"][0], y=buttons["vertex_num"][1])
        pyautogui.press("right", presses=10)

        pyautogui.click(x=buttons["add_output"][0], y=buttons["add_output"][1])
        pyautogui.write(file_dest)
        pyautogui.click(x=buttons["save"][0], y=buttons["save"][1], interval=0.3)
        pyautogui.click(x=buttons["confirm_save"][0], y=buttons["confirm_save"][1], interval=0.2)

        pyautogui.click(x=buttons["create"][0], y=buttons["create"][1])
        time.sleep(1)

pyautogui.hotkey('alt', 'f4')
pyautogui.hotkey('enter')

