#lang scheme

(define (matrix-multiply matrix1 matrix2)
    (define (transpose matrix)
        (apply map list matrix))

    (define (dot-product vec1 vec2)
        (apply + (map * vec1 vec2)))

    (define transposed-matrix2 (transpose matrix2))

    (define (multiply-row row)
        (map (lambda (col) (dot-product row col)) transposed-matrix2))

    (map multiply-row matrix1))

(define matrix1 '((1 2 3) (4 5 6) (7 8 9))) ; Example matrix 1
(define matrix2 '((9 8 7) (6 5 4) (3 2 1))) ; Example matrix 2

(display "Matrix 1:")
(newline)
(for-each (lambda (row) (display row) (newline)) matrix1)
(newline)

(display "Matrix 2:")
(newline)
(for-each (lambda (row) (display row) (newline)) matrix2)
(newline)

(display "Product of Matrix 1 and Matrix 2:")
(newline)
(for-each (lambda (row) (display row) (newline)) (matrix-multiply matrix1 matrix2))
