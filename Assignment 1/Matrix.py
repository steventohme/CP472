def Matrix_For(mat1, mat2):
    # check if the matrix can be multiplied
    if len(mat1[0]) != len(mat2):
        print("Cannot multiply the matrix" )
        return
    
    # set the matrix to the output size to 
    res_mat = [[0 for _ in range(len(mat2[0]))] for _ in range(len(mat1))]
    for i in range(len(mat1)):
        for j in range(len(mat2[0])):
            for k in range(len(mat2)):
                res_mat[i][j] += mat1[i][k] * mat2[k][j]
    
    return res_mat

def Matrix_While(mat1, mat2):
    pass

if __name__ == "__main__":
    mat1 = [[1, 2, 3], [4, 5, 6]]
    mat2 = [[7, 8], [9, 10], [11, 12]]
    print(Matrix_For(mat1, mat2))