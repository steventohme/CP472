#lang scheme

(define (apply-to-each f lst)
    (if (null? lst)
        '()
        (cons (f (car lst)) (apply-to-each f (cdr lst)))))

(define (double x) (* 2 x))

(define numbers '(1 2 3 4 5))

(define doubled-numbers (apply-to-each double numbers))

(display doubled-numbers)
(newline)