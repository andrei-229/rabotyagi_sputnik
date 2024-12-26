import json
import matplotlib.pyplot as plt

with open('altitude_in_ksp.json') as f:
    altitude_in_ksp = json.load(f)

with open('altitude_math_model.json') as f:
    altitude_math_model = json.load(f)

with open('time_in_ksp.json') as f:
    time = json.load(f)

time = [time[i] - time[0] for i in range(len(time))]
altitude_in_ksp = altitude_in_ksp[:len(time)]
altitude_math_model = altitude_math_model[:len(time)]
# print(len(time), len(speed_in_ksp), len(speed_math_model))
print(len(altitude_in_ksp))
plt.title('График высоты полёта ракеты от времени. Сравнение', fontsize=12, fontweight="bold")
plt.ylabel("Высота y(t) (м)", fontsize=14)
plt.xlabel("Время t (с)", fontsize=14)
plt.grid()
plt.plot(time, altitude_in_ksp, '-r', label='h(t) ksp')
plt.plot(time, altitude_math_model, '-b', label='h(t) math')
plt.show()
