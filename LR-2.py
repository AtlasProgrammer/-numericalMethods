def roman_to_arabic(roman):
    roman_numerals = {
        'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 
        'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10
    }
    arabic = 0
    length = len(roman)
    
    for i in range(length):
        value = roman_numerals.get(roman[i], 0)

        if i + 1 < length and roman_numerals.get(roman[i + 1], 0) > value:
            arabic -= value
        else:
            arabic += value

    return arabic

def solve_system_of_linear_equations(matrix_A, matrix_B):
    n = len(matrix_A)
    matrix = [row + [b] for row, b in zip(matrix_A, matrix_B)]
    for i in range(n):
        pivot = matrix[i][i]
        if pivot == 0:
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    pivot = matrix[i][i]
                    break
            else:
                return None

        for j in range(len(matrix[i])):
            matrix[i][j] /= pivot

        for j in range(i + 1, n):
            factor = matrix[j][i]
            for k in range(len(matrix[j])):
                matrix[j][k] -= factor * matrix[i][k]

    solutions = [0] * n
    for i in range(n - 1, -1, -1):
        solutions[i] = matrix[i][-1]
        for j in range(i - 1, -1, -1):
            matrix[j][-1] -= matrix[j][i] * solutions[i]

    return solutions

def check_solution(matrix_A, matrix_B, solutions):
    for i in range(len(matrix_A)):
        left_side = sum(matrix_A[i][j] * solutions[j] for j in range(len(matrix_A[i])))
        if abs(left_side - matrix_B[i]) > 1e-9:
            return False
    return True

def input_matrix_A():
    n = int(input("Введите количество уравнений (размерность матрицы A): "))
    matrix_A = []
    print("Введите коэффициенты матрицы A:")
    for i in range(n):
        while True:
            num_coefficients = int(input(f"Введите количество коэффициентов для строки {i + 1}: "))
            row = input(f"Строка {i + 1} (введите {num_coefficients} коэффициентов): ").split()
            if len(row) != num_coefficients:
                print(f"Ошибка: ожидается {num_coefficients} коэффициентов. Пожалуйста, введите значения снова.")
                continue
            
            if any(
                not (value.replace('.', '', 1).replace('/', '', 1).lstrip('-').isdigit() or all(c in 'IVXLCDM' for c in value))
                for value in row
            ):
                print("Ошибка: введены некорректные значения (буквы или символы). Пожалуйста, введите значения снова.")
                continue
            
            try:
                row = [float(eval(value)) if any(c.isdigit() for c in value) else float(roman_to_arabic(value)) for value in row]
                if any(isinstance(value, float) and value == 0 for value in row):
                    print("Ошибка: один из знаменателей равен нулю. Пожалуйста, введите значения снова.")
                    continue
                matrix_A.append(row)
                break
            except (ZeroDivisionError, ValueError, SyntaxError):
                print("Ошибка: неверный ввод. Пожалуйста, введите значения снова.")
    return matrix_A

def input_matrix_B():
    n = int(input("Введите количество уравнений (размерность матрицы B): "))
    matrix_B = []
    print("Введите свободные члены матрицы B:")
    for i in range (n):
        while True:
            value = input(f"Свободный член для уравнения {i + 1}: ")
            if not (value.replace('.', '', 1).replace('/', '', 1).lstrip('-').isdigit() or all(c in 'IVXLCDM' for c in value)):
                print("Ошибка: введены некорректные значения (буквы или символы). Пожалуйста, введите значения снова.")
                continue
            
            try:
                value = float(eval(value)) if any(c.isdigit() for c in value) else float(roman_to_arabic(value))
                matrix_B.append(value)
                break
            except (ZeroDivisionError, ValueError, SyntaxError):
                print("Ошибка: неверный ввод. Пожалуйста, введите значения снова.")
    return matrix_B

while True:
    matrix_A = input_matrix_A()
    matrix_B = input_matrix_B()
    solution = solve_system_of_linear_equations(matrix_A, matrix_B)
    if solution is not None:
        print("Решение системы уравнений:", solution)
        if check_solution(matrix_A, matrix_B, solution):
            print("Проверка: найденные решения удовлетворяют системе уравнений.")
        else:
            print("Проверка: найденные решения не удовлетворяют системе уравнений.")
    else:
        print("Система уравнений несовместна.")
