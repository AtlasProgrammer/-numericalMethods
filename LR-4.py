import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def parse_input(value):
    """Парсит строку и обрабатывает значения, включая деления."""
    try:
        return eval(value)
    except Exception as e:
        messagebox.showerror("Ошибка", "Ошибка ввода: " + str(e))
        return None

def calculate_divided_diff(x, y):
    """Вычисляет разделенные разности."""
    n = len(y)
    div_diff = [[0] * n for _ in range(n)]  # Создаем двумерный список
    for i in range(n):
        div_diff[i][0] = y[i]  # Заполняем первый столбец значениями y

    for j in range(1, n):
        for i in range(n - j):
            div_diff[i][j] = (div_diff[i + 1][j - 1] - div_diff[i][j - 1]) / (x[i + j] - x[i])

    return div_diff

def lagrange_interpolation(x, y, x_value):
    total = 0
    n = len(x)
    for i in range(n):
        term = y[i]
        for j in range(n):
            if j != i:
                term *= (x_value - x[j]) / (x[i] - x[j])
        total += term
    return total

def newton_interpolation(x, div_diff, x_value):
    total = div_diff[0][0]
    n = len(x)
    for i in range(1, n):
        term = div_diff[0][i]
        for j in range(i):
            term *= (x_value - x[j])
        total += term
    return total

def plot_lagrange(x, y):
    plt.figure(figsize=(10, 5))
    plt.scatter(x, y, color='red', label='Точки')
    
    x_vals = [min(x) - 1 + i * (max(x) - min(x) + 2) / 99 for i in range(100)]
    y_vals_lagrange = [lagrange_interpolation(x, y, val) for val in x_vals]
    plt.plot(x_vals, y_vals_lagrange, label='Полином Лагранжа', color='blue')

    plt.title('Интерполяция: Полином Лагранжа')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid()
    plt.show(block=False)

def plot_newton(x, y):
    plt.figure(figsize=(10, 5))
    plt.scatter(x, y, color='red', label='Точки')
    
    div_diff = calculate_divided_diff(x, y)
    x_vals = [min(x) - 1 + i * (max(x) - min(x) + 2) / 99 for i in range(100)]
    y_vals_newton = [newton_interpolation(x, div_diff, val) for val in x_vals]
    plt.plot(x_vals, y_vals_newton, label='Полином Ньютона', color='green')

    plt.title('Интерполяция: Полином Ньютона')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid()
    plt.show(block=False)

def create_table(x, y, div_diff):
    table_text = "xi;yi;Разделенная разность 1го порядка;Разделенная разность 2го порядка\n"
    for i in range(3):
        if i == 2:
            table_text += del_2_3
        table_text += f"{x[i]}   {y[i]}   "

        for j in range(3):  
            if j < len(div_diff) and j > 0 and div_diff[i][j] != 0: 
                if i == 0:
                    if j == 1:
                        del_1_2 = f"\n        {div_diff[i][j]}"
                        table_text += del_1_2
                    else:
                        del_1_2_3 = f"   {div_diff[i][j]}"
                if i == 1 and j == 1:
                    del_2_3 = f"        {div_diff[i][j]}\n"
        if i == 1:
            table_text += del_1_2_3
        
        table_text += "\n"

    return table_text

def solve():
    x1 = parse_input(entry_x1.get())
    x2 = parse_input(entry_x2.get())
    x3 = parse_input(entry_x3.get())
    y1 = parse_input(entry_y1.get())
    y2 = parse_input(entry_y2.get())
    y3 = parse_input(entry_y3.get())

    if None in (x1, x2, x3, y1, y2, y3):
        return

    x = [x1, x2, x3]
    y = [y1, y2, y3]

    div_diff = calculate_divided_diff(x, y)

    table_text = create_table(x, y, div_diff)

    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, table_text)

    plot_lagrange(x, y)
    plot_newton(x, y)

def calculate_y():
    x1 = parse_input(entry_x1.get())
    x2 = parse_input(entry_x2.get())
    x3 = parse_input(entry_x3.get())
    y1 = parse_input(entry_y1.get())
    y2 = parse_input(entry_y2.get())
    y3 = parse_input(entry_y3.get())

    if None in (x1, x2, x3, y1, y2, y3):
        return

    x = [x1, x2, x3]
    y = [y1, y2, y3]

    x_value = parse_input(entry_x_value.get())
    if x_value is not None:
        y_value_lagrange = lagrange_interpolation(x, y, x_value)
        y_value_newton = newton_interpolation(x, calculate_divided_diff(x, y), x_value)
        result_text = f"y({x_value}) = {y_value_lagrange} (Полином Лагранжа)\n"
        result_text += f"y({x_value}) = {y_value_newton} (Полином Ньютона)"
        result_area.delete(1.0, tk.END)
        result_area.insert(tk.END, result_text)

root = tk.Tk()
root.title("Интерполяция")

padx_value = 1
pady_value = 1

tk.Label(root, text="x1:").grid(row=0, column=0, padx=padx_value, pady=pady_value)
entry_x1 = tk.Entry(root)
entry_x1.grid(row=0, column=1, padx=padx_value, pady=pady_value)

tk.Label(root, text="y1:").grid(row=0, column=2, padx=padx_value, pady=pady_value)  
entry_y1 = tk.Entry(root)
entry_y1.grid(row=0, column=3, padx=padx_value, pady=pady_value) 

tk.Label(root, text="x2:").grid(row=1, column=0, padx=padx_value, pady=pady_value)
entry_x2 = tk.Entry(root)
entry_x2.grid(row=1, column=1, padx=padx_value, pady=pady_value)

tk.Label(root, text="y2:").grid(row=1, column=2, padx=padx_value, pady=pady_value)  
entry_y2 = tk.Entry(root)
entry_y2.grid(row=1, column=3, padx=padx_value, pady=pady_value)  

tk.Label(root, text="x3:").grid(row=2, column=0, padx=padx_value, pady=pady_value)
entry_x3 = tk.Entry(root)
entry_x3.grid(row=2, column=1, padx=padx_value, pady=pady_value)

tk.Label(root, text="y3:").grid(row=2, column=2, padx=padx_value, pady=pady_value)  
entry_y3 = tk.Entry(root)
entry_y3.grid(row=2, column=3, padx=padx_value, pady=pady_value)

tk.Label(root, text="x:").grid(row=3, column=0, padx=padx_value, pady=pady_value)
entry_x_value = tk.Entry(root)
entry_x_value.grid(row=3, column=1, padx=padx_value, pady=pady_value)

btn_solve = tk.Button(root, text="Решить", command=solve)  
btn_solve.grid(row=6, column=0, columnspan=4, pady=pady_value)

btn_calculate_y = tk.Button(root, text="Вычислить y", command=calculate_y)  
btn_calculate_y.grid(row=7, column=0, columnspan=4, pady=pady_value)

text_area = tk.Text(root, height=10, width=80)
text_area.grid(row=8, column=0, columnspan=4, pady=pady_value)

result_area = tk.Text(root, height=2, width=80)
result_area.grid(row=9, column=0, columnspan=4, pady=pady_value)

root.mainloop()
