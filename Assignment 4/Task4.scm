#lang scheme

(define (bubble-sort lst)
    ; Swap the first two elements if they are in the wrong order
    (define (swap lst)
    (if (or (null? lst) (null? (cdr lst)))
        lst
        (let ((current (car lst))
                (next (cadr lst))
                (rest (cddr lst)))
            (if (> current next)
                (cons next (cons current (swap rest)))
                (cons current (swap (cons next rest)))))))

    ; Keep swapping until the list is sorted
    (let loop ((lst lst) (swapped #t))
    (if swapped
        (let ((new-list (swap lst)))
            (if (equal? new-list lst)
                lst
                (loop new-list #t)))
        lst)))

(define numbers '(5 3 8 1 4 2 7 6))

(display "Original list: ")
(display numbers)
(newline)

(define sorted-list (bubble-sort numbers))

(display "Sorted list: ")
(display sorted-list)
(newline)