import matplotlib.pyplot as plt

def eval_func(expr, x):
    try:
        return eval(expr, {"__builtins__": None, "x": x})
    except ZeroDivisionError:
        return float('inf')  

def bisection_method(expr, a, b, tolerance=0.01):
    f_a = eval_func(expr, a)
    f_b = eval_func(expr, b)

    if f_a * f_b > 0:
        print("Неверный отрезок: на границах функции имеют одинаковые знаки!")
        return None

    while (b - a) / 2.0 > tolerance:
        c = (a + b) / 2.0
        f_c = eval_func(expr, c)
        if f_c == 0:
            return c
        elif f_a * f_c < 0:
            b = c
        else:
            a = c
            f_a = f_c
    return (a + b) / 2.0

def newton_method(expr, x0, tolerance=0.01):
    def derivative(expr, x):
        h = 1e-5
        return (eval_func(expr, x + h) - eval_func(expr, x)) / h

    x_n = x0
    while True:
        f_x_n = eval_func(expr, x_n)
        f_prime_x_n = derivative(expr, x_n)

        if f_prime_x_n == 0:
            print("Производная равна нулю, метод Ньютона не может быть применен.")
            return None

        x_n1 = x_n - f_x_n / f_prime_x_n

        if abs(x_n1 - x_n) < tolerance or abs(eval_func(expr, x_n1)) < tolerance:
            return x_n1

        x_n = x_n1

def find_interval(expr):
    a = float(input("введите порог а:  "))
    b = float(input("введите порог для b:  "))
    step = 0.1

    last_value = eval_func(expr, a)

    while a <= b:
        current_value = eval_func(expr, a)
        if last_value * current_value < 0:
            return (a - step, a) 
        last_value = current_value
        a += step

    print("Корни не найдены в заданном диапазоне.")
    return None

def preprocess_equation(equation):
    if '=' in equation:
        left, right = equation.split('=')
        return f'({left}) - ({right})' 
    return equation  

def main(equation):
    user_input = equation
    equation = preprocess_equation(equation)

    interval = find_interval(equation)
    if interval is None:
        return

    a, b = interval
    x0 = (a + b) / 2

    print("\nРешение:")
    root_bisection = bisection_method(equation, a, b)
    root_newton = newton_method(equation, x0)

    if root_bisection is not None:
        print(f"Корень методом деления отрезка пополам: {root_bisection:.4f}")
    
    if root_newton is not None:
        print(f"Корень методом Ньютона: {root_newton:.4f}")
    
    plot_equations(user_input, False)

def plot_equations(user_input, flag):
    if flag:
        left_side = ''
        right_side = '0'

        if '=' in user_input:
            left_side, right_side = user_input.split('=')
            left_side = left_side.strip()
            right_side = right_side.strip()

            if right_side == '0' or right_side == 'null': 
                right_side = "0" 
            else:  
                right_side = right_side.strip()
        else: 
            left_side = user_input.strip()

        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')

        x = [j / 100.0 for j in range(-1000, 1001, 1)]

        try:
            y_left = []
            for val in x:
                try:
                    y_left.append(eval(left_side, {"x": val}))
                except ZeroDivisionError:
                    y_left.append(float("nan"))
                    continue
                except Exception as e:
                    print(f"Ошибка в уравнении (левая часть): {left_side} - {e}")
                    return
            plt.plot(x, y_left, label=f'Левая формула: {left_side}')
        except Exception as e:
            print(f"Ошибка в уравнении (левая часть): {left_side} - {e}")

        if right_side != "0":
            y_right = []
            for val in x:
                try:
                    y_right.append(eval(right_side, {"x": val}))
                except ZeroDivisionError:
                    y_right.append(float("nan"))
                    continue
                except Exception as e:
                    print(f"Ошибка в уравнении (правая часть): {right_side} - {e}")
                    return
            plt.plot(x, y_right, label=f'Правая формула: {right_side}')
        

        
        plt.title('Графики уравнений')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.ylim(-10, 10)
        plt.xlim(-10, 10)
        plt.grid()
        plt.legend()
        plt.show(block=False)
    else:
        plt.show()



user_input = input("Введите уравнение: ")
plot_equations(user_input, True)
main(user_input)
