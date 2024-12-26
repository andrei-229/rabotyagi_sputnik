import json
import numpy as np
import matplotlib.pyplot as plt

# Скорость в ksp
with open('altitude_in_ksp.json', 'r') as f:
    altitude_in_ksp = json.load(f)

# Время в ksp
with open('time_in_ksp.json', 'r') as f:
    time_in_ksp = json.load(f)

altitude_in_ksp = altitude_in_ksp[:len(time_in_ksp)]

x = np.array(time_in_ksp)
y = np.array(altitude_in_ksp)
print(len(x))
print(len(y))
plt.title('График высоты полёта ракеты от времени в KSP', fontsize=12, fontweight="bold") # Титульник на графике
plt.ylabel("Высота y(t) (м)", fontsize=14) # Описание функции y на графике
plt.xlabel("Время t (c)", fontsize=14) # Описание функции x на графике
plt.grid(True) # Вывод сетки
plt.plot(x - time_in_ksp[0], y, '-r', label='h(t)') # Вывод переменных на экран
plt.show() # Вывод графика