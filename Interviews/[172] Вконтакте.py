# Задача1.
# Вводим текст с клавиатуры. Плохо работает клавиша: а = аа. Вывести ТОЧНО правильно работающие клавиши
# Ввод: abbccb
# Вывод: ab

t = 'abbccb'
t3 = 'aabbbcdabcd'

def good_buttons(t: str):
    t2 = ''
    if t[1] != t[0]:
        t2 += t[0]
    for i in range(1, len(t)-1):
        if t[i] != t[i-1] and t[i] != t[i+1]:
            t2 += t[i]
    if t[-1] != t[-2]:
        t2 += t[-1]
    print(t2)


good_buttons(t)


# or
def good_buttons2(t):
    t2 = ''
    for i in range(len(t)):
        prev = t[i - 1] if i > 0 else None
        curr = t[i]
        next_ = t[i + 1] if i < len(t) - 1 else None
        if curr != prev and curr != next_:
            t2 += curr
    return t2

print(good_buttons2(t))
