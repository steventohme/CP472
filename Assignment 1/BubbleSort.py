def bubble_sort(arr):
    # check if the input is a list
    if not isinstance(arr, list):
        print("Error: Input is not a list")
        return

    # check if the input has values
    if len(arr) == 0:
        print("Error: Input is empty")
        return

    # check if all values are integers (to keep everything simple)
    for i in arr:
        if not isinstance(i, int):
            print("Error: Input contains non-integer values")
            return
    
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j+1] :
                temp = arr[j]
                arr[j] = arr[j+1]
                arr[j+1] = temp
    
    return arr

if __name__ == "__main__":
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(bubble_sort(arr))