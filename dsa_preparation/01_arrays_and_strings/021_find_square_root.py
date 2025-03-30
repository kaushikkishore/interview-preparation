def find_square_root(num):
    left = 0
    right = num

    while left <= right:

        mid = left + (right - left) // 2
        square = mid * mid 
        if square == num:
            return mid 
        if square > num :
            right = mid -1 
        else:
            left = mid +1 
    return right


    
    

print(find_square_root(150))