import multiprocessing
import pyopencl as cl
import numpy as np
from numba import cuda, jit


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
        platform = cl.get_platforms()[0]
        device = platform.get_devices()[0]
        ctx = cl.Context([device])
        # Создаем очередь команд
        queue = cl.CommandQueue(ctx)
        # Компилируем код ядра
        prg = cl.Program(ctx, """
            __kernel void mergeSort(__global int *arr, int n) {
                if (n > 1) {
                    int mid = n / 2;
                    __global int* left = arr;
                    __global int* right = arr + mid;
                    mergeSort(left, mid);
                    mergeSort(right, n - mid);
                    int i = 0, j = mid, k = 0;
                    __global int* temp = (__global int*)cl_malloc(sizeof(int) * n, 0, 0);
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
                    cl_free(temp);
                }
            }
            """).build(options=['-cl-fast-relaxed-math'])
        # Определяем размер локальных и глобальных массивов
        global_size = arr.shape[0]
        local_size = 128
        # Создаем буферы памяти для передачи данных в ядро
        arr_gpu = cl.Buffer(ctx, cl.mem_flags.READ_WRITE, arr.nbytes)
        # Копируем данные в буфер
        cl.enqueue_copy(queue, arr_gpu, arr)
        # Выполняем ядро
        prg.mergeSort(queue, (global_size,), (local_size,), arr_gpu, np.int32(global_size))
        # Копируем результат обратно в массив
        cl.enqueue_copy(queue, arr, arr_gpu)
        return arr

    @cuda.jit
    def sort_gpu_cuda(arr, tmp, start, end):
        if start >= end:
            return

        mid = (start + end) // 2

        Sort.sort_gpu_cuda[arr, tmp, start, mid]
        Sort.sort_gpu_cuda[arr, tmp, mid + 1, end]

        i = start
        j = mid + 1
        k = start

        while i <= mid and j <= end:
            if arr[i] < arr[j]:
                tmp[k] = arr[i]
                i += 1
            else:
                tmp[k] = arr[j]
                j += 1
            k += 1

        while i <= mid:
            tmp[k] = arr[i]
            i += 1
            k += 1

        while j <= end:
            tmp[k] = arr[j]
            j += 1
            k += 1

        for i in range(start, end + 1):
            arr[i] = tmp[i]

    def merge_sort_gpu(arr):
        n = arr.shape[0]
        tmp = cuda.device_array(n, arr.dtype)
        Sort.merge_sort_gpu[arr, tmp, 0, n - 1]


arr = np.random.randint(0, 100, size=10)
print("Unsorted array: ", arr)
Sort.merge_sort_gpu(arr)
print("Sorted array: ", arr)
