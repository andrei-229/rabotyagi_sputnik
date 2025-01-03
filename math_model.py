import math
import matplotlib.pyplot as plt
import json

# Массы
m_all = 58_000 # Масса всей ракеты
m_srbs = 14_250 # Масса твердотопливных ускорителлей
m_srbs_fuel_kg = 11_240 # Масса твердого топлива
m_liquid = 36_000 # Масса топливного бака
m_liquid_fuel_kg = 32_000 # Масса жидкого топлива с окислителем
m_vessel_without_srbs = 35_750 # Масса ракеты без твердотопливных ускорителей

# Удельный импульс
I_ud_srbs = 230 # Удельный импульс твердотопливных ускорителей
I_ud_luquid = 320 # Удельный импульс жидкого двигателя и после откреплления твердотопловных ускорителей
I_ud = 550 # Удельный импульс до открепления твердотопливных ускорителей

# Тяга
Ft_srbs_start = 270 # Тяга твердотопливных ускорителей(4) в начале с 33.5 % мощностью
Ft_srbs_end = 300 # Тяга твердотопливных ускорителей(4) с 33.5 % мощностью перед их откреплением
Ft_liquid_start = 570 # Тяга жидкого двигателя в начале
Ft_liquid_end = 650_000 # Тяга жидкого двигателя при откреплении твердотопливных ускорителей
Ft_liquid_25 = 162_000 # Тяга жидкого двигателя при 25%
Ft_start = 840_000 # Суммарная тяга в начале
Ft_end = 950_000 # Суммарная тяга при откреплении твердотопливных ускорителей
Ft_average = 870_000 # Средняя суммарная тяга перед откреплением твердотпливных ускорителей 

# Время
time_srbs_separate = 82 # Время работы твердотопливных ускорителей
time_liquid_to_25 = 122 # Время работы жидкого двигателя до уменьшения его тяги с 100 до 25 %
time_liquid_to_0 = 132 # Время работы жидкого двигателя до уменьшения его тяги с 25 до 0 %
time_to_out_atmosphere = 142 # Время до выхода за пределы атмосферы

# Расход топлива на разных этапах
k_to_srbs_separate = (m_srbs_fuel_kg + m_liquid_fuel_kg / 2.15) / (time_srbs_separate) # Расход топлива до открелпения твердотопливных ускорителей (исрасходовалось 0.535 жидкого топлива) - 318.582
k_to_liquid_25 = (m_liquid_fuel_kg / 2.15 - m_liquid_fuel_kg / 4.55) / (time_liquid_to_25 - time_srbs_separate) # Расход топлива до уменьшения тяги жидкого двигателя до 25 % - 196.269
k_liquid_from_25_to_0 = (m_liquid_fuel_kg / 2.15 - m_liquid_fuel_kg / 4.55 - m_liquid_fuel_kg / 5) / (time_liquid_to_0 - time_liquid_to_25) # Расход топлива до уменьшения тяги жидкого двигателя до 0 % - 145.075

# Константы
e = 2.72 # Эксопнента
g = 9.81 # Ускорение свободного падения
pi = 3.1416 # Число Пи
da = 0.6375 # Изменение угла в секунду - 0.6375 градусов
Cf = 0.5 # Коэффицент сопротивления воздуха для ракеты
d = 4.7 # Ширина-диаметр ракеты
s = 17.35 # Площадь ракеты
M_A = 0.29 # Молярная масса (29 г/моль для сухого воздуха)
R = 8.31 # Универсальная газовая постоянная
T = 300 # Температура
P_0 = 10 ** 5 # Давление
GAZ_P = M_A / (R * T)

ax_values = [0]
ay_values = [-9.81]
vx_values = [0]
vy_values = [0]
x_values = [0]
y_values = [0]


x = 0
y = 0
vx = 0
vy = 0
ax = 0
ay = 0

step = 0.08
for i in range(int(time_to_out_atmosphere // step)):
    t = i * step

    ro = GAZ_P * P_0 * (e ** (-g * y * GAZ_P)) # Плотность воздуха (изменяется с изменением высоты)
    Fs_x = Cf * s * ro * vx_values[-1] ** 2 / 2 # Сила сопротивления воздуха
    Fs_y = Cf * s * ro * vy_values[-1] ** 2 / 2

    # 2 закон Ньютона на разных временных этапах
    if t < time_srbs_separate:
        ax = (Ft_average * math.cos((90 - da * t) * pi / 180) - Fs_x) / (m_all - k_to_srbs_separate * t)
        ay = (Ft_average * math.sin((90 - da * t) * pi / 180) - Fs_x) / (m_all - k_to_srbs_separate * t) - g * math.sin((90 - da * t) * pi / 180)

    elif time_srbs_separate < t < time_liquid_to_25:
        ax = (Ft_liquid_end * math.cos((90 - da * t) * pi / 180) - Fs_x) / (m_vessel_without_srbs - k_to_liquid_25 * (t - time_srbs_separate))
        ay = (Ft_liquid_end * math.sin((90 - da * t) * pi / 180) - Fs_x) / (m_vessel_without_srbs - k_to_liquid_25 * (t - time_srbs_separate)) - g * math.sin((90 - da * t) * pi / 180)
    
    elif time_liquid_to_25 < t < time_liquid_to_0:
        ax = (Ft_liquid_25 * math.cos((90 - da * t) * pi / 180) - Fs_x) / (m_vessel_without_srbs - k_liquid_from_25_to_0 * (t - time_srbs_separate))
        ay = (Ft_liquid_25 * math.sin((90 - da * t) * pi / 180) - Fs_x) / (m_vessel_without_srbs - k_liquid_from_25_to_0 * (t - time_srbs_separate)) - g * math.sin((90 - da * t) * pi / 180)
    
    elif time_liquid_to_0 < t < time_to_out_atmosphere:
        ax = -Fs_x / (m_vessel_without_srbs - k_liquid_from_25_to_0 * (t - time_srbs_separate))
        ay = -Fs_x / (m_vessel_without_srbs - k_liquid_from_25_to_0 * (t - time_srbs_separate)) - g * math.sin((90 - da * t) * pi / 180)
    
    vx = vx_values[-1] + ax * step
    vy = vy_values[-1] + ay * step
    x = x_values[-1] + vx * step
    y = y_values[-1] + vy * step

    ax_values.append(ax)
    ay_values.append(ay)
    vx_values.append(vx)
    vy_values.append(vy)
    x_values.append(x)
    y_values.append(round(y,2))
    if t == 80:
        print(f'{round((vx_values[-1] ** 2 + vy_values[-1] ** 2) ** 0.5, 4)} м/с, шаг = {step}, t = {t} c')
    if t == 120:
        print(f'{round((vx_values[-1] ** 2 + vy_values[-1] ** 2) ** 0.5, 4)} м/с, шаг = {step}, t = {t} c')
    if t == 50:
        print(f'{round((vx_values[-1] ** 2 + vy_values[-1] ** 2) ** 0.5, 4)} м/с, шаг = {step}, t = {t} c')
    if t == 132:
        print(f'{round((vx_values[-1] ** 2 + vy_values[-1] ** 2) ** 0.5, 4)} м/с, шаг = {step}, t = {t} c')


speed = [round((vx_values[i] ** 2 + vy_values[i] ** 2) ** 0.5, 4) for i in range(len(vx_values))] # Вычисление скорости и запись значений в массив

with open('speed_math_model.json', 'w') as f:
    json.dump(speed, f)
with open('altitude_math_model.json', 'w') as f:
    json.dump(y_values, f)

