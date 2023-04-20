import multiprocessing
import pyopencl as cl
import numpy as np


class Sort:
    @staticmethod
    def merge_sort(arr):
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

    def mergeArray(self, arrayList):
        array = []
        for i in arrayList:
            print(i)
            array += arrayList[i]["Data"]
        return array

    @staticmethod
    def merge_sort_parallel(arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_arr = arr[:mid]
            right_arr = arr[mid:]

            with multiprocessing.Pool(processes=2) as pool:
                left_arr = pool.apply(Sort.merge_sort_parallel, [left_arr])
                right_arr = pool.apply(Sort.merge_sort_parallel, [right_arr])

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

    def sort_gpu(arr):
        # Создаем контекст OpenCL
        ctx = cl.create_some_context()
        # Создаем очередь команд
        queue = cl.CommandQueue(ctx)
        # Компилируем код ядра
        prg = cl.Program(ctx, """
            __kernel void mergeSort(__global int *arr, int n) {
                if (n > 1) {
                    int mid = n / 2;
                    int* left = arr;
                    int* right = arr + mid;
                    mergeSort(left, mid);
                    mergeSort(right, n - mid);
                    int i = 0, j = mid, k = 0;
                    int* temp = (int*)malloc(sizeof(int) * n);
                    while (i < mid && j < n) {
                        if (left[i] < right[j]) {
                            temp[k] = left[i];
                            i++;
                        }
                        else {
                            temp[k] = right[j];
                            j++;
                        }
                        k++;
                    }
                    while (i < mid) {
                        temp[k] = left[i];
                        i++;
                        k++;
                    }
                    while (j < n) {
                        temp[k] = right[j];
                        j++;
                        k++;
                    }
                    for (int l = 0; l < n; l++) {
                        arr[l] = temp[l];
                    }
                    free(temp);
                }
            }
            """).build()

        # Создаем буфер в GPU
        arr_gpu = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, arr.nbytes)
        # Копируем массив на видеокарту
        cl.enqueue_copy(queue, arr_gpu, arr)
        # Вызываем сортировку
        prg.mergeSort(queue, arr.shape, None, arr_gpu, np.int32(arr.shape[0]))
        # Копируем отсортированный массив обратно в ОЗУ
        cl.enqueue_copy(queue, arr, arr_gpu)
        return arr
