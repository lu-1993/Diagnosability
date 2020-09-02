; model

(set-option :produce-unsat-cores true)

;declare data structure to store transitions as follows:
;the first arguement stores the source state, the second for destination state, and the third for the event

(declare-datatypes (T1) ((Pair (mk-pair (first T1) (second T1) (third T1)))))

;read all transitions of systems (finite automaton) from model.txt
;for example, the first transition is from state 1 to state 2 with event 1

(assert (and (= (first p1) 1)(= (second p1) 2)(= (third p1) 1
)(= (trS 1) p1)))
(assert (and (= (first p2) 2)(= (second p2) 3)(= (third p2) 2
)(= (trS 2) p2)))
(assert (and (= (first p3) 3)(= (second p3) 4)(= (third p3) 6
)(= (trS 3) p3)))
(assert (and (= (first p4) 4)(= (second p4) 5)(= (third p4) 4
)(= (trS 4) p4)))
(assert (and (= (first p5) 5)(= (second p5) 5)(= (third p5) 3
)(= (trS 5) p5)))
(assert (and (= (first p6) 2)(= (second p6) 6)(= (third p6) 2
)(= (trS 6) p6)))
(assert (and (= (first p7) 6)(= (second p7) 7)(= (third p7) 5
)(= (trS 7) p7)))
(assert (and (= (first p8) 7)(= (second p8) 8)(= (third p8) 2
)(= (trS 8) p8)))
(assert (and (= (first p9) 8)(= (second p9) 8)(= (third p9) 2
)(= (trS 9) p9)))
(assert (and (= (first p10) 1)(= (second p10) 3)(= (third p10) 1
)(= (trS 10) p10)))

;function to verify whether a given event (integer) is an observable event (in this system, 1,2,3 are observable)

(define-fun obs ((o Int)) Bool
  (if (and (>= o 1) (<= o 3))
    true
    false))

;define loc (states of normal path) and locFault (states of faulty path) and initialization (both begin from the state 1)

(declare-fun loc (Int) Int)
(declare-fun locFault (Int) Int)
(assert (=(loc 0) 1))
(assert (=(locFault 0) 1))

;define event (events of normal path) and eventFault (events of faulty path) and initialization

(declare-fun event (Int) Int)
(declare-fun eventFault (Int) Int)
(assert (=(event -1)0))
(assert (=(eventFault -1)0))

;function to check whether a given event on the faulty/normal path is faulty (event 6) or normal (events 1-5)

(define-fun existF((fau Int)) Bool
  (if (= (eventFault fau) 6)
  true false))

(define-fun notF((nor Int)) Bool
  (if(and (>= (event nor) 1) (<= (event nor) 5)) true false))

;some functions to computer k-value on the specific transition (k represents the number of steps after the fault)

(declare-fun k (Int) Int)

(assert (= (k -1) 0))(define-fun ifault((fau Int)) Int
  (if (= (eventFault fau) 6)
  1 0))
(assert (=(ifault -1)0))

(declare-fun isfault (Int) Int)
(assert (=(isfault -1)0))

(define-fun midk ((i Int)) Bool
(if (or(=(ifault i)1)(=(isfault (- i 1))1))
(=(isfault i)1)
(=(isfault i)0)))

(define-fun compk ((i Int)) Bool
(if (=(isfault i)0)
(=(k i)0)
(= (k i) (+(k (- i 1))1))))

;declare two constants lf/ln: length of faulty/normal path

(declare-const lf Int)

(declare-const ln Int)

;declare two arrays obsn/obsf: arrays to store all observable events on the normal/faulty path;

(declare-const obsn (Array Int Int))
(declare-const obsf (Array Int Int))

;declare constants count/countf to represent the index of the obsn/obsf and initialization


(declare-fun count (Int) Int)
(assert (= (count 0) 0))
(declare-fun countf (Int) Int)
(assert (= (countf 0) 0))

