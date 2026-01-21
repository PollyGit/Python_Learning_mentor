# 2

hours = [0, 2, 4,6, 3]
target = 2

def empl(hours, target):
    n = 0
    for i in hours:
        if i >= target:
            n += 1
    return n

print(f'количество сотрудников, отработавших {target} часов :', empl(hours, target))












#