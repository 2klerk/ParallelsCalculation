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