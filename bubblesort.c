#include <stdio.h>
#include <stdbool.h>


// Function to swap two elements using pointers
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Recursive Bubble Sort function
void recursiveBubbleSort(int arr[], int n) {
    // Base Case: If array size is 1, it is already sorted
    if (n == 1) {
        return;
    }

    bool swapped = false;

    // One pass of bubble sort. 
    // Fixes the largest element of the current subarray at the end.
    for (int i = 0; i < n - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            swap(&arr[i], &arr[i + 1]);
            swapped = true;
        }
    }

    // Optimization: If no elements were swapped in this pass, the array is sorted
    if (!swapped) {
        return;
    }

    // Recursive Call: Sort the remaining n-1 elements
    recursiveBubbleSort(arr, n - 1);
}

// Function to print the array
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    int data[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(data) / sizeof(data[0]);
    
    printf("Original array: \n");
    printArray(data, n);
    
    recursiveBubbleSort(data, n);
    
    printf("Sorted array: \n");
    printArray(data, n);
    
    return 0;
}
