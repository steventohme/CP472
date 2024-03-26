#lang scheme
(define (move n from to aux)
    (if (= n 1)
        (display (list 'move 'disk 'from from 'to to))
        (begin
        (move (- n 1) from aux to)
        (display (list 'move 'disk 'from from 'to to))
        (move (- n 1) aux to from))))

(define (hanoi)
    (display "Enter the number of disks: ")
    (define n (read))
    (move n 'peg1 'peg3 'peg2))

(hanoi)