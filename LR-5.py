import matplotlib.pyplot as plt

x1_0 = [1.0, 1.1, 0.9, 0.9, 0.8, 1.1, 1.0, 1.2, 1.2, 1.1, 0.8, 0.8, 0.8, 1.1, 0.8, 1.0, 0.9, 1.2, 1.2, 1.2, 2.8, 3.8, 4.8, 1.5, 6.0, 10.0, 5.9, 0.2, 12.0, 0.12]
x1_2 = [2.1, 2.2, 2.0, 1.9, 2.0, 2.2, 2.1, 1.8, 2.0, 1.9, 2.0, 2.2, 1.8, 2.2, 1.9, 1.8, 2.0, 2.2, 2.2, 2.0, 2.0, 3.2, 3.8, 2.7, 4.9, 11.8, 7.0, 2.2, 22.0, 0.25]
x1_4 = [2.9, 3.2, 3.0, 3.2, 2.9, 3.2, 3.1, 3.2, 3.0, 3.2, 2.8, 2.9, 2.9, 3.0, 3.2, 2.8, 2.8, 3.0, 3.2, 3.2, 1.8, 2.9, 2.9, 3.2, 4.2, 12.8, 8.8, 2.6, 32.0, 0.55]
x1_6 = [3.8, 4.2, 3.8, 3.8, 4.2, 4.2, 3.8, 4.1, 3.8, 3.8, 4.0, 4.0, 4.0, 4.1, 4.1, 3.8, 3.8, 4.0, 3.8, 4.2, 1.6, 3.0, 2.0, 4.0, 4.5, 13.5, 8.8, 2.9, 38.0, 0.42]
x1_8 = [5.2, 5.2, 5.1, 5.1, 5.2, 5.1, 5.2, 5.2, 5.0, 4.9, 5.2, 5.2, 4.9, 4.9, 5.0, 4.8, 4.9, 4.8, 4.8, 4.8, 2.2, 4.2, 1.9, 4.5, 5.0, 14.3, 7.9, 3.1, 48.0, 0.48]
x2_0 = [5.9, 6.0, 5.8, 6.1, 5.8, 5.9, 6.2, 6.1, 6.1, 5.8, 6.0, 5.8, 6.1, 5.9, 6.0, 5.8, 6.2, 5.8, 6.0, 6.1, 3.0, 4.8, 1.1, 4.9, 6.0, 15.0, 6.2, 3.2, 60.0, 0.6]

def runing_method(A, B, C, F):
    n = len(A)
    alpha = [0] * (n + 1)
    beta = [0] * (n + 1)
    y = [0] * (n + 1)

    for i in range(1, n - 1):
        alpha[i + 1] = B[i] / (C[i] - alpha[i] * A[i])
        beta[i + 1] = (A[i] * beta[i] + F[i]) / (C[i] - alpha[i] * A[i])

    for i in range(n - 1, -1, -1):
        y[i] = alpha[i + 1] * y[i + 1] + beta[i + 1]

    return y

def cubic_spline(Xs, Ys, x_value):
    n = len(Xs)
    h = [0] * n
    for i in range(1, n): h[i] = Xs[i] - Xs[i - 1]

    A,B,C,F = [0] * (n - 1),[0] * (n - 1),[0] * (n - 1),[0] * (n - 1)
    a,b,c,d = [0] * n, [0] * n, [0] * n, [0] * n

    for i in range(1, n - 1):
        A[i] = h[i]
        C[i] = -2 * (h[i] + h[i + 1])
        B[i] = h[i + 1]
        F[i] = -6 * ((Ys[i + 1] - Ys[i]) / h[i + 1] - (Ys[i] - Ys[i - 1]) / h[i])

    c = runing_method(A, B, C, F)
    a[0] = Ys[0]

    for i in range(1, len(c)):
        a[i] = Ys[i]
        d[i] = (c[i] - c[i - 1]) / h[i]
        b[i] = h[i] / 2 * c[i] - h[i] ** 2 / 6 * d[i] + (Ys[i] - Ys[i - 1]) / h[i]

    global res 
    for i in range(1, n):
        if Xs[i - 1] <= x_value <= Xs[i]:
            res = a[i] + b[i] * (x_value - Xs[i]) + c[i] / 2 * (x_value - Xs[i]) ** 2 + d[i] / 6 * (x_value - Xs[i]) ** 3
    print(f"Значение функции для варианта {option} и x = {x_value}: y = {res:.4f}")

    s, Xt = [], []
    for i in range(1, n):
        x = Xs[i - 1]
        while x <= Xs[i]:
            s.append(a[i] + b[i] * (x - Xs[i]) + c[i] / 2 * (x - Xs[i]) ** 2 + d[i] / 6 * (x - Xs[i]) ** 3)
            Xt.append(x)
            x += 0.001
    return Xt, s

def get_valid_input(prompt, min_value, max_value, value_type=int):
    while True:
        try:
            value = value_type(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Ошибка: значение должно быть в диапазоне от {min_value} до {max_value}. Пожалуйста, попробуйте снова.")
        except ValueError:
            print("Ошибка: введено неверное значение. Пожалуйста, введите корректное число.")

option = get_valid_input("Выберите вариант (от 1 до 30): ", 1, 30, int)
x_value = get_valid_input("Выберите значение произвольного x (от 1 до 2): ", 1, 2, float)
print(f"Вы выбрали вариант: {option}\nВы выбрали значение x: {x_value}")

rows = [x1_0, x1_2, x1_4, x1_6, x1_8, x2_0]
y_data = [rows[i][option - 1] for i in range(len(rows))]
x_data = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0]

Xt, spline_values = cubic_spline(x_data, y_data, x_value)

plt.figure(figsize=(10, 6))
plt.plot(Xt, spline_values, label='График функции', color='blue')
plt.scatter(x_data, y_data, color='red', label='Базовые точки')
plt.scatter(x_value, res, color='green', label='Найденная точка')
plt.title('CSI - Cubic Spline Interpolation')
plt.xlabel('X-Ось')
plt.ylabel('Y-Ось')
plt.legend()
plt.grid()
plt.show()
