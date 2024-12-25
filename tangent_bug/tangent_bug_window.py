import json
import math
import matplotlib.pyplot as plt
import os
import time
from matplotlib.animation import FuncAnimation

# Параметры алгоритма
SQ_SIZE = 12 # Размер окна включения в анализ
SENSOR_RANGE = 8  # Радиус действия сенсора
STEP_SIZE = 1  # Длина шага

# print("Current working directory:", os.getcwd())

def distance(point1, point2):
    """Вычисляет евклидово расстояние между двумя точками."""
    return math.sqrt((point1['x'] - point2['x'])**2 + (point1['y'] - point2['y'])**2)

def is_visible(current, target, polygons):
    """
    Проверяет, существует ли прямая видимость между двумя точками
    с учетом всех препятствий.
    """
    for polygon in polygons:
        points = polygon['points']
        n = len(points)
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]  # Следующая вершина (замыкаем полигон)
            if lines_intersect(current, target, p1, p2):
                return False
    return True

def is_within_square(current, anchor, square_size=50):
    """Проверяет, попадает ли якорная точка полигона в квадратную область вокруг текущей точки робота."""
    return abs(current['x'] - anchor['x']) <= square_size and abs(current['y'] - anchor['y']) <= square_size

def lines_intersect(a, b, c, d):
    """
    Проверяет пересечение двух отрезков: (a, b) и (c, d).
    Использует векторную математику.
    """
    def ccw(p1, p2, p3):
        return (p3['y'] - p1['y']) * (p2['x'] - p1['x']) > (p2['y'] - p1['y']) * (p3['x'] - p1['x'])

    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

def get_cur_poly(polygons, current):
    cur_poly = []
    for poly in polygons:
        if is_within_square(current, poly["anchor"], SQ_SIZE):
            cur_poly.append(poly)
    return cur_poly

def tangent_bug_algorithm(data, sensor_range, step_size):
    """Реализация Tangent Bug Algorithm с ограничением на дальность сенсора и длину шага."""
    def step(current1, direction1, dest_point1):
        norm = math.sqrt(direction1['x']**2 + direction1['y']**2)
        step = min(step_size, distance(current1, dest_point1))
        if norm == 0:
            current_local = {
            'x': current1['x'],
            'y': current1['y']
            }   
            return current_local
            exit(0)
            norm = 0.1
        current_local = {
            'x': current1['x'] + direction1['x'] / norm * step,
            'y': current1['y'] + direction1['y'] / norm * step
        }
        return current_local
    
    def big_step(current1, direction1, dest_point1):
        norm = math.sqrt(direction1['x']**2 + direction1['y']**2)
        if norm == 0:
            current_local = {
            'x': current1['x'],
            'y': current1['y']
            }   
            return current_local
            exit(0)
            norm = 0.1
        step = min(sensor_range, distance(current1, dest_point1))
        current_local = {
            'x': current1['x'] + direction1['x'] / norm * step,
            'y': current1['y'] + direction1['y'] / norm * step
        }
        return current_local
    
    start = data[1]  # startPoint
    goal = data[2]  # endPoint
    polygons = [item for item in data if item['type'] == 'polygon']

    # Добавление якорной точки для каждого полигона
    for polygon in polygons:
        polygon['anchor'] = polygon['points'][0]

    path = [start]  # Хранит путь, который проходит робот
    current = start
    count = 0

    while distance(current, goal) > 1e-2 and count < 1000:  # Пока не достигнем цели
        count += 1
        visible_points = []

        cur_polygons = get_cur_poly(polygons, current)
        # print(len(cur_polygons))

        direction = {
                'x': goal['x'] - current['x'],
                'y': goal['y'] - current['y']
        }

        if is_visible(current, goal, cur_polygons) and distance(current, goal) <= sensor_range:
            # Если цель видна и в пределах сенсора, двигаемся прямо к цели
            new_pos = step(current, direction, goal)
            if current['x'] == new_pos['x'] and current['y'] == new_pos['y']:
                return path, count 
            current = new_pos.copy()    
            path.append(current)
            
            continue

        closest_point = big_step(current, direction, goal)
        if is_visible(current, closest_point, cur_polygons):
            new_pos = step(current, direction, goal)
            if current['x'] == new_pos['x'] and current['y'] == new_pos['y']:
                return path, count 
            current = new_pos.copy()
            path.append(current)
            continue

        for polygon in cur_polygons:
            for point in polygon['points']:
                if is_visible(current, point, cur_polygons) and distance(current, point) <= sensor_range:
                    visible_points.append(point)

        # Если видимых точек нет, то  
        if not visible_points:
            print("Цель недостижима!")
            return path, count

        # Выбираем видимую точку, ближайшую к цели
        closest_point = min(visible_points, key=lambda p: distance(p, goal))

        # Двигаемся на шаг в направлении ближайшей точки
        direction = {
            'x': closest_point['x'] - current['x'],
            'y': closest_point['y'] - current['y']
        }
        current = step(current, direction, closest_point)
        path.append(current)

    return path, count

def visualize(data, path, sensor_range, count):
    """Визуализирует результат работы Tangent Bug Algorithm с помощью анимации."""
    # Настройка графика
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title("Tangent Bug Algorithm", fontsize=14)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    pause_time =  1000 / count

    # Начальная и конечная точки
    start = data[1]
    goal = data[2]

    # Препятствия (полигоны)
    polygons = [item for item in data if item['type'] == 'polygon']

    # Рисуем полигоны
    for polygon in polygons:
        points = polygon['points']
        x_coords = [p['x'] for p in points] + [points[0]['x']]
        y_coords = [p['y'] for p in points] + [points[0]['y']]
        ax.fill(x_coords, y_coords, color='lightgray', edgecolor='black', linewidth=1, alpha=0.7)

    # Начальная и конечная точки
    ax.scatter(start['x'], start['y'], color='green', label="Start Point", zorder=5)
    ax.scatter(goal['x'], goal['y'], color='red', label="Goal Point", zorder=5)

    # Путь робота
    path_line, = ax.plot([], [], color='blue', linewidth=2, label="Path")
    sensor_circle = plt.Circle((0, 0), sensor_range, color='cyan', fill=False, linestyle='--', linewidth=1)
    ax.add_artist(sensor_circle)

    ax.legend()
    ax.grid(True)

    # Анимация
    def init():
        """Инициализация анимации."""
        path_line.set_data([], [])
        sensor_circle.set_center((start['x'], start['y']))
        return path_line, sensor_circle

    def update(frame):
        """Обновление на каждом кадре."""
        if frame >= len(path):
            return path_line, sensor_circle

        # Обновляем путь
        x_data = [p['x'] for p in path[:frame + 1]]
        y_data = [p['y'] for p in path[:frame + 1]]
        path_line.set_data(x_data, y_data)

        # Обновляем положение сенсора
        current_position = path[frame]
        sensor_circle.set_center((current_position['x'], current_position['y']))

        return path_line, sensor_circle

    anim = FuncAnimation(
        fig, update, frames=len(path), init_func=init, blit=True, interval=pause_time
    )

    plt.show()

if __name__ == "__main__":

    # Считываем данные из внешнего файла
    with open('C:\study\master\sem_3\\tangent_bug\obstacle_outputs\density_44_sample_5.json', 'r') as file:
        data = json.load(file)

    print("File is read")
    path, count = tangent_bug_algorithm(data, SENSOR_RANGE, STEP_SIZE)
    print(count)
    # Визуализируем путь
    start_time = time.time()
    visualize(data, path, SENSOR_RANGE, count)
    end_time = time.time()
    print(end_time - start_time)