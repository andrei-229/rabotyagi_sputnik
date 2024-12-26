import json
import numpy as np
import matplotlib.pyplot as plt

# Скорость в ksp
with open('altitude_math_model.json', 'r') as f:
    y = json.load(f)

# Время в ksp
with open('x_math_model.json', 'r') as f:
    x = json.load(f)


x = np.array(x)
y = np.array(y)

plt.title('Траектория полёта по расчётам', fontsize=12, fontweight="bold") # Титульник на графике
plt.ylabel("y (м)", fontsize=14) # Описание функции y на графике
plt.xlabel("x (м)", fontsize=14) # Описание функции x на графике
plt.grid(True) # Вывод сетки
plt.plot(x , y, '-b', label='h(t)') # Вывод переменных на экран
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(10_000))
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(10_000))
plt.show() # Вывод графика