;;; construct a faulty path with bound
(assert (and 

;construct a faulty path
(or(and (= (first (trS 1)) (locFault 0))(= (eventFault 0) (third (trS 1))) (= (locFault  1) (second (trS 1))))(and (= (first (trS 2)) (locFault 0))(= (eventFault 0) (third (trS 2))) (= (locFault  1) (second (trS 2))))(and (= (first (trS 3)) (locFault 0))(= (eventFault 0) (third (trS 3))) (= (locFault  1) (second (trS 3))))(and (= (first (trS 4)) (locFault 0))(= (eventFault 0) (third (trS 4))) (= (locFault  1) (second (trS 4))))(and (= (first (trS 5)) (locFault 0))(= (eventFault 0) (third (trS 5))) (= (locFault  1) (second (trS 5))))(and (= (first (trS 6)) (locFault 0))(= (eventFault 0) (third (trS 6))) (= (locFault  1) (second (trS 6))))(and (= (first (trS 7)) (locFault 0))(= (eventFault 0) (third (trS 7))) (= (locFault  1) (second (trS 7))))(and (= (first (trS 8)) (locFault 0))(= (eventFault 0) (third (trS 8))) (= (locFault  1) (second (trS 8)))))
(or(and (= (first (trS 1)) (locFault 1))(= (eventFault 1) (third (trS 1))) (= (locFault  2) (second (trS 1))))(and (= (first (trS 2)) (locFault 1))(= (eventFault 1) (third (trS 2))) (= (locFault  2) (second (trS 2))))(and (= (first (trS 3)) (locFault 1))(= (eventFault 1) (third (trS 3))) (= (locFault  2) (second (trS 3))))(and (= (first (trS 4)) (locFault 1))(= (eventFault 1) (third (trS 4))) (= (locFault  2) (second (trS 4))))(and (= (first (trS 5)) (locFault 1))(= (eventFault 1) (third (trS 5))) (= (locFault  2) (second (trS 5))))(and (= (first (trS 6)) (locFault 1))(= (eventFault 1) (third (trS 6))) (= (locFault  2) (second (trS 6))))(and (= (first (trS 7)) (locFault 1))(= (eventFault 1) (third (trS 7))) (= (locFault  2) (second (trS 7))))(and (= (first (trS 8)) (locFault 1))(= (eventFault 1) (third (trS 8))) (= (locFault  2) (second (trS 8)))))
(or(and (= (first (trS 1)) (locFault 2))(= (eventFault 2) (third (trS 1))) (= (locFault  3) (second (trS 1))))(and (= (first (trS 2)) (locFault 2))(= (eventFault 2) (third (trS 2))) (= (locFault  3) (second (trS 2))))(and (= (first (trS 3)) (locFault 2))(= (eventFault 2) (third (trS 3))) (= (locFault  3) (second (trS 3))))(and (= (first (trS 4)) (locFault 2))(= (eventFault 2) (third (trS 4))) (= (locFault  3) (second (trS 4))))(and (= (first (trS 5)) (locFault 2))(= (eventFault 2) (third (trS 5))) (= (locFault  3) (second (trS 5))))(and (= (first (trS 6)) (locFault 2))(= (eventFault 2) (third (trS 6))) (= (locFault  3) (second (trS 6))))(and (= (first (trS 7)) (locFault 2))(= (eventFault 2) (third (trS 7))) (= (locFault  3) (second (trS 7))))(and (= (first (trS 8)) (locFault 2))(= (eventFault 2) (third (trS 8))) (= (locFault  3) (second (trS 8)))))
(or(and (= (first (trS 1)) (locFault 3))(= (eventFault 3) (third (trS 1))) (= (locFault  4) (second (trS 1))))(and (= (first (trS 2)) (locFault 3))(= (eventFault 3) (third (trS 2))) (= (locFault  4) (second (trS 2))))(and (= (first (trS 3)) (locFault 3))(= (eventFault 3) (third (trS 3))) (= (locFault  4) (second (trS 3))))(and (= (first (trS 4)) (locFault 3))(= (eventFault 3) (third (trS 4))) (= (locFault  4) (second (trS 4))))(and (= (first (trS 5)) (locFault 3))(= (eventFault 3) (third (trS 5))) (= (locFault  4) (second (trS 5))))(and (= (first (trS 6)) (locFault 3))(= (eventFault 3) (third (trS 6))) (= (locFault  4) (second (trS 6))))(and (= (first (trS 7)) (locFault 3))(= (eventFault 3) (third (trS 7))) (= (locFault  4) (second (trS 7))))(and (= (first (trS 8)) (locFault 3))(= (eventFault 3) (third (trS 8))) (= (locFault  4) (second (trS 8)))))
(or(and (= (first (trS 1)) (locFault 4))(= (eventFault 4) (third (trS 1))) (= (locFault  5) (second (trS 1))))(and (= (first (trS 2)) (locFault 4))(= (eventFault 4) (third (trS 2))) (= (locFault  5) (second (trS 2))))(and (= (first (trS 3)) (locFault 4))(= (eventFault 4) (third (trS 3))) (= (locFault  5) (second (trS 3))))(and (= (first (trS 4)) (locFault 4))(= (eventFault 4) (third (trS 4))) (= (locFault  5) (second (trS 4))))(and (= (first (trS 5)) (locFault 4))(= (eventFault 4) (third (trS 5))) (= (locFault  5) (second (trS 5))))(and (= (first (trS 6)) (locFault 4))(= (eventFault 4) (third (trS 6))) (= (locFault  5) (second (trS 6))))(and (= (first (trS 7)) (locFault 4))(= (eventFault 4) (third (trS 7))) (= (locFault  5) (second (trS 7))))(and (= (first (trS 8)) (locFault 4))(= (eventFault 4) (third (trS 8))) (= (locFault  5) (second (trS 8)))))



;check that at least one fault occur on the faulty path
(or(existF 0)(existF 1)(existF 2)(existF 3)(existF 4))

;computer k value in each step
(and(compk 0)(midk 0)(compk 1)(midk 1)(compk 2)(midk 2)(compk 3)(midk 3)(compk 4)(midk 4))

;lenght of the faulty path
(or( and (= (k 0)3)(= lf 1))( and (= (k 1)3)(= lf 2))( and (= (k 2)3)(= lf 3))( and (= (k 3)3)(= lf 4))( and (= (k 4)3)(= lf 5)))

;array to store all observable events of the faulty path
(and(ite (and (=(obs (eventFault 0)) true)(not(= (eventFault 0)(eventFault -1)))) (and (= (countf 1) (+ (countf 0) 1))(= (store obsf (countf 0) (eventFault 0)) obsf)) (= (countf 1)(countf 0)))(ite (and (=(obs (eventFault 1)) true)(not(= (eventFault 1)(eventFault 0)))) (and (= (countf 2) (+ (countf 1) 1))(= (store obsf (countf 1) (eventFault 1)) obsf)) (= (countf 2)(countf 1)))(ite (and (=(obs (eventFault 2)) true)(not(= (eventFault 2)(eventFault 1)))) (and (= (countf 3) (+ (countf 2) 1))(= (store obsf (countf 2) (eventFault 2)) obsf)) (= (countf 3)(countf 2)))(ite (and (=(obs (eventFault 3)) true)(not(= (eventFault 3)(eventFault 2)))) (and (= (countf 4) (+ (countf 3) 1))(= (store obsf (countf 3) (eventFault 3)) obsf)) (= (countf 4)(countf 3)))(ite (and (=(obs (eventFault 4)) true)(not(= (eventFault 4)(eventFault 3)))) (and (= (countf 5) (+ (countf 4) 1))(= (store obsf (countf 4) (eventFault 4)) obsf)) (= (countf 5)(countf 4))))
))

