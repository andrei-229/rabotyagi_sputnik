import json
import numpy as np
import matplotlib.pyplot as plt

# Скорость в ksp
with open('time_in_ksp.json', 'r') as f:
    x = json.load(f)

# Время в ksp
with open('x_math_model.json', 'r') as f:
    y = json.load(f)


x = np.array(x)
y = np.array(y)
x = x[:len(y)]
print(len(x))

plt.title('График x ракеты от времени в KSP', fontsize=12, fontweight="bold") # Титульник на графике
plt.ylabel("x(t) (м)", fontsize=14) # Описание функции y на графике
plt.xlabel("Время t (с)", fontsize=14) # Описание функции x на графике
plt.grid(True) # Вывод сетки
plt.plot(x - x[0], y, '-r', label='h(t)') # Вывод переменных на экран
plt.show() # Вывод графика