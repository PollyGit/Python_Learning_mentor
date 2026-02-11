# 1


nums = [8, 8, 7, 10, 5, 7, 8]
target  = 8

def find(nums, target):
    out = []
    nums2 = sorted(nums)
    for i in range(len(nums2)):
        if nums2[i] == target:
            out.append(i)
    if len(out) == 0:
        return [-1, -1]
    elif len(out) > 2:
        a1 = min(out)
        a2 = max(out)
        out = [a1, a2]
    return out


print(find(nums, 8))








