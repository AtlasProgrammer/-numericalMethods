import flet as ft
from decimal import Decimal, getcontext

def main(page: ft.Page):
    page.title = "Создание ячеек для уравнений"

    left_column = ft.Column(horizontal_alignment=ft.MainAxisAlignment.CENTER)

    entry_n = ft.TextField(label="Количество уравнений", width=200)
    entry_k = ft.TextField(label="Количество переменных", width=200)
    left_column.controls.append(ft.Row(controls=[entry_n, entry_k]))

    entry_matrix = ft.Column()
    left_column.controls.append(entry_matrix)

    def update_matrix_fields(e):
        entry_matrix.controls.clear()
        try:
            n = int(entry_n.value)
            k = int(entry_k.value)
            for i in range(n):
                equation_row = ft.Row()
                for j in range(k):
                    variable_field = ft.TextField(label=f"x{j + 1}", width=50)
                    equation_row.controls.append(variable_field)
                free_member_field = ft.TextField(label="=", width=50)
                equation_row.controls.append(free_member_field)
                entry_matrix.controls.append(equation_row)
            page.update()
        except ValueError:
            pass

    entry_n.on_change = update_matrix_fields
    entry_k.on_change = update_matrix_fields

    solve_button = ft.ElevatedButton("Решить", on_click=lambda _: on_solve(entry_n, entry_matrix, page))
    left_column.controls.append(solve_button)

    page.add(left_column)

def solve_tri_diagonal(A, B):
    n = len(B)
    if n == 0:
        return []

    alpha = [Decimal(0)] * n
    beta = [Decimal(0)] * n
    x = [Decimal(0)] * n

    if A[0][0] == 0:
        raise ValueError("Первый коэффициент матрицы не должен быть равен нулю.")

    alpha[0] = A[0][0]
    beta[0] = B[0] / alpha[0]

    for i in range(1, n):
        temp = A[i][i] - A[i][i-1] * (A[i-1][i] / alpha[i-1]) if i > 0 else A[i][i]
        if temp == 0:
            raise ValueError("Деление на ноль в прогонке.")
        alpha[i] = temp
        beta[i] = (B[i] - A[i][i-1] * beta[i-1]) / alpha[i]

    x[n - 1] = beta[n - 1]
    for i in range(n - 2, -1, -1):
        x[i] = beta[i] - A[i][i + 1] * x[i + 1] / alpha[i] if i + 1 < n else beta[i]

    return x

def on_solve(entry_n, entry_matrix, page):
    try:
        n = int(entry_n.value)
        A = []  # Массив коэффициентов
        B = []  # Массив свободных членов

        for row in entry_matrix.controls:
            coefficients = []
            for j in range(len(row.controls) - 1):  # Входные поля переменных
                coefficients.append(Decimal(row.controls[j].value) if row.controls[j].value else Decimal(0))
            free_member = Decimal(row.controls[-1].value) if row.controls[-1].value else Decimal(0)
            A.append(coefficients)
            B.append(free_member)

        # Проверяем на трёхдиагональность
        for i in range(n):
            if len(A[i]) != n or (i > 0 and A[i][i-1] == 0 and A[i-1][i] != 0):
                raise ValueError("Матрица не является трёхдиагональной.")

        # Решение методом прогонки
        x = solve_tri_diagonal(A, B)
        result_text = "Решение: " + ", ".join([f"x{i+1} = {val}" for i, val in enumerate(x)])

        # Подстановка значений x в уравнения
        substitution_results = []
        for idx, row in enumerate(A):
            left_side = sum(coeff * x[j] for j, coeff in enumerate(row))
            free_member = B[idx]
            substitution_results.append(f"Уравнение {idx + 1}: {left_side:.6f} (вычислено) = {free_member:.6f} (дано)")

        substitution_text = "\n".join(substitution_results)

    except Exception as e:
        result_text = f"Ошибка: {str(e)}"
        substitution_text = ""

    page.add(ft.Text(result_text, color="blue"))
    page.add(ft.Text(substitution_text, color="green"))


ft.app(target=main)