;;; construct a normal path with bound

(assert (or

;; construct a normal path of length 1 and verify the diagnosability.
(and
;construct normal path
(or(and (= (first (trS 1)) (loc 0))(= (event 0) (third (trS 1))) (= (loc 1) (second (trS 1))))(and (= (first (trS 2)) (loc 0))(= (event 0) (third (trS 2))) (= (loc 1) (second (trS 2))))(and (= (first (trS 3)) (loc 0))(= (event 0) (third (trS 3))) (= (loc 1) (second (trS 3))))(and (= (first (trS 4)) (loc 0))(= (event 0) (third (trS 4))) (= (loc 1) (second (trS 4))))(and (= (first (trS 5)) (loc 0))(= (event 0) (third (trS 5))) (= (loc 1) (second (trS 5))))(and (= (first (trS 6)) (loc 0))(= (event 0) (third (trS 6))) (= (loc 1) (second (trS 6))))(and (= (first (trS 7)) (loc 0))(= (event 0) (third (trS 7))) (= (loc 1) (second (trS 7))))(and (= (first (trS 8)) (loc 0))(= (event 0) (third (trS 8))) (= (loc (+ 0 1)) (second (trS 8)))))

;check that all transitions are labeled normal events on the normal path
(notF 0)

;array to store all observable events of the normal path
(ite (=(obs (event 0)) true)(and (= (count 1) (+ (count 0) 1))(= (store obsn (count 0) (event 0)) obsn)) (= (count 1)(count 0)))

;check that two path(normal and fauly path) are the same observation
(= obsn obsf)
(= ln 1))

;; construct a normal path of length 2 and verify the diagonsability.
(and

;construct nomal path
(or(and (= (first (trS 1)) (loc 0))(= (event 0) (third (trS 1))) (= (loc 1) (second (trS 1))))(and (= (first (trS 2)) (loc 0))(= (event 0) (third (trS 2))) (= (loc 1) (second (trS 2))))(and (= (first (trS 3)) (loc 0))(= (event 0) (third (trS 3))) (= (loc 1) (second (trS 3))))(and (= (first (trS 4)) (loc 0))(= (event 0) (third (trS 4))) (= (loc 1) (second (trS 4))))(and (= (first (trS 5)) (loc 0))(= (event 0) (third (trS 5))) (= (loc 1) (second (trS 5))))(and (= (first (trS 6)) (loc 0))(= (event 0) (third (trS 6))) (= (loc 1) (second (trS 6))))(and (= (first (trS 7)) (loc 0))(= (event 0) (third (trS 7))) (= (loc 1) (second (trS 7))))(and (= (first (trS 8)) (loc 0))(= (event 0) (third (trS 8))) (= (loc 1) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 1))(= (event 1) (third (trS 1))) (= (loc 2) (second (trS 1))))(and (= (first (trS 2)) (loc 1))(= (event 1) (third (trS 2))) (= (loc 2) (second (trS 2))))(and (= (first (trS 3)) (loc 1))(= (event 1) (third (trS 3))) (= (loc 2) (second (trS 3))))(and (= (first (trS 4)) (loc 1))(= (event 1) (third (trS 4))) (= (loc 2) (second (trS 4))))(and (= (first (trS 5)) (loc 1))(= (event 1) (third (trS 5))) (= (loc 2) (second (trS 5))))(and (= (first (trS 6)) (loc 1))(= (event 1) (third (trS 6))) (= (loc 2) (second (trS 6))))(and (= (first (trS 7)) (loc 1))(= (event 1) (third (trS 7))) (= (loc 2) (second (trS 7))))(and (= (first (trS 8)) (loc 1))(= (event 1) (third (trS 8))) (= (loc 2) (second (trS 8)))))

;check that all transitions are labeled normal events on the normal path
(and(notF 0)(notF 1))

;array to store all observable events of the normal path
(and(ite (and (=(obs (event 0)) true)(not(= (event 0)(event -1)))) (and (= (count 1) (+ (count 0) 1))(= (store obsn (count 0)(event 0)) obsn)) (= (count 1)(count 0)))(ite (and (=(obs (event 1)) true)(not(= (event 1)(event 0)))) (and (= (count 2) (+ (count 1) 1))(= (store obsn (count 1)(event 1)) obsn)) (= (count 2)(count 1))))
(= ln 2))



;; construct a normal path of length 3 and verify the diagonsability.
(and

;construct nomal path
(or(and (= (first (trS 1)) (loc 0))(= (event 0) (third (trS 1))) (= (loc 1) (second (trS 1))))(and (= (first (trS 2)) (loc 0))(= (event 0) (third (trS 2))) (= (loc 1) (second (trS 2))))(and (= (first (trS 3)) (loc 0))(= (event 0) (third (trS 3))) (= (loc 1) (second (trS 3))))(and (= (first (trS 4)) (loc 0))(= (event 0) (third (trS 4))) (= (loc 1) (second (trS 4))))(and (= (first (trS 5)) (loc 0))(= (event 0) (third (trS 5))) (= (loc 1) (second (trS 5))))(and (= (first (trS 6)) (loc 0))(= (event 0) (third (trS 6))) (= (loc 1) (second (trS 6))))(and (= (first (trS 7)) (loc 0))(= (event 0) (third (trS 7))) (= (loc 1) (second (trS 7))))(and (= (first (trS 8)) (loc 0))(= (event 0) (third (trS 8))) (= (loc 1) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 1))(= (event 1) (third (trS 1))) (= (loc 2) (second (trS 1))))(and (= (first (trS 2)) (loc 1))(= (event 1) (third (trS 2))) (= (loc 2) (second (trS 2))))(and (= (first (trS 3)) (loc 1))(= (event 1) (third (trS 3))) (= (loc 2) (second (trS 3))))(and (= (first (trS 4)) (loc 1))(= (event 1) (third (trS 4))) (= (loc 2) (second (trS 4))))(and (= (first (trS 5)) (loc 1))(= (event 1) (third (trS 5))) (= (loc 2) (second (trS 5))))(and (= (first (trS 6)) (loc 1))(= (event 1) (third (trS 6))) (= (loc 2) (second (trS 6))))(and (= (first (trS 7)) (loc 1))(= (event 1) (third (trS 7))) (= (loc 2) (second (trS 7))))(and (= (first (trS 8)) (loc 1))(= (event 1) (third (trS 8))) (= (loc 2) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 2))(= (event 2) (third (trS 1))) (= (loc 3) (second (trS 1))))(and (= (first (trS 2)) (loc 2))(= (event 2) (third (trS 2))) (= (loc 3) (second (trS 2))))(and (= (first (trS 3)) (loc 2))(= (event 2) (third (trS 3))) (= (loc 3) (second (trS 3))))(and (= (first (trS 4)) (loc 2))(= (event 2) (third (trS 4))) (= (loc 3) (second (trS 4))))(and (= (first (trS 5)) (loc 2))(= (event 2) (third (trS 5))) (= (loc 3) (second (trS 5))))(and (= (first (trS 6)) (loc 2))(= (event 2) (third (trS 6))) (= (loc 3) (second (trS 6))))(and (= (first (trS 7)) (loc 2))(= (event 2) (third (trS 7))) (= (loc 3) (second (trS 7))))(and (= (first (trS 8)) (loc 2))(= (event 2) (third (trS 8))) (= (loc 3) (second (trS 8)))))

