import krpc
import math
import time
import json

time.sleep(3)

turn_start_altitude = 250
turn_end_altitude = 45_000
target_altitude = 150_000

conn = krpc.connect(name = "sputnik")
vessel = conn.space_center.active_vessel # Наша ракета
print(vessel.name)

# Set up streams for telemetry
ut = conn.add_stream(getattr, conn.space_center, 'ut') # getattr достаёт атрибут "времени"
m_all = vessel.mass # Масса всей ракеты
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude') # Достаём высоту
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude') # Достаём апоапсис(апогеию)
stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False) # Достаём ресурсы для 2 ступени - твердое топливо
'''
Как видит метод resources_in_decoulpe_stage() ступени

for i in range(-2,4):
 print(f'Stage {i}: {vessel.resources_in_decouple_stage(stage=i, cumulative=False).names}')
Stage -2: []
Stage -1: ['ElectricCharge', 'MonoPropellant']
Stage 0: []
Stage 1: ['LiquidFuel', 'Oxidizer', 'ElectricCharge']
Stage 2: ['SolidFuel']
Stage 3: []
'''

srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel') # Масса твёрдого топлива 


# Pre-Launch setup
vessel.control.sas = False 
vessel.control.rcs = False  
vessel.control.throttle = 1.0 # Тяга 100%

#Countdown
print(3)
time.sleep(1)
print(2)
time.sleep(1)
print(1)
time.sleep(1)
print('Start!')
# print(ut())
print()


vessel.control.activate_next_stage() # Переход на следующую ступень(запуск)
vessel.auto_pilot.engage() # Активация автопилота
vessel.auto_pilot.target_pitch_and_heading(90, 90) # Тангаж и рыскание строго вертикально(начальное направление)

# f_for_impulse = 0
srbs_separeted = False # Флаг для отсоединения топливного бака
turn_angle = 0
new_turn_angle = 0
time_values = []
speed_values = []
altitude_values = []
angle_values = []

while True:
    t = round(ut(), 4) # Получение значения текущего времени
    v = round(vessel.flight(vessel.orbit.body.reference_frame).speed, 4) # Получение значения текущей скорости
    h = round(altitude(), 4) # Получение значения текущей высоты
    time_values.append(t)
    speed_values.append(v)
    altitude_values.append(h)

    # Постепенный "поворот" ракеты при повышении высоты
    if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
        frac = (altitude() - turn_start_altitude) / (turn_end_altitude - turn_start_altitude) # Соотношение пройденного пути ко всему
        new_turn_angle = 90 * frac # Угол поворота в зависимости от набранной высоты(соотношения)
        angle_values.append(new_turn_angle)
        if abs(new_turn_angle - turn_angle) > 0.5:
            turn_angle = new_turn_angle
            vessel.auto_pilot.target_pitch_and_heading(90 - turn_angle, 90) # Поворот ракеты на новый угол
    
    # Отсоединение топливных баков, когда закончится топливо
    if not srbs_separeted:
        # if srb_fuel() < 0.2 and not f_for_impulse:
        #     ue = vessel.specific_impulse
        #     print(ue)
        #     f_for_impulse = 1
        if srb_fuel() < 0.1:
            # print(ut())
            vessel.control.activate_next_stage()
            srbs_separeted = True
            print('Открепление топливных баков')

    # Уменьшение тяги при уменьшении сопротивления от атмосферы (при приближении апогеи ракеты к целевой апогее)
    if apoapsis() > target_altitude * 0.9:
        print('Приближаемся к апогее')
        break

# print(ut())
# ue = vessel.specific_impulse
# print(ue)

vessel.control.throttle = 0.25

# Отключение двигателей, когда достигнем целевой апогеи
while apoapsis() < target_altitude:
    t = round(conn.space_center.ut, 4) # Получение значения текущего времени
    v = round(vessel.flight(vessel.orbit.body.reference_frame).speed, 4) # Получение значения текущей скорости
    h = round(altitude(), 4) # Получение значения текущей высоты 
    time_values.append(t)
    speed_values.append(v)
    altitude_values.append(h)
    pass

