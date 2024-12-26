import json
import matplotlib.pyplot as plt

with open('speed_in_ksp.json') as f:
    speed_in_ksp = json.load(f)

with open('speed_math_model.json') as f:
    speed_math_model = json.load(f)

with open('time_in_ksp.json') as f:
    time = json.load(f)

time = [time[i] - time[0] for i in range(len(time))]
speed_in_ksp = speed_in_ksp[:len(time)]
speed_math_model = speed_math_model[:len(time)]
print(len(time), len(speed_in_ksp), len(speed_math_model))

plt.title('График скорости ракеты от времени. Сравнение', fontsize=12, fontweight="bold")
plt.ylabel("Скорость v(t) (м/с)", fontsize=14)
plt.xlabel("Время t (c)", fontsize=14)
plt.grid()
plt.plot(time, speed_in_ksp, '-r', label='v(t) ksp')
plt.plot(time, speed_math_model, '-b', label='v(t) math')
plt.show()

