#lang scheme
(define (sum-of-squares lst)
    ; Define a function to square a number
    (define (square x) (* x x))
    ; Map the square function over the list
    (define squared-list (map square lst))
    ; Define a function to sum two numbers
    (define (sum a b) (+ a b))
    ; Fold the sum function over the squared list
    (foldr sum 0 squared-list))

(define numbers '(1 2 3 4 5))

(display "Sum of squares: ")
(display (sum-of-squares numbers))