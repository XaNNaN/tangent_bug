import tangent_bug_window as tg_bug
import json
import time
import numpy as np
import pandas as pd

from pathlib import Path


    
# Параметры алгоритма
SQ_SIZE = 12 # Размер окна включения в анализ
SENSOR_RANGE = 8  # Радиус действия сенсора
STEP_SIZE = 1  # Длина шага

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Записываем время начала выполнения
        result = func(*args, **kwargs)  # Выполняем функцию
        end_time = time.time()  # Записываем время окончания выполнения
        execution_time = end_time - start_time  # Вычисляем время выполнения
        return result, execution_time  # Возвращаем результат выполнения функции
    return wrapper
    
def call_with_decorator(func, *args, **kwargs):
    # Применяем декоратор ко временному обертке для конкретного вызова
    decorated_func = timing_decorator(func)
    result, exec_time = decorated_func(*args, **kwargs)
    return result, exec_time
def make_file_name(file_rel_path: str, density: int, sample: int)-> str:
    file_name = file_rel_path + f'\\obstacle_outputs\\density_{density}_sample_{sample}_n.json'
    return file_name

if __name__ == "__main__":
    density_counter = 50
    samples_counter = 10
    cwd = Path.cwd()

    cur_density_timers = np.empty((0, 3)) 
    total_timers = np.empty((0, 3))

    for density in range(1, density_counter):
        cur_density_timers = np.empty((0, 3)) 
        for sample in range(samples_counter):
            file_path_name = make_file_name(str(cwd), density, sample)
            with open(file_path_name, 'r') as file:
                data, file_loading_time = call_with_decorator(json.load, file)
                result, path_finding_time = call_with_decorator(tg_bug.tangent_bug_algorithm, data, SENSOR_RANGE, STEP_SIZE)
                path = result[0]
                count = result[1]
                cur_density_timers = np.vstack([cur_density_timers, [file_loading_time, count, path_finding_time]])

        total_timers = np.vstack([total_timers, cur_density_timers.mean(axis=0)])
        print("Density: " + str(density))
        print(total_timers[-1, :])

df = pd.DataFrame(total_timers)
print(df.describe())

df.to_csv("result.csv")