matrix1 = []
matrix1.append(list(eval(input())))
size = len(matrix1[0])

for i in range(size - 1):
    matrix1.append(list(eval(input())))
    
matrix2 = []
for i in range(size):
    matrix2.append(list(eval(input())))
    
res_matrix = []
for i in range(size):
    new_row = []
    for j in range(size):
        new_elem = 0
        for s in range(size):
            new_elem += matrix1[i][s] * matrix2[s][j]
        new_row.append(new_elem)
    res_matrix.append(new_row)

for row in res_matrix:
    print(*row, sep = ',')