;check that all transitions are labeled normal events on the normal path
(and(notF 0)(notF 1)(notF 2))

;array to store all observable events of the normal path
(and(ite (and (=(obs (event 0)) true)(not(= (event 0)(event -1)))) (and (= (count 1) (+ (count 0) 1))(= (store obsn (count 0)(event 0)) obsn)) (= (count 1)(count 0)))(ite (and (=(obs (event 1)) true)(not(= (event 1)(event 0)))) (and (= (count 2) (+ (count 1) 1))(= (store obsn (count 1)(event 1)) obsn)) (= (count 2)(count 1)))(ite (and (=(obs (event 2)) true)(not(= (event 2)(event 1)))) (and (= (count 3) (+ (count 2) 1))(= (store obsn (count 2)(event 2)) obsn)) (= (count 3)(count 2))))
(= ln 3))



;; construct a normal path of length 4 and verify the diagonsability.
(and

;construct nomal path
(or(and (= (first (trS 1)) (loc 0))(= (event 0) (third (trS 1))) (= (loc 1) (second (trS 1))))(and (= (first (trS 2)) (loc 0))(= (event 0) (third (trS 2))) (= (loc 1) (second (trS 2))))(and (= (first (trS 3)) (loc 0))(= (event 0) (third (trS 3))) (= (loc 1) (second (trS 3))))(and (= (first (trS 4)) (loc 0))(= (event 0) (third (trS 4))) (= (loc 1) (second (trS 4))))(and (= (first (trS 5)) (loc 0))(= (event 0) (third (trS 5))) (= (loc 1) (second (trS 5))))(and (= (first (trS 6)) (loc 0))(= (event 0) (third (trS 6))) (= (loc 1) (second (trS 6))))(and (= (first (trS 7)) (loc 0))(= (event 0) (third (trS 7))) (= (loc 1) (second (trS 7))))(and (= (first (trS 8)) (loc 0))(= (event 0) (third (trS 8))) (= (loc 1) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 1))(= (event 1) (third (trS 1))) (= (loc 2) (second (trS 1))))(and (= (first (trS 2)) (loc 1))(= (event 1) (third (trS 2))) (= (loc 2) (second (trS 2))))(and (= (first (trS 3)) (loc 1))(= (event 1) (third (trS 3))) (= (loc 2) (second (trS 3))))(and (= (first (trS 4)) (loc 1))(= (event 1) (third (trS 4))) (= (loc 2) (second (trS 4))))(and (= (first (trS 5)) (loc 1))(= (event 1) (third (trS 5))) (= (loc 2) (second (trS 5))))(and (= (first (trS 6)) (loc 1))(= (event 1) (third (trS 6))) (= (loc 2) (second (trS 6))))(and (= (first (trS 7)) (loc 1))(= (event 1) (third (trS 7))) (= (loc 2) (second (trS 7))))(and (= (first (trS 8)) (loc 1))(= (event 1) (third (trS 8))) (= (loc 2) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 2))(= (event 2) (third (trS 1))) (= (loc 3) (second (trS 1))))(and (= (first (trS 2)) (loc 2))(= (event 2) (third (trS 2))) (= (loc 3) (second (trS 2))))(and (= (first (trS 3)) (loc 2))(= (event 2) (third (trS 3))) (= (loc 3) (second (trS 3))))(and (= (first (trS 4)) (loc 2))(= (event 2) (third (trS 4))) (= (loc 3) (second (trS 4))))(and (= (first (trS 5)) (loc 2))(= (event 2) (third (trS 5))) (= (loc 3) (second (trS 5))))(and (= (first (trS 6)) (loc 2))(= (event 2) (third (trS 6))) (= (loc 3) (second (trS 6))))(and (= (first (trS 7)) (loc 2))(= (event 2) (third (trS 7))) (= (loc 3) (second (trS 7))))(and (= (first (trS 8)) (loc 2))(= (event 2) (third (trS 8))) (= (loc 3) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 3))(= (event 3) (third (trS 1))) (= (loc 4) (second (trS 1))))(and (= (first (trS 2)) (loc 3))(= (event 3) (third (trS 2))) (= (loc 4) (second (trS 2))))(and (= (first (trS 3)) (loc 3))(= (event 3) (third (trS 3))) (= (loc 4) (second (trS 3))))(and (= (first (trS 4)) (loc 3))(= (event 3) (third (trS 4))) (= (loc 4) (second (trS 4))))(and (= (first (trS 5)) (loc 3))(= (event 3) (third (trS 5))) (= (loc 4) (second (trS 5))))(and (= (first (trS 6)) (loc 3))(= (event 3) (third (trS 6))) (= (loc 4) (second (trS 6))))(and (= (first (trS 7)) (loc 3))(= (event 3) (third (trS 7))) (= (loc 4) (second (trS 7))))(and (= (first (trS 8)) (loc 3))(= (event 3) (third (trS 8))) (= (loc 4) (second (trS 8)))))

