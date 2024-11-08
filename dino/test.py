#!/usr/bin/env python3

class A:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        # return f"x : {self.x} y : {self.y}"
        # return f"{self.x}"
        return f"({self.x},{self.y})"


arr = [
    A(3,2),
    A(3,3),
    A(2,2),
    A(1,1),
    A(2,1),
    A(2,2),
    A(0,1),
    A(2,5),
    A(0,100)
]

# arr2 = sorted(arr, key=lambda a: a.x)
print(arr)
arr.sort(key=lambda a:a.x)


# print(arr2)
print(arr)

print(1 + 2 * 3)
print(10 / 2 + 1)
print(abs(2 - 10))

# lst = [1,2,3,4,5]
# it = iter(lst)

# for element in lst:
#     print(element)
#     next_element = next(it, None)
#     print(element, next_element)

my_list = [1, 2, 3, 4, 5]
iterator = iter(my_list)

for item in iterator:
    next_item = next(iterator, None)  # Get the next element or None if there is no next element
    next_next = next(iterator, None)
    print(item, next_item, next_next)



debug = True
if debug: print("Hello")

# NEJAK TAKTO

# from itertools import tee, islice

# my_list = [1, 2, 3, 4, 5]
# iterator = iter(my_list)

# for item in iterator:
#     print(f"Current: {item}")

#     # Duplicate the iterator to peek ahead
#     next_iterator, next_next_iterator = tee(iterator, 2)
    
#     # Peek the next element or None
#     next_item = next(next_iterator, None)
#     print(f"Next: {next_item}")
    
#     # Peek the next of the next element or None
#     next_next_item = next(islice(next_next_iterator, 1, None), None)
#     print(f"Next of the Next: {next_next_item}")
