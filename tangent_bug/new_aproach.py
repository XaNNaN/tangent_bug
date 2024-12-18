import json
import math
import matplotlib.pyplot as plt
import os
print("Current working directory:", os.getcwd())

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

def lines_intersect(a, b, c, d):
    """
    Проверяет пересечение двух отрезков: (a, b) и (c, d).
    Использует векторную математику.
    """
    def ccw(p1, p2, p3):
        return (p3['y'] - p1['y']) * (p2['x'] - p1['x']) > (p2['y'] - p1['y']) * (p3['x'] - p1['x'])

    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

def tangent_bug_algorithm(data, sensor_range, step_size):
    """Реализация Tangent Bug Algorithm с ограничением на дальность сенсора и длину шага."""
    def step(current1, direction1, dest_point1):
        norm = math.sqrt(direction1['x']**2 + direction1['y']**2)
        step = min(step_size, distance(current1, dest_point1))
        current_local = {
            'x': current1['x'] + direction1['x'] / norm * step,
            'y': current1['y'] + direction1['y'] / norm * step
        }
        return current_local
    
    def big_step(current1, direction1, dest_point1):
        norm = math.sqrt(direction1['x']**2 + direction1['y']**2)
        step = min(sensor_range, distance(current1, dest_point1))
        current_local = {
            'x': current1['x'] + direction1['x'] / norm * step,
            'y': current1['y'] + direction1['y'] / norm * step
        }
        return current_local
    
    start = data[1]  # startPoint
    goal = data[2]  # endPoint
    polygons = [item for item in data if item['type'] == 'polygon']

    path = [start]  # Хранит путь, который проходит робот
    current = start
    count = 0

    while distance(current, goal) > 1e-2 and count < 1000:  # Пока не достигнем цели
        count += 1
        visible_points = []

        direction = {
                'x': goal['x'] - current['x'],
                'y': goal['y'] - current['y']
        }

        if is_visible(current, goal, polygons) and distance(current, point) <= sensor_range:
            # Если цель видна и в пределах сенсора, двигаемся прямо к цели
            current = step(current, direction, goal)     
            path.append(current)
            continue

        closest_point = big_step(current, direction, goal)
        if is_visible(current, closest_point, polygons):
            current = step(current, direction, goal)
            path.append(current)
            continue

        for polygon in polygons:
            for point in polygon['points']:
                if is_visible(current, point, polygons) and distance(current, point) <= sensor_range:
                    visible_points.append(point)

        # Если видимых точек нет, то  
        if not visible_points:
            print("Цель недостижима!")
            return path

        # Выбираем видимую точку, ближайшую к цели
        closest_point = min(visible_points, key=lambda p: distance(p, goal))

        # Двигаемся на шаг в направлении ближайшей точки
        direction = {
            'x': closest_point['x'] - current['x'],
            'y': closest_point['y'] - current['y']
        }
        current = step(current, direction, closest_point)
        path.append(current)

    return path

def visualize(data, path, sensor_range):
    """Визуализирует результат работы Tangent Bug Algorithm, включая процесс поиска пути."""
    # Начальная и конечная точки
    start = data[1]
    goal = data[2]

    # Препятствия (полигоны)
    polygons = [item for item in data if item['type'] == 'polygon']

    # Настройка графика
    plt.figure(figsize=(10, 10))
    plt.title("Tangent Bug Algorithm", fontsize=14)
    plt.xlabel("X")
    plt.ylabel("Y")

    # Рисуем полигоны
    for polygon in polygons:
        points = polygon['points']
        x_coords = [p['x'] for p in points] + [points[0]['x']]
        y_coords = [p['y'] for p in points] + [points[0]['y']]
        plt.fill(x_coords, y_coords, color='lightgray', edgecolor='black', linewidth=1, alpha=0.7)

    # Рисуем путь робота поэтапно
    for i in range(1, len(path)):
        segment_x = [path[i - 1]['x'], path[i]['x']]
        segment_y = [path[i - 1]['y'], path[i]['y']]

        # Рисуем окружность радиуса сенсора вокруг текущей позиции робота
        current = path[i - 1]
        sensor_circle = plt.Circle((current['x'], current['y']), sensor_range, color='cyan', fill=False, linestyle='--', linewidth=1)
        plt.gca().add_artist(sensor_circle)
        
        # рисуем начальную и конечную точки
        start_point = plt.scatter(start['x'], start['y'], color='green', label="start point", zorder=5)
        end_point = plt.scatter(goal['x'], goal['y'], color='red', label="goal point", zorder=5)
        legend = plt.legend()
        grid = plt.grid(True)
    

        plt.plot(segment_x, segment_y, color='blue', linewidth=2, label="Path" if i == 1 else "")
        plt.pause(0.1)  # Анимация поиска пути

        # Удаляем отображение сенсора после текущего шага
        sensor_circle.remove()
        start_point.remove()
        end_point.remove()
        legend.remove()
        # grid.remove()

    # рисуем начальную и конечную точки
    plt.scatter(start['x'], start['y'], color='green', label="start point", zorder=5)
    plt.scatter(goal['x'], goal['y'], color='red', label="goal point", zorder=5)

    # Дополнительные настройки
    plt.legend()
    plt.grid(True)
    plt.show()

# Считываем данные из внешнего файла
with open('D:\study\master\sem_3\\tangent_bug\obstacle_outputs\dots10_density40_size1.json', 'r') as file:
    data = json.load(file)

# Параметры алгоритма
SENSOR_RANGE = 20  # Радиус действия сенсора
STEP_SIZE = 2  # Длина шага

path = tangent_bug_algorithm(data, SENSOR_RANGE, STEP_SIZE)

# Визуализируем путь
visualize(data, path, SENSOR_RANGE)
