import math
import matplotlib.pyplot as plt
import json

time_to_out_atmosphere = 142
step = 0.08
with open('altitude_math_model.json') as f:
    y_values = json.load(f)


plt.title('График высоты полёта ракеты от времени по расчётам', fontsize=12, fontweight="bold") # Титульник на графике
plt.ylabel("Высота y(м)", fontsize=12) # Описание функции y на графике
plt.xlabel("Время t(с)", fontsize=12) # Описание функции x на графике
plt.grid() # Вывод сетки
plt.plot(range(0, 148), y_values[::int(step ** -1)])
plt.show()

