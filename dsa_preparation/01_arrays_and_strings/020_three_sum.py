def three_sum(nums):
    # Replace this placeholder return statement with your code
    # 01 Sort
    nums.sort()
    print(nums)
    result = []
    for idx, num in enumerate(nums):
        if num > 0:
            break

        if idx > 0 and nums[idx - 1] == num:
            continue
        left, right = 0, len(nums) - 1

        while right > left:
            if left == idx:
                left += 1
            if right == idx:
                right -= 1
            sum = nums[left] + nums[right] + num
            if sum == 0:
                result.append((nums[left], nums[right], num))
                left += 1
                right -= 1
            if sum < 0:
                left += 1
            if sum > 0:
                right -= 1
        # print("current idx",idx, num)
    return result


print(three_sum([-1, 0, 1, 2, -1, -4]))