print('Апогея достигнута')
vessel.control.throttle = 0.0

# print(ut())
# ue = vessel.specific_impulse
# print(ue)

# Ждем, пока не выйдем из атмосферы
print('Выход за пределы атмосферы')
while altitude() < 70_500:
    t = round(conn.space_center.ut, 4) # Получение значения текущего времени
    v = round(vessel.flight(vessel.orbit.body.reference_frame).speed, 4) # Получение значения текущей скорости 
    h = round(altitude(), 4) # Получение значения текущей высоты
    time_values.append(t)
    speed_values.append(v)
    altitude_values.append(h)
    pass

# Запсиь скорости, времени и высоты в файл для дальнейшего использования в построении графиков
time_values = sorted(set(time_values))
speed_values = sorted(set(speed_values))
altitude_values = sorted(set(altitude_values))
angle_values = sorted(set(angle_values))
with open('speed_in_ksp.json', 'w') as f:
    json.dump(speed_values, f)
with open('time_in_ksp.json', 'w') as f:
    json.dump(time_values, f)
with open('altitude_in_ksp.json', 'w') as f:
    json.dump(altitude_values, f)
with open('angle_in_ksp.json', 'w') as f:
    json.dump(angle_values, f)

# print(ut())
# ue = vessel.specific_impulse
# print(ue)

# Вычисление приращение скорости для выхода на круговую орбиту (используя уравнение vis-viva(Бургаса))
print('Вычисление приращения скорости для выхода на круговую орбиту')
mu = vessel.orbit.body.gravitational_parameter # Гравитационный параметр мю
r = vessel.orbit.apoapsis # Расстояние между спутником и землёй(двумя центрами масс)
a = vessel.orbit.semi_major_axis # Длина большой полуоси
v1 = math.sqrt(mu * (2/r - 1/a))
v2 = math.sqrt(mu * (2/r - 1/r))
dv = v2 - v1
node = vessel.control.add_node(ut() + vessel.orbit.time_to_apoapsis, prograde = dv) # Создание узла манёвра дельта-v в прямом направлении

# time.sleep(1)

# Вычисление время манёвра (используя уравнение ракеты Циалковского)
F = vessel.available_thrust # Тяга
Im = vessel.specific_impulse * 9.82 # Удельный импульс - Эффективная скорость выхлопа.
m0 = vessel.mass
m1 = m0 / math.exp(dv / Im) # Конечная масса без топлива
flow_rate = F / Im # Расход 
burn_time = (m0 - m1) / flow_rate # Время манёвра

# print(burn_time)
# time.sleep(1)

# Ориентация корабля
print('Ориентация корабля для округления орбиты')
vessel.auto_pilot.reference_frame = node.reference_frame # Задаём кораблю систему отсчёта, которая фиксирована относительно узла маневра
vessel.auto_pilot.target_direction = (0, 1, 0) # Задаём вектор направления (по оси Y - в направлении облета)
vessel.auto_pilot.wait() # Отправляем в "сон" автопилот

# time.sleep(1)

# Ждем пока долетил/округлит орбиту
print('Ждем пока округлит орбиту')
burn_ut = ut() + vessel.orbit.time_to_apoapsis - burn_time / 2 # Время "прибытия"
lead_time = 5 # останавливаем перемотку за 5 секунд до конечной цели
conn.space_center.warp_to(burn_ut - lead_time) # Перематываем время до момента достижения апогеи

# Манёвр(торможение)
print('Готов к манёвру')
time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis') # время до апогеи, когда надо будет совершить манёвр для наивысшей эффективности
while time_to_apoapsis() - (burn_time/2) > 0:
    pass
print('Осуществление манёвра')
vessel.control.throttle = 1.0
time.sleep(burn_time - 0.1)
print('Тонкая настройка')
vessel.control.throttle = 0.05
remaining_burn = conn.add_stream(node.remaining_burn_vector, node.reference_frame) # Задаём вектор направления
while remaining_burn()[1] > 0 and ut() < 450:
    pass
vessel.control.throttle = 0.0
node.remove()

print('Запуск завершён')