#lang scheme
(define (simple-interest principal rate time)
  (let ((interest (* principal rate time)))
    (/ interest 100)))

(define (main)
  (display "Enter principal amount: ")
  (define principal (read))
  (display "Enter rate of interest: ")
  (define rate (read))
  (display "Enter time (in years): ")
  (define time (read))
  (let ((interest (simple-interest principal rate time)))
    (display "Simple Interest: ")
    (display interest)
    (newline)))

(main)