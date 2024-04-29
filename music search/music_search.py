# you may use pandas only for IO reason
# Using it to do sort will impact your grade
import pandas as pd
import random
import timeit
import math
import csv
import bisect

def timeFunc(method):
    """
    Define the main body of the decorator that decorates a method.
    Returns
    -------
    Callable
        A wrapper that defines the behavior of the decorated method
    """
    def wrapper(*args, **kwargs):
        """
        Define the behavior of the decorated method
        Parameters:
            Same as the parameters used in the methods to be decorated
        Returns:
            Same as the objects returned by the methods to be decorated
        """
        start = timeit.default_timer()
        result = method(*args, **kwargs)
        # record the time consumption of executing the method
        time = timeit.default_timer() - start
        # send metadata to standard output
        print(f"Method: {method.__name__}")
        print(f"Result: {result}")
        print(f"Elapsed time of 10000 times: {time*10000} seconds")
        return result
    return wrapper


class MusicLibrary:
    def __init__(self):
        """
        Initialize the MusicLibrary object with default values.
        self.data the collect of music library
        self.rows: the row number 
        self.cols: the col number 
        self.nameIndex: the number represent the index of name in each element of self.data
        self.albumIndex: the number represent the index of album in each element of self.data
        self.trackIndex: the number represent the index of track in each element of self.data
        """
        self.data = []
        self.rows = 0
        self.cols = 0
        self.nameIndex = 0
        self.albumIndex = 1
        self.trackIndex = 1

    def readFile(self, fileName):
        """
        Read music data from a CSV file and store it in the self.data attribute.
        The self.rows and self.cols should be updated accordingly. 
        The self.data should be [[name, albums count, tract count],...]
        You could assume the file is in the same directory with your code.
        Please research about the correct encoding for the given data set, 
        as it is not UTF-8.
        You are allowed to use pandas or csv reader, 
        but self.data should be in the described form above.

        Parameters
        ----------
        fileName : str
            The file name of the CSV file to be read.
        """
        df = pd.read_csv(fileName, encoding='ISO-8859-1', header=None)
        self.data = df.values.tolist()
        self.rows, self.cols = df.shape

    def printData(self):
        """
        Print the data attribute stored in the library instance in a formatted manner.
        """
        for row in self.data:
            print(row)

    def shuffleData(self):
        """
        Shuffle the data stored in the library.
        refer to the random package
        """
        random.shuffle(self.data)

    @timeFunc
    def binarySearch(self, key, keyIndex):
        """
        Perform a binary search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
    # Check if key is found
        low, high = 0, self.rows - 1
        while low <= high:
            mid = (low + high) // 2
            if self.data[mid][keyIndex] == key:
                return mid
            elif self.data[mid][keyIndex] < key:
                low = mid + 1
            else:
                high = mid - 1
        return -1
        # low = 0
        # high = self.rows -1
        # while low <= high:
        #     mid = (low + high) // 2
        #     if self.data[mid][keyIndex] == key:
        #         return mid
        #     elif self.data[mid][keyIndex] > key:
        #         high = mid + 1
        #     else:
        #         high = mid - 1
        # return -1
    @timeFunc
    def seqSearch(self, key, keyIndex):
        """
        Perform a sequential search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        for i in range(len(self.data)):
            if self.data[i][keyIndex] == key:
                return i
        return -1

    @timeFunc
    def bubbleSort(self, keyIndex):
        """
        Sort the data using the bubble sort algorithm based on a specific column index.
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        for i in range(self.rows):
            for j in range(0, self.rows-i-1):
                if self.data[j][keyIndex] > self.data[j+1][keyIndex]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]

    def merge(self, L, R, keyIndex):
        """
        Merge two sorted sublists into a single sorted list.
        This is the helper function for merge sort.
        You may change the name of this function or even not have it.
        Parameters
        ----------
        L, R : list
            The left and right sublists to merge.
        keyIndex : int
            The column index to sort by.
        Returns
        -------
        list
            The merged and sorted list.
        """
        merged_list = []
        while L and R:
            if L[0][keyIndex] < R[0][keyIndex]:
                merged_list.append(L.pop(0))
            else:
                merged_list.append(R.pop(0))
        merged_list.extend(L or R)
        return merged_list

    @timeFunc
    def mergeSort(self, keyIndex):
        """
        Sort the data using the merge sort algorithm.
        This is the main mergeSort function
        self.data will have to be in sorted order after calling this function.
        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        # Merge the sorted sublists
        self.data = self._mergeSort(self.data, keyIndex)

    def _mergeSort(self, arr, keyIndex):
    # This is the helper function for merge sort.
    # You may change the name of this function or even not have it.
    # This is a helper method for mergeSort
        if len(arr) <=1:
            return arr
        mid = len(arr) // 2
        left_half = self._mergeSort(arr[:mid], keyIndex)
        right_half = self._mergeSort(arr[mid:], keyIndex)
        return self.merge(left_half, right_half, keyIndex)

    @timeFunc
    def quickSort(self, keyIndex):
        """
        Sort the data using the quick sort algorithm.
        This is the main quickSort function
        self.data will have to be in sorted order after calling this function.
        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        self._quickSort(self.data, 0, len(self.data) -1, keyIndex)

    def _quickSort(self, arr, low, high, keyIndex):
    # This is a helper method for quickSort
        if low < high:
            pi = self.partition(arr, low, high, keyIndex)
            self._quickSort(arr, low, pi - 1, keyIndex)
            self._quickSort(arr, pi + 1, high, keyIndex)
            # if len(arr) <= 1:
        #     return arr
        # pivot = arr[len(arr) // 2][keyIndex]
        # left = [x for x in arr if x[keyIndex] < pivot]
        # middle = [x for x in arr if x[keyIndex] == pivot]
        # right = [x for x in arr if x[keyIndex] > pivot]
        # return self._quickSort(left, keyIndex) + middle + self._quickSort(right, keyIndex)

    def comment(self):
        '''
        Based on the result you find about the run time of calling different
        function,
        Write a small paragraph (more than 50 words) about time complexity, and
        print it.
        '''
        comment_text = """
        The time complexity of an algorithm is a measure of the amount of time it takes to complete as a function of the size of its input. Different sorting algorithms have different time complexities, which impact their performance on different datasets. For example, bubble sort has a time complexity of O(n^2), making it inefficient for large datasets, while quicksort and mergesort have average time complexities of O(n log n), making them more suitable for larger datasets. It's essential to consider the time complexity of algorithms when selecting the appropriate one for a particular task.
        """
        print(comment_text)

    # Create instance and call the following instance method
    # using decorator to decorate each instance method
    def main(self):
        random.seed(42)
        myLibrary = MusicLibrary()
        myLibrary.main()
        filePath = 'music.csv'
        myLibrary.readFile(filePath)
        idx = 0
        myLibrary.data.sort(key = lambda data: data[idx])
        myLibrary.seqSearch(key="30 Seconds To Mars", keyIndex=idx)
        myLibrary.binarySearch(key="30 Seconds To Mars", keyIndex=idx)
        idx = 2
        myLibrary.shuffleData()
        myLibrary.bubbleSort(keyIndex=idx)
        myLibrary.shuffleData()
        myLibrary.quickSort(keyIndex=idx)
        myLibrary.shuffleData()
        myLibrary.mergeSort(myLibrary.data, keyIndex=idx)
        myLibrary.printData()

# if __name__ == "__main__":
#     myLibrary = MusicLibrary()
#     myLibrary.main()