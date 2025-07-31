import matplotlib.pyplot as plt

optimal_path = [0, 8, 7, 2, 3, 4, 5, 9, 1, 6, 0]
points_raw = [(1, 12), (0, 2), (5, 5), (10, 2), (4, 1), (4, 2), (0, 3), (5, 8), (7, 9), (3, 3)]
x = [1, 0, 5, 10, 4, 4, 0, 5, 7, 3]
y = [12, 2, 5, 2, 1, 2, 3, 8, 9, 3]
points = [points_raw[i] for i in optimal_path]

x_route = [x[i] for i in optimal_path]
y_route = [y[i] for i in optimal_path]

plt.figure(figsize=(8, 6))

# Рисуем точки
plt.plot(x, y, 'o', color='orangered', markersize=8)

# Рисуем стрелки между точками
for i in range(len(points)-1):
    plt.annotate("", 
                xy=points[i+1], 
                xytext=points[i],
                arrowprops=dict(arrowstyle="->", color='royalblue', lw=2))

# Стрелка от последней точки к первой (для замкнутого маршрута)
plt.annotate("", 
            xy=points[0], 
            xytext=points[-1],
            arrowprops=dict(arrowstyle="->", color='royalblue', lw=2))

# Подписи точек
for i, (xi, yi) in enumerate(points_raw):
    plt.text(xi, yi, f' {i}', fontsize=12, ha='left', va='bottom')

plt.grid(True)
plt.title('Маршрут коммивояжёра')
plt.show()