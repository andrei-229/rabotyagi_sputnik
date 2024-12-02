import json

with open ('angle_in_ksp.json') as f:
    angle_values = json.load(f)

m = []
for i in range(1, len(angle_values)):
    m.append(angle_values[i] - angle_values[i - 1])


average_angle_turn = sum(m) / len(m)
average_angle_turn_in_second = sum(m) / 141  # Среднее изменение угла при полёте ракеты в секунду - 0.6375 градусов
print(average_angle_turn_in_second)
