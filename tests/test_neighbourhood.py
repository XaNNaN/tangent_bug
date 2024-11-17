import numpy as np

from  tangent_bug.neighbourhood import neighbours_for_point
from numpy.testing import assert_array_equal

def check_arrays(result, exp_arr1, exp_arr2):
     # Проверяем, что возвращаемый кортеж состоит из двух массивов
    assert isinstance(result, tuple), f"Expected tuple, but got {type(result)}"
    assert len(result) == 2, f"Expected tuple of length 2, but got length {len(result)}"
    
    # Проверяем, что каждый из элементов в кортеже - это numpy массив
    assert isinstance(result[0], np.ndarray), f"Expected np.ndarray, but got {type(result[0])}"
    assert isinstance(result[1], np.ndarray), f"Expected np.ndarray, but got {type(result[1])}"

    # Проверяем, что массивы равны ожидаемым
    assert_array_equal(result[0], exp_arr1)
    assert_array_equal(result[1], exp_arr2)


def test_normal_point():
    point_n = np.array(
        [
            [0, 0], 
            [0, 1],  
            [0, 2],  
            [1, 0],  
            [1, 2],  
            [2, 0],  
            [2, 1],  
            [2, 2]
        ]
    )

    border_n = np.array(
        [
            [0, 1],
            [1, 0],
            [1, 2],
            [2, 1]
        ]
    )

    result = neighbours_for_point(1, 1) 
    check_arrays(result, point_n, border_n)


def test_low_border_point():
    point_n = np.array(
        [
            [0, 0], 
            [0, 1],  
            [1, 1],  
            [2, 0],  
            [2, 1],  
        ]
    )

    border_n = np.array(
        [
            [0, 0],
            [1, 1],
            [2, 0] 
        ]
    )

    result = neighbours_for_point(1, 0) 
    check_arrays(result, point_n, border_n)


def test_top_border_point():
    point_n = np.array(
        [
            [0, 998], 
            [0, 999],  
            [1, 998],  
            [2, 998],  
            [2, 999],  
        ]
    )

    border_n = np.array(
        [
            [0, 999],
            [1, 998],
            [2, 999] 
        ]
    )

    result = neighbours_for_point(1, 999) 
    check_arrays(result, point_n, border_n)


def test_right_border_point():
    point_n = np.array(
        [
            [998, 0], 
            [998, 1],  
            [998, 2],  
            [999, 0],  
            [999, 2],  
        ]
    )

    border_n = np.array(
        [
            [998, 1],  
            [999, 0],  
            [999, 2],
        ]
    )

    result = neighbours_for_point(999, 1) 
    check_arrays(result, point_n, border_n)

def test_left_border_point():
    point_n = np.array(
        [
            [0, 0], 
            [0, 2],  
            [1, 0],  
            [1, 1],  
            [1, 2],  
        ]
    )

    border_n = np.array(
        [
            [0, 0],  
            [0, 2],  
            [1, 1],
        ]
    )

    result = neighbours_for_point(0, 1) 
    check_arrays(result, point_n, border_n)

def test_left_bottom_corner_point():
    point_n = np.array(
        [
            [0, 1], 
            [1, 0],  
            [1, 1],  
        ]
    )

    border_n = np.array(
        [
            [0, 1],  
            [1, 0],  
        ]
    )

    result = neighbours_for_point(0, 0) 
    check_arrays(result, point_n, border_n)

def test_right_bottom_corner_point():
    point_n = np.array(
        [
            [998, 0], 
            [998, 1],  
            [999, 1],  
        ]
    )

    border_n = np.array(
        [
            [998, 0],  
            [999, 1],  
        ]
    )

    result = neighbours_for_point(999, 0) 
    check_arrays(result, point_n, border_n)

def test_right_top_corner_point():
    point_n = np.array(
        [
            [998, 998], 
            [998, 999],  
            [999, 998],  
        ]
    )

    border_n = np.array(
        [
            [998, 999],  
            [999, 998],  
        ]
    )

    result = neighbours_for_point(999, 999) 
    check_arrays(result, point_n, border_n)


def test_left_top_corner_point():
    point_n = np.array(
        [
            [0, 998], 
            [1, 998],  
            [1, 999],  
        ]
    )

    border_n = np.array(
        [
            [0, 998], 
            [1, 999],  
        ]
    )

    result = neighbours_for_point(0, 999) 
    check_arrays(result, point_n, border_n)


