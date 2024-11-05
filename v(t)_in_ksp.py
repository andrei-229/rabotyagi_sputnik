import json
import numpy as np
import matplotlib.pyplot as plt

# Скорость в ksp
with open('speed_in_ksp.json', 'r') as f:
    speed_in_ksp = json.load(f)

# Время в ksp
with open('time_in_ksp.json', 'r') as f:
    time_in_ksp = json.load(f)

speed_in_ksp = speed_in_ksp[:len(time_in_ksp)]
x = np.array(time_in_ksp)
y = np.array(speed_in_ksp)
plt.title('График скорости ракеты от времени в KSP', fontsize=12, fontweight="bold") # Титульник на графике
plt.ylabel("Скорость V(t)", fontsize=14) # Описание функции y на графике
plt.xlabel("Время t", fontsize=14) # Описание функции x на графике
plt.grid(True) # Вывод сетки
plt.plot(x - time_in_ksp[0], y, '-r', label='v(t)') # Вывод переменных на экран
plt.show() # Вывод графика