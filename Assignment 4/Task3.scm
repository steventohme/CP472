#lang scheme
(define (filter-even-and-product lst)
    ; function to filter even numbers
    (define (is-even? x) (= (remainder x 2) 0))

    ; filter even numbers
    (define even-numbers (filter is-even? lst))

    ; function to find product
    (define (product a b) (* a b))

    (foldl product 1 even-numbers))

(define numbers '(1 2 3 4 5 6 7 8 9 10)) 

(display "Product of even numbers: ")
(display (filter-even-and-product numbers))