;check that all transitions are labeled normal events on the normal path
(and(notF 0)(notF 1)(notF 2)(notF 3))

;array to store all observable events of the normal path
(and(ite (and (=(obs (event 0)) true)(not(= (event 0)(event -1)))) (and (= (count 1) (+ (count 0) 1))(= (store obsn (count 0)(event 0)) obsn)) (= (count 1)(count 0)))(ite (and (=(obs (event 1)) true)(not(= (event 1)(event 0)))) (and (= (count 2) (+ (count 1) 1))(= (store obsn (count 1)(event 1)) obsn)) (= (count 2)(count 1)))(ite (and (=(obs (event 2)) true)(not(= (event 2)(event 1)))) (and (= (count 3) (+ (count 2) 1))(= (store obsn (count 2)(event 2)) obsn)) (= (count 3)(count 2)))(ite (and (=(obs (event 3)) true)(not(= (event 3)(event 2)))) (and (= (count 4) (+ (count 3) 1))(= (store obsn (count 3)(event 3)) obsn)) (= (count 4)(count 3))))
(= ln 4))



;; construct a normal path of length 5 and verify the diagonsability.
(and

;construct normal path
(or(and (= (first (trS 1)) (loc 0))(= (event 0) (third (trS 1))) (= (loc 1) (second (trS 1))))(and (= (first (trS 2)) (loc 0))(= (event 0) (third (trS 2))) (= (loc 1) (second (trS 2))))(and (= (first (trS 3)) (loc 0))(= (event 0) (third (trS 3))) (= (loc 1) (second (trS 3))))(and (= (first (trS 4)) (loc 0))(= (event 0) (third (trS 4))) (= (loc 1) (second (trS 4))))(and (= (first (trS 5)) (loc 0))(= (event 0) (third (trS 5))) (= (loc 1) (second (trS 5))))(and (= (first (trS 6)) (loc 0))(= (event 0) (third (trS 6))) (= (loc 1) (second (trS 6))))(and (= (first (trS 7)) (loc 0))(= (event 0) (third (trS 7))) (= (loc 1) (second (trS 7))))(and (= (first (trS 8)) (loc 0))(= (event 0) (third (trS 8))) (= (loc 1) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 1))(= (event 1) (third (trS 1))) (= (loc 2) (second (trS 1))))(and (= (first (trS 2)) (loc 1))(= (event 1) (third (trS 2))) (= (loc 2) (second (trS 2))))(and (= (first (trS 3)) (loc 1))(= (event 1) (third (trS 3))) (= (loc 2) (second (trS 3))))(and (= (first (trS 4)) (loc 1))(= (event 1) (third (trS 4))) (= (loc 2) (second (trS 4))))(and (= (first (trS 5)) (loc 1))(= (event 1) (third (trS 5))) (= (loc 2) (second (trS 5))))(and (= (first (trS 6)) (loc 1))(= (event 1) (third (trS 6))) (= (loc 2) (second (trS 6))))(and (= (first (trS 7)) (loc 1))(= (event 1) (third (trS 7))) (= (loc 2) (second (trS 7))))(and (= (first (trS 8)) (loc 1))(= (event 1) (third (trS 8))) (= (loc 2) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 2))(= (event 2) (third (trS 1))) (= (loc 3) (second (trS 1))))(and (= (first (trS 2)) (loc 2))(= (event 2) (third (trS 2))) (= (loc 3) (second (trS 2))))(and (= (first (trS 3)) (loc 2))(= (event 2) (third (trS 3))) (= (loc 3) (second (trS 3))))(and (= (first (trS 4)) (loc 2))(= (event 2) (third (trS 4))) (= (loc 3) (second (trS 4))))(and (= (first (trS 5)) (loc 2))(= (event 2) (third (trS 5))) (= (loc 3) (second (trS 5))))(and (= (first (trS 6)) (loc 2))(= (event 2) (third (trS 6))) (= (loc 3) (second (trS 6))))(and (= (first (trS 7)) (loc 2))(= (event 2) (third (trS 7))) (= (loc 3) (second (trS 7))))(and (= (first (trS 8)) (loc 2))(= (event 2) (third (trS 8))) (= (loc 3) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 3))(= (event 3) (third (trS 1))) (= (loc 4) (second (trS 1))))(and (= (first (trS 2)) (loc 3))(= (event 3) (third (trS 2))) (= (loc 4) (second (trS 2))))(and (= (first (trS 3)) (loc 3))(= (event 3) (third (trS 3))) (= (loc 4) (second (trS 3))))(and (= (first (trS 4)) (loc 3))(= (event 3) (third (trS 4))) (= (loc 4) (second (trS 4))))(and (= (first (trS 5)) (loc 3))(= (event 3) (third (trS 5))) (= (loc 4) (second (trS 5))))(and (= (first (trS 6)) (loc 3))(= (event 3) (third (trS 6))) (= (loc 4) (second (trS 6))))(and (= (first (trS 7)) (loc 3))(= (event 3) (third (trS 7))) (= (loc 4) (second (trS 7))))(and (= (first (trS 8)) (loc 3))(= (event 3) (third (trS 8))) (= (loc 4) (second (trS 8)))))
(or(and (= (first (trS 1)) (loc 4))(= (event 4) (third (trS 1))) (= (loc 5) (second (trS 1))))(and (= (first (trS 2)) (loc 4))(= (event 4) (third (trS 2))) (= (loc 5) (second (trS 2))))(and (= (first (trS 3)) (loc 4))(= (event 4) (third (trS 3))) (= (loc 5) (second (trS 3))))(and (= (first (trS 4)) (loc 4))(= (event 4) (third (trS 4))) (= (loc 5) (second (trS 4))))(and (= (first (trS 5)) (loc 4))(= (event 4) (third (trS 5))) (= (loc 5) (second (trS 5))))(and (= (first (trS 6)) (loc 4))(= (event 4) (third (trS 6))) (= (loc 5) (second (trS 6))))(and (= (first (trS 7)) (loc 4))(= (event 4) (third (trS 7))) (= (loc 5) (second (trS 7))))(and (= (first (trS 8)) (loc 4))(= (event 4) (third (trS 8))) (= (loc 5) (second (trS 8)))))

