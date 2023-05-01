import multiprocessing
from multiprocessing import freeze_support

# import pyopencl as cl
import numpy as np


# import time


class Sort:
    @staticmethod
    def merge_sort(arr):
        print(arr)
        if len(arr) > 1:
            mid = len(arr) // 2
            left_arr = arr[:mid]
            right_arr = arr[mid:]

            Sort.merge_sort(left_arr)
            Sort.merge_sort(right_arr)

            i = j = k = 0

            while i < len(left_arr) and j < len(right_arr):
                if left_arr[i] < right_arr[j]:
                    arr[k] = left_arr[i]
                    i += 1
                else:
                    arr[k] = right_arr[j]
                    j += 1
                k += 1

            while i < len(left_arr):
                arr[k] = left_arr[i]
                i += 1
                k += 1

            while j < len(right_arr):
                arr[k] = right_arr[j]
                j += 1
                k += 1

        return arr

    @staticmethod
    def mergeArray(arrayList):
        array = []
        for i in arrayList:
            print(i)
            array += arrayList[i]["Data"]
        return array

# array = [2,1,5,21,3213,5,1,2,521,5,99,34,6456]
# S = Sort()
# array = S.merge_sort(array)
# print(array)
