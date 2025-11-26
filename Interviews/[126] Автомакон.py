# Напиши функцию для расчета accuracy/precision метрик прогноза

import numpy as np

predict = np.random.randint(0, 2, 10)
target = np.random.randint(0, 2, 10)

print(predict)
print(target)

count_match = 0

for i, j in zip(predict, target):
    if i == j:
        count_match += 1

accuracy = count_match/len(predict)
print(accuracy)























#