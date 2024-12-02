import matplotlib.pyplot as plt
import json


time_to_out_atmosphere = 142
step = 0.08
with open('speed_math_model.json') as f:
    speed = json.load(f)

plt.title('График скорости ракеты от времени по расчётам', fontsize=12, fontweight="bold") # Титульник на графике

plt.ylabel("Скорость V(t)", fontsize=12) # Описание функции y на графике
plt.xlabel("Время t", fontsize=12) # Описание функции x на графике
plt.grid() # Вывод сетки
plt.plot(range(0 ,time_to_out_atmosphere + 6), speed[::int(step ** -1)])
plt.show()