;check that all transitions are labeled normal events on the normal path
(and(notF 0)(notF 1)(notF 2)(notF 3)(notF 4))

;array to store all observable events of the normal path
(and(ite (and (=(obs (event 0)) true)(not(= (event 0)(event -1)))) (and (= (count 1) (+ (count 0) 1))(= (store obsn (count 0)(event 0)) obsn)) (= (count 1)(count 0)))(ite (and (=(obs (event 1)) true)(not(= (event 1)(event 0)))) (and (= (count 2) (+ (count 1) 1))(= (store obsn (count 1)(event 1)) obsn)) (= (count 2)(count 1)))(ite (and (=(obs (event 2)) true)(not(= (event 2)(event 1)))) (and (= (count 3) (+ (count 2) 1))(= (store obsn (count 2)(event 2)) obsn)) (= (count 3)(count 2)))(ite (and (=(obs (event 3)) true)(not(= (event 3)(event 2)))) (and (= (count 4) (+ (count 3) 1))(= (store obsn (count 3)(event 3)) obsn)) (= (count 4)(count 3)))(ite (and (=(obs (event 4)) true)(not(= (event 4)(event 3)))) (and (= (count 5) (+ (count 4) 1))(= (store obsn (count 4)(event 4)) obsn)) (= (count 5)(count 4))))
(= ln 5))



;check that two path(normal and fauly path) are the same observation
(assert (= obsn obsf))
(assert ( = (count ln)(countf 10)))

;get information about sat and unsat
(check-sat)
(get-value(ln))
(get-value(lf))
(get-value ((loc 0)(loc 1)(loc 2)(loc 3)(loc 4)(loc 5)))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)(locFault 5)))
(get-value ((event 0)(event 1)(event 2)(event 3)(event 4)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)(eventFault 4)))
(get-unsat-core)
(get-info :all-statistics)
