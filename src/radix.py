"""Radix sorting module."""
from collections import OrderedDict
from collections import deque
def count_sort(x: str) -> str:
    """Count-sort the string x.

    >>> count_sort('abaab')
    'aaabb'
    >>> count_sort('')
    ''
    """
    sorted_word = ''.join(sorted(x))
    return sorted_word


def bucket_sort(x: str, idx: list[int]) -> list[int]:
    #Bucket-sort the indices in idx using keys from the string x.
   
    # scan through x and count how often you see each character.
    countOfChars = dict()
    for char in x:
        try:
            countOfChars[char] += 1
        except KeyError:
            countOfChars[char] = 1
    countOfChars = OrderedDict(sorted(countOfChars.items()))    #sort elements in buckets
    # buckets: compute the cummulative sun of the table
    ## make a new table where for key k you have the number of letters with keys k' smaller than k
    buckets = dict()
    cumSum = 0
    for key, value in countOfChars.items():
        buckets[key] = cumSum
        cumSum = cumSum + value
    out = [None] * len(idx)
    for i in idx:
        pos = buckets[x[i]] 
        out[pos] = i
        buckets[x[i]] += 1
    return out, buckets

def key(x:str, col:int): 
    col_x = ''
    for i in range(0, len(x)):
        if  i + col < len(x):
            col_x = "".join([col_x, x[i+col]])
        else:
            col_x = "".join([col_x, '0'])
    return col_x

def lsd_radix_sort(x: str) -> list[int]:
#Compute the suffix array for x using a least-significant digit radix sort.

    # need to add 0 otherwise output differs
    x = "".join([x,'0'])
    idx = range(0, len(x))
    for col in reversed(idx):
        x_col = key(x, col)
        idx, buckets = bucket_sort(x_col, idx)
    
    return idx

def key_2(x:str, col:int, idx:list[int]): 
    col_x = ''
    for i in idx:
        if  i + col < len(x):
            col_x = "".join([col_x, x[i+col]])
        else:
            col_x = "".join([col_x, '0'])
    return col_x

def msd_radix_sort(x: str) -> list[int]:
    """
    Compute the suffix array for x using a most-significant digit radix sort.

    >>> msd_radix_sort('abaab')
    [5, 2, 3, 0, 4, 1]
    >>> msd_radix_sort('mississippi')
    [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    """
    x = "".join([x,'0'])
    idx = range(0, len(x))
    col = 0
    sub_range = [0, col]
    que = deque([(col, idx, idx)])
    # stack = [[col, idx, idx]]
    while len(que) != 0 and col < len(x):
        col, idx, sub_range = que.popleft()
        # for each bucket call sort
        if len(idx) > 1:
            x_col = key_2(x, col, idx)
            idx, buckets = bucket_sort2(x, x_col, idx, col)
            old_value = 0
            for key, value in buckets.items():
                if value != old_value:
                    que.append([col+1, idx[old_value:int(value)], [old_value, int(value)]])
                    old_value = int(value)
        else:
            que.append([col+1, idx, None])
    
    result = []
    while len(que) != 0:
        col, idx, sub_range = que.popleft()
        result += idx
    #not pretty, but it works
    result = [result[len(result)-1]] + result[0:len(result)-1]
    return result


def bucket_sort2(x_original: str, x: str, idx: list[int], col: int) -> list[int]:
#Bucket-sort the indices in idx using keys from the string x.

# scan through x and count how often you see each character.
    countOfChars = dict()
    for char in x:
        try:
            countOfChars[char] += 1
        except KeyError:
            countOfChars[char] = 1
    countOfChars = OrderedDict(sorted(countOfChars.items()))    #sort elements in buckets
    # buckets: compute the cummulative sun of the table
    ## make a new table where for key k you have the number of letters with keys k' smaller than k
    buckets = dict()
    cumSum = 0
    for key, value in countOfChars.items():
        buckets[key] = cumSum
        cumSum = cumSum + value
    out = [None] * len(x)
    for i in idx:
        pos = buckets[x_original[i+col]] 
        out[pos] = i
        buckets[x_original[i+col]] += 1
    return out, buckets

#test
def main():
    #print(count_sort('abaab'))
    #print(count_sort(''))
    #print(bucket_sort('abaab', [0, 1, 2, 3, 4]))
    #print(bucket_sort('', []))
    #print(bucket_sort('abaab', [4, 3, 2, 1, 0]))
    #print(lsd_radix_sort('abaab'))
    #    [5, 2, 3, 0, 4, 1]
    #print(lsd_radix_sort('mississippi'))
    #    [11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    print(msd_radix_sort('aba'))
    print(msd_radix_sort('abaab'))
    #[5, 2, 3, 0, 4, 1]
    print(msd_radix_sort('mississippi'))
    #[11, 10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]



if __name__ == '__main__':
    main()