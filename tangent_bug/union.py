import json
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

from pathlib import Path

# Функция для чтения JSON
def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Функция для записи JSON
def write_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Функция для создания полигона из списка точек
def create_polygon(points):
    return Polygon([(point['x'], point['y']) for point in points])

def polygon_to_json(polygon):
    """
    Преобразует полигон в JSON-формат, добавляя точки на середине каждого отрезка.

    Args:
        polygon: Полигон объекта Shapely.

    Returns:
        Словарь, представляющий полигон в формате JSON.
    """
    coords = list(polygon.exterior.coords)  # Получаем координаты полигона
    new_coords = []

    for i in range(len(coords) - 1):  # Обрабатываем каждый отрезок
        p1 = coords[i]
        p2 = coords[i + 1]

        # Добавляем начальную точку отрезка
        new_coords.append({"type": "point", "x": p1[0], "y": p1[1]})

        # Вычисляем среднюю точку и добавляем её
        # midpoint = {"type": "point", "x": (p1[0] + p2[0]) / 2, "y": (p1[1] + p2[1]) / 2}
        # new_coords.append(midpoint)

    # Последняя точка не добавляется, так как она совпадает с первой (замкнутый полигон)
    return {
        "type": "polygon",
        "points": new_coords
    }

# Основная функция для обработки пересекающихся полигонов
def process_polygons(input_file, output_file):
    data = read_json(input_file)

    merged_data = []
    # Добавляем в JSON остальную информацию (startPoint, endPoint, info)
    for item in data:
        if item['type'] != 'polygon':
            merged_data.append(item)

    # Извлекаем полигоны из входного JSON
    polygons = [create_polygon(item['points']) for item in data if item['type'] == 'polygon']

     # Проверяем и исправляем валидность каждого полигона
    valid_polygons = [polygon.buffer(0) if not polygon.is_valid else polygon for polygon in polygons]

    # Объединяем пересекающиеся полигоны
    merged_polygons = unary_union(valid_polygons)

    # Если результат - MultiPolygon, преобразуем его в список полигонов
    if isinstance(merged_polygons, MultiPolygon):
        merged_polygons = list(merged_polygons.geoms)
    elif merged_polygons.geom_type == 'Polygon':
        # Если результат - единичный полигон, обернуть в список
        merged_polygons = [merged_polygons]

    # Преобразуем результат обратно в JSON
    # merged_data = [polygon_to_json(poly) for poly in merged_polygons]
    for poly in merged_polygons:
        merged_data.append(polygon_to_json(poly))


    # Записываем результат в новый файл
    write_json(merged_data, output_file)

def make_file_name(file_rel_path: str, density: int, sample: int)-> str:
    file_name = file_rel_path + f'\\obstacle_outputs\\density_{density}_sample_{sample}.json'
    return file_name

def make_file_name_1(file_rel_path: str, density: int, sample: int)-> str:
    file_name = file_rel_path + f'\\obstacle_outputs\\density_{density}_sample_{sample}_n.json'
    return file_name

density_counter = 50
samples_counter = 10
cwd = Path.cwd()

for density in range(1, density_counter):
    for sample in range(samples_counter):
        old_file = make_file_name(str(cwd), density, sample)
        new_file = make_file_name_1(str(cwd), density, sample)
        process_polygons( old_file, new_file)

