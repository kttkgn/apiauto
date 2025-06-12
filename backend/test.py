from collections import Counter

def sort_by_frequency(arr):
    counter = Counter(arr)
    print(counter)
    # 根据频率倒序排序，如果频率相同可按值本身排序
    sorted_arr = sorted(arr, key=lambda x: (-counter[x], x))


    return sorted_arr

# 示例
arr = [3, 1, 2, 2, 4, 3, 3, 1, 2]
print(sort_by_frequency(arr))  # 输出: [3,