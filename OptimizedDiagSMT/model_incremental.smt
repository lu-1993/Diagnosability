(set-option :produce-unsat-cores true)

;declare data structure to store transitions

(declare-datatypes (T1) ((Pair (mk-pair (first T1) (second T1) (third T1)))))

(declare-fun trS (Int) (Pair Int))
(declare-const p10(Pair Int))
(declare-const p9(Pair Int))
(declare-const p8(Pair Int))
(declare-const p7(Pair Int))
(declare-const p6(Pair Int))
(declare-const p5(Pair Int))
(declare-const p4(Pair Int))
(declare-const p3(Pair Int))
(declare-const p2(Pair Int))
(declare-const p1(Pair Int))
;read all transitions of systems (finite automata) from modelsmt.txt

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
(declare-fun a0 () Bool)
(declare-fun a1 () Bool)
(declare-fun a2 () Bool)
(declare-fun a3 () Bool)
(declare-fun a4 () Bool)
(declare-fun a5 () Bool)
(declare-fun c0 () Bool)
(declare-fun b0 () Bool)
(declare-fun b1 () Bool)
(declare-fun b2 () Bool)
(declare-fun b3 () Bool)
(declare-fun b4 () Bool)
(declare-fun b5 () Bool)
;function to verify whether a given event (integer) is an observable event

(define-fun obs ((o Int)) Bool
( if (and ( >= o 1)( <= o 3))
true
false))

;define event (events of normal path) and eventFault (events of faulty path) and initialization
(declare-fun event (Int) Int)
(declare-fun eventFault (Int) Int)
(assert (= (event -1) 0))
(assert (= (eventFault -1) 0))
;define loc (states of normal path) and locFault (states of faulty path) and initialization (both begin from the state 1)
(declare-fun loc (Int) Int)
(declare-fun locFault (Int) Int)
(assert (= (loc 0) 1))
(assert (= (locFault 0) 1))
;declare two const. lf/ln: length fo faulty/normal path
(declare-const ln Int)
(declare-const lf Int)
;some functions to computer k-value on the specific transition (k represents the number of steps after the fault)
(define-fun ifault((fau Int)) Int
( if (> (eventFault fau) 5)
1
0))

(assert (=(ifault -1)0))

(declare-fun isfault (Int) Int)
(assert (=(isfault -1)0))
(declare-fun k (Int) Int)
(assert (= (k -1) -1))

(define-fun midk ((i Int)) Bool
( if (or (= (ifault i) 1)(= (isfault (- i 1)) 1))
(= (isfault i) 1)
(= (isfault i) 0)))
(define-fun compk ((i Int)) Bool
(if (=(isfault i)0)
(=(k i) -1)
(= (k i) (+(k (- i 1))1))))

;function to check whether a given event on the faulty path 

(define-fun existF((fau Int)) Bool
( if (> (eventFault fau) 5)
true
false))

(define-fun notF((nor Int)) Bool
( if (and ( >= (event nor) 1)(<= (event nor) 5))
true
false))

(declare-const obsf (Array Int Int))
(declare-fun countf (Int) Int)
(assert (= (countf 0) 0))
(assert ( = (countf -1) -1))
(assert ( = (store obsf -1 0) obsf ))

(declare-const obsn (Array Int Int))
(declare-fun count (Int) Int)
(assert (= (count 0) 0))
(assert ( = (count -1) -1))
(assert ( = (store obsn -1 0) obsn ))

(assert (=> a0 (and 
;construct normal path of length 1
(or(and (= (first (trS 1)) (loc 0))(= (event 0) (third (trS 1)))(= (loc 1) (second (trS 1))))(and (= (first (trS 2)) (loc 0))(= (event 0) (third (trS 2)))(= (loc 1) (second (trS 2))))(and (= (first (trS 3)) (loc 0))(= (event 0) (third (trS 3)))(= (loc 1) (second (trS 3))))(and (= (first (trS 4)) (loc 0))(= (event 0) (third (trS 4)))(= (loc 1) (second (trS 4))))(and (= (first (trS 5)) (loc 0))(= (event 0) (third (trS 5)))(= (loc 1) (second (trS 5))))(and (= (first (trS 6)) (loc 0))(= (event 0) (third (trS 6)))(= (loc 1) (second (trS 6))))(and (= (first (trS 7)) (loc 0))(= (event 0) (third (trS 7)))(= (loc 1) (second (trS 7))))(and (= (first (trS 8)) (loc 0))(= (event 0) (third (trS 8)))(= (loc 1) (second (trS 8))))(and (= (first (trS 9)) (loc 0))(= (event 0) (third (trS 9)))(= (loc 1) (second (trS 9))))(and (= (first (trS 10)) (loc 0))(= (event 0) (third (trS 10)))(= (loc 1) (second (trS 10)))))
;array to store all observable events of the normal path
(and(ite (and (=(obs (event 0)) true)(not(=(event 0)(select obsn ( - (count 0) 1 )))))(and (= (count 1) (+ (count 0) 1))(= (store obsn (count 0) (event 0)) obsn)) (= (count 1)(count 0))))
(notF 0)
(= obsn obsf)
(ite(and( < (count 1)(countf lf)))
(> ln 1)
(ite(and( = (count 1)(countf lf)))
(and (= ln 1) (not a1))
false))
)
)
)
(assert (=> a1 (and 
;construct normal path of length 2
(or(and (= (first (trS 1)) (loc 1))(= (event 1) (third (trS 1)))(= (loc 2) (second (trS 1))))(and (= (first (trS 2)) (loc 1))(= (event 1) (third (trS 2)))(= (loc 2) (second (trS 2))))(and (= (first (trS 3)) (loc 1))(= (event 1) (third (trS 3)))(= (loc 2) (second (trS 3))))(and (= (first (trS 4)) (loc 1))(= (event 1) (third (trS 4)))(= (loc 2) (second (trS 4))))(and (= (first (trS 5)) (loc 1))(= (event 1) (third (trS 5)))(= (loc 2) (second (trS 5))))(and (= (first (trS 6)) (loc 1))(= (event 1) (third (trS 6)))(= (loc 2) (second (trS 6))))(and (= (first (trS 7)) (loc 1))(= (event 1) (third (trS 7)))(= (loc 2) (second (trS 7))))(and (= (first (trS 8)) (loc 1))(= (event 1) (third (trS 8)))(= (loc 2) (second (trS 8))))(and (= (first (trS 9)) (loc 1))(= (event 1) (third (trS 9)))(= (loc 2) (second (trS 9))))(and (= (first (trS 10)) (loc 1))(= (event 1) (third (trS 10)))(= (loc 2) (second (trS 10)))))
;array to store all observable events of the normal path
(and(ite (and (=(obs (event 1)) true)(not(=(event 1)(select obsn ( - (count 1) 1 )))))(and (= (count 2) (+ (count 1) 1))(= (store obsn (count 1) (event 1)) obsn)) (= (count 2)(count 1))))
(notF 1)
(= obsn obsf)
(ite(and( < (count 2)(countf lf)))
(> ln 2)
(ite(and( = (count 2)(countf lf)))
(and (= ln 2) (not a2))
false))
)
)
)
(assert (=> a2 (and 
;construct normal path of length 3
(or(and (= (first (trS 1)) (loc 2))(= (event 2) (third (trS 1)))(= (loc 3) (second (trS 1))))(and (= (first (trS 2)) (loc 2))(= (event 2) (third (trS 2)))(= (loc 3) (second (trS 2))))(and (= (first (trS 3)) (loc 2))(= (event 2) (third (trS 3)))(= (loc 3) (second (trS 3))))(and (= (first (trS 4)) (loc 2))(= (event 2) (third (trS 4)))(= (loc 3) (second (trS 4))))(and (= (first (trS 5)) (loc 2))(= (event 2) (third (trS 5)))(= (loc 3) (second (trS 5))))(and (= (first (trS 6)) (loc 2))(= (event 2) (third (trS 6)))(= (loc 3) (second (trS 6))))(and (= (first (trS 7)) (loc 2))(= (event 2) (third (trS 7)))(= (loc 3) (second (trS 7))))(and (= (first (trS 8)) (loc 2))(= (event 2) (third (trS 8)))(= (loc 3) (second (trS 8))))(and (= (first (trS 9)) (loc 2))(= (event 2) (third (trS 9)))(= (loc 3) (second (trS 9))))(and (= (first (trS 10)) (loc 2))(= (event 2) (third (trS 10)))(= (loc 3) (second (trS 10)))))
;array to store all observable events of the normal path
(and(ite (and (=(obs (event 2)) true)(not(=(event 2)(select obsn ( - (count 2) 1 )))))(and (= (count 3) (+ (count 2) 1))(= (store obsn (count 2) (event 2)) obsn)) (= (count 3)(count 2))))
(notF 2)
(= obsn obsf)
(ite(and( < (count 3)(countf lf)))
(> ln 3)
(ite(and( = (count 3)(countf lf)))
(and (= ln 3) (not a3))
false))
)
)
)
(assert (=> a3 (and 
;construct normal path of length 4
(or(and (= (first (trS 1)) (loc 3))(= (event 3) (third (trS 1)))(= (loc 4) (second (trS 1))))(and (= (first (trS 2)) (loc 3))(= (event 3) (third (trS 2)))(= (loc 4) (second (trS 2))))(and (= (first (trS 3)) (loc 3))(= (event 3) (third (trS 3)))(= (loc 4) (second (trS 3))))(and (= (first (trS 4)) (loc 3))(= (event 3) (third (trS 4)))(= (loc 4) (second (trS 4))))(and (= (first (trS 5)) (loc 3))(= (event 3) (third (trS 5)))(= (loc 4) (second (trS 5))))(and (= (first (trS 6)) (loc 3))(= (event 3) (third (trS 6)))(= (loc 4) (second (trS 6))))(and (= (first (trS 7)) (loc 3))(= (event 3) (third (trS 7)))(= (loc 4) (second (trS 7))))(and (= (first (trS 8)) (loc 3))(= (event 3) (third (trS 8)))(= (loc 4) (second (trS 8))))(and (= (first (trS 9)) (loc 3))(= (event 3) (third (trS 9)))(= (loc 4) (second (trS 9))))(and (= (first (trS 10)) (loc 3))(= (event 3) (third (trS 10)))(= (loc 4) (second (trS 10)))))
;array to store all observable events of the normal path
(and(ite (and (=(obs (event 3)) true)(not(=(event 3)(select obsn ( - (count 3) 1 )))))(and (= (count 4) (+ (count 3) 1))(= (store obsn (count 3) (event 3)) obsn)) (= (count 4)(count 3))))
(notF 3)
(= obsn obsf)
(ite(and( < (count 4)(countf lf)))
(> ln 4)
(ite(and( = (count 4)(countf lf)))
(and (= ln 4) (not a4))
false))
)
)
)
(assert (=> a4 (and 
;construct normal path of length 5
(or(and (= (first (trS 1)) (loc 4))(= (event 4) (third (trS 1)))(= (loc 5) (second (trS 1))))(and (= (first (trS 2)) (loc 4))(= (event 4) (third (trS 2)))(= (loc 5) (second (trS 2))))(and (= (first (trS 3)) (loc 4))(= (event 4) (third (trS 3)))(= (loc 5) (second (trS 3))))(and (= (first (trS 4)) (loc 4))(= (event 4) (third (trS 4)))(= (loc 5) (second (trS 4))))(and (= (first (trS 5)) (loc 4))(= (event 4) (third (trS 5)))(= (loc 5) (second (trS 5))))(and (= (first (trS 6)) (loc 4))(= (event 4) (third (trS 6)))(= (loc 5) (second (trS 6))))(and (= (first (trS 7)) (loc 4))(= (event 4) (third (trS 7)))(= (loc 5) (second (trS 7))))(and (= (first (trS 8)) (loc 4))(= (event 4) (third (trS 8)))(= (loc 5) (second (trS 8))))(and (= (first (trS 9)) (loc 4))(= (event 4) (third (trS 9)))(= (loc 5) (second (trS 9))))(and (= (first (trS 10)) (loc 4))(= (event 4) (third (trS 10)))(= (loc 5) (second (trS 10)))))
;array to store all observable events of the normal path
(and(ite (and (=(obs (event 4)) true)(not(=(event 4)(select obsn ( - (count 4) 1 )))))(and (= (count 5) (+ (count 4) 1))(= (store obsn (count 4) (event 4)) obsn)) (= (count 5)(count 4))))
(notF 4)
(= obsn obsf)
(ite(and( < (count 5)(countf lf)))
(> ln 5)
(ite(and( = (count 5)(countf lf)))
(and (= ln 5) (not a5))
false))
)
)
)
(assert (=> b0 (and 
;construct faulty path of length 1
(or(and (= (first (trS 1)) (locFault 0))(= (eventFault 0) (third (trS 1)))(= (locFault  1) (second (trS 1))))(and (= (first (trS 2)) (locFault 0))(= (eventFault 0) (third (trS 2)))(= (locFault  1) (second (trS 2))))(and (= (first (trS 3)) (locFault 0))(= (eventFault 0) (third (trS 3)))(= (locFault  1) (second (trS 3))))(and (= (first (trS 4)) (locFault 0))(= (eventFault 0) (third (trS 4)))(= (locFault  1) (second (trS 4))))(and (= (first (trS 5)) (locFault 0))(= (eventFault 0) (third (trS 5)))(= (locFault  1) (second (trS 5))))(and (= (first (trS 6)) (locFault 0))(= (eventFault 0) (third (trS 6)))(= (locFault  1) (second (trS 6))))(and (= (first (trS 7)) (locFault 0))(= (eventFault 0) (third (trS 7)))(= (locFault  1) (second (trS 7))))(and (= (first (trS 8)) (locFault 0))(= (eventFault 0) (third (trS 8)))(= (locFault  1) (second (trS 8))))(and (= (first (trS 9)) (locFault 0))(= (eventFault 0) (third (trS 9)))(= (locFault  1) (second (trS 9))))(and (= (first (trS 10)) (locFault 0))(= (eventFault 0) (third (trS 10)))(= (locFault  1) (second (trS 10)))))
(compk 0)
(midk 0)
;array to store all observable events of the faulty path
(and(ite (and (=(obs (eventFault 0)) true)(not(=(eventFault 0)(select obsf ( - (countf 0) 1 )))))(and (= (countf 1) (+ (countf 0) 1))(= (store obsf (countf 0) (eventFault 0)) obsf)) (= (countf 1)(countf 0))))
)
)
)
(assert (=> b1 (and 
;construct faulty path of length 2
(or(and (= (first (trS 1)) (locFault 1))(= (eventFault 1) (third (trS 1)))(= (locFault  2) (second (trS 1))))(and (= (first (trS 2)) (locFault 1))(= (eventFault 1) (third (trS 2)))(= (locFault  2) (second (trS 2))))(and (= (first (trS 3)) (locFault 1))(= (eventFault 1) (third (trS 3)))(= (locFault  2) (second (trS 3))))(and (= (first (trS 4)) (locFault 1))(= (eventFault 1) (third (trS 4)))(= (locFault  2) (second (trS 4))))(and (= (first (trS 5)) (locFault 1))(= (eventFault 1) (third (trS 5)))(= (locFault  2) (second (trS 5))))(and (= (first (trS 6)) (locFault 1))(= (eventFault 1) (third (trS 6)))(= (locFault  2) (second (trS 6))))(and (= (first (trS 7)) (locFault 1))(= (eventFault 1) (third (trS 7)))(= (locFault  2) (second (trS 7))))(and (= (first (trS 8)) (locFault 1))(= (eventFault 1) (third (trS 8)))(= (locFault  2) (second (trS 8))))(and (= (first (trS 9)) (locFault 1))(= (eventFault 1) (third (trS 9)))(= (locFault  2) (second (trS 9))))(and (= (first (trS 10)) (locFault 1))(= (eventFault 1) (third (trS 10)))(= (locFault  2) (second (trS 10)))))
(compk 1)
(midk 1)
;array to store all observable events of the faulty path
(and(ite (and (=(obs (eventFault 1)) true)(not(=(eventFault 1)(select obsf ( - (countf 1) 1 )))))(and (= (countf 2) (+ (countf 1) 1))(= (store obsf (countf 1) (eventFault 1)) obsf)) (= (countf 2)(countf 1))))
)
)
)
(assert (=> b2 (and 
;construct faulty path of length 3
(or(and (= (first (trS 1)) (locFault 2))(= (eventFault 2) (third (trS 1)))(= (locFault  3) (second (trS 1))))(and (= (first (trS 2)) (locFault 2))(= (eventFault 2) (third (trS 2)))(= (locFault  3) (second (trS 2))))(and (= (first (trS 3)) (locFault 2))(= (eventFault 2) (third (trS 3)))(= (locFault  3) (second (trS 3))))(and (= (first (trS 4)) (locFault 2))(= (eventFault 2) (third (trS 4)))(= (locFault  3) (second (trS 4))))(and (= (first (trS 5)) (locFault 2))(= (eventFault 2) (third (trS 5)))(= (locFault  3) (second (trS 5))))(and (= (first (trS 6)) (locFault 2))(= (eventFault 2) (third (trS 6)))(= (locFault  3) (second (trS 6))))(and (= (first (trS 7)) (locFault 2))(= (eventFault 2) (third (trS 7)))(= (locFault  3) (second (trS 7))))(and (= (first (trS 8)) (locFault 2))(= (eventFault 2) (third (trS 8)))(= (locFault  3) (second (trS 8))))(and (= (first (trS 9)) (locFault 2))(= (eventFault 2) (third (trS 9)))(= (locFault  3) (second (trS 9))))(and (= (first (trS 10)) (locFault 2))(= (eventFault 2) (third (trS 10)))(= (locFault  3) (second (trS 10)))))
(compk 2)
(midk 2)
;array to store all observable events of the faulty path
(and(ite (and (=(obs (eventFault 2)) true)(not(=(eventFault 2)(select obsf ( - (countf 2) 1 )))))(and (= (countf 3) (+ (countf 2) 1))(= (store obsf (countf 2) (eventFault 2)) obsf)) (= (countf 3)(countf 2))))
)
)
)
(assert (=> b3 (and 
;construct faulty path of length 4
(or(and (= (first (trS 1)) (locFault 3))(= (eventFault 3) (third (trS 1)))(= (locFault  4) (second (trS 1))))(and (= (first (trS 2)) (locFault 3))(= (eventFault 3) (third (trS 2)))(= (locFault  4) (second (trS 2))))(and (= (first (trS 3)) (locFault 3))(= (eventFault 3) (third (trS 3)))(= (locFault  4) (second (trS 3))))(and (= (first (trS 4)) (locFault 3))(= (eventFault 3) (third (trS 4)))(= (locFault  4) (second (trS 4))))(and (= (first (trS 5)) (locFault 3))(= (eventFault 3) (third (trS 5)))(= (locFault  4) (second (trS 5))))(and (= (first (trS 6)) (locFault 3))(= (eventFault 3) (third (trS 6)))(= (locFault  4) (second (trS 6))))(and (= (first (trS 7)) (locFault 3))(= (eventFault 3) (third (trS 7)))(= (locFault  4) (second (trS 7))))(and (= (first (trS 8)) (locFault 3))(= (eventFault 3) (third (trS 8)))(= (locFault  4) (second (trS 8))))(and (= (first (trS 9)) (locFault 3))(= (eventFault 3) (third (trS 9)))(= (locFault  4) (second (trS 9))))(and (= (first (trS 10)) (locFault 3))(= (eventFault 3) (third (trS 10)))(= (locFault  4) (second (trS 10)))))
(compk 3)
(midk 3)
;array to store all observable events of the faulty path
(and(ite (and (=(obs (eventFault 3)) true)(not(=(eventFault 3)(select obsf ( - (countf 3) 1 )))))(and (= (countf 4) (+ (countf 3) 1))(= (store obsf (countf 3) (eventFault 3)) obsf)) (= (countf 4)(countf 3))))
)
)
)
(assert (=> b4 (and 
;construct faulty path of length 5
(or(and (= (first (trS 1)) (locFault 4))(= (eventFault 4) (third (trS 1)))(= (locFault  5) (second (trS 1))))(and (= (first (trS 2)) (locFault 4))(= (eventFault 4) (third (trS 2)))(= (locFault  5) (second (trS 2))))(and (= (first (trS 3)) (locFault 4))(= (eventFault 4) (third (trS 3)))(= (locFault  5) (second (trS 3))))(and (= (first (trS 4)) (locFault 4))(= (eventFault 4) (third (trS 4)))(= (locFault  5) (second (trS 4))))(and (= (first (trS 5)) (locFault 4))(= (eventFault 4) (third (trS 5)))(= (locFault  5) (second (trS 5))))(and (= (first (trS 6)) (locFault 4))(= (eventFault 4) (third (trS 6)))(= (locFault  5) (second (trS 6))))(and (= (first (trS 7)) (locFault 4))(= (eventFault 4) (third (trS 7)))(= (locFault  5) (second (trS 7))))(and (= (first (trS 8)) (locFault 4))(= (eventFault 4) (third (trS 8)))(= (locFault  5) (second (trS 8))))(and (= (first (trS 9)) (locFault 4))(= (eventFault 4) (third (trS 9)))(= (locFault  5) (second (trS 9))))(and (= (first (trS 10)) (locFault 4))(= (eventFault 4) (third (trS 10)))(= (locFault  5) (second (trS 10)))))
(compk 4)
(midk 4)
;array to store all observable events of the faulty path
(and(ite (and (=(obs (eventFault 4)) true)(not(=(eventFault 4)(select obsf ( - (countf 4) 1 )))))(and (= (countf 5) (+ (countf 4) 1))(= (store obsf (countf 4) (eventFault 4)) obsf)) (= (countf 5)(countf 4))))
)
)
)
(push)
(assert (=> c0 (and (= (k 3) 2)(= lf 4))))
(check-sat c0 b0 b1 b2 b3 a0 )
(echo "b0 b1 b2 b3 a0 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)))
(get-value (ln))
(get-value ((loc 0)(loc 1)))
(get-value ((event 0)))
(get-info :all-statistics)
(pop)
(push)
(assert (=> c0 (and (= (k 3) 2)(= lf 4))))
(check-sat c0 b0 b1 b2 b3 a0 a1 )
(echo "b0 b1 b2 b3 a0 a1 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)))
(get-value (ln))
(get-value ((loc 0)(loc 1)(loc 2)))
(get-value ((event 0)(event 1)))
(get-info :all-statistics)
(pop)
(push)
(assert (=> c0 (and (= (k 3) 2)(= lf 4))))
(check-sat c0 b0 b1 b2 b3 a0 a1 a2 )
(echo "b0 b1 b2 b3 a0 a1 a2 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)))
(get-value (ln))
(get-value ((loc 0)(loc 1)(loc 2)(loc 3)))
(get-value ((event 0)(event 1)(event 2)))
(get-info :all-statistics)
(pop)
(push)
(assert (=> c0 (and (= (k 3) 2)(= lf 4))))
(check-sat c0 b0 b1 b2 b3 a0 a1 a2 a3 )
(echo "b0 b1 b2 b3 a0 a1 a2 a3 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)))
(get-value (ln))
(get-value ((loc 0)(loc 1)(loc 2)(loc 3)(loc 4)))
(get-value ((event 0)(event 1)(event 2)(event 3)))
(get-info :all-statistics)
(pop)
(push)
(assert (=> c0 (and (= (k 3) 2)(= lf 4))))
(check-sat c0 b0 b1 b2 b3 a0 a1 a2 a3 a4 )
(echo "b0 b1 b2 b3 a0 a1 a2 a3 a4 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)))
(get-value (ln))
(get-value ((loc 0)(loc 1)(loc 2)(loc 3)(loc 4)(loc 5)))
(get-value ((event 0)(event 1)(event 2)(event 3)(event 4)))
(get-info :all-statistics)
(pop)
(push)
(assert (=> c0 (and (= (k 4) 2)(= lf 5))))
(check-sat c0 b0 b1 b2 b3 b4 a0 )
(echo "b0 b1 b2 b3 b4 a0 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)(locFault 5)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)(eventFault 4)))
(get-value (ln))
(get-value ((loc 0)(loc 1)))
(get-value ((event 0)))
(get-info :all-statistics)
(pop)
(push)
(assert (=> c0 (and (= (k 4) 2)(= lf 5))))
(check-sat c0 b0 b1 b2 b3 b4 a0 a1 )
(echo "b0 b1 b2 b3 b4 a0 a1 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)(locFault 5)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)(eventFault 4)))
(get-value (ln))
(get-value ((loc 0)(loc 1)(loc 2)))
(get-value ((event 0)(event 1)))
(get-info :all-statistics)
(pop)
(push)
(assert (=> c0 (and (= (k 4) 2)(= lf 5))))
(check-sat c0 b0 b1 b2 b3 b4 a0 a1 a2 )
(echo "b0 b1 b2 b3 b4 a0 a1 a2 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)(locFault 5)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)(eventFault 4)))
(get-value (ln))
(get-value ((loc 0)(loc 1)(loc 2)(loc 3)))
(get-value ((event 0)(event 1)(event 2)))
(get-info :all-statistics)
(pop)
(push)
(assert (=> c0 (and (= (k 4) 2)(= lf 5))))
(check-sat c0 b0 b1 b2 b3 b4 a0 a1 a2 a3 )
(echo "b0 b1 b2 b3 b4 a0 a1 a2 a3 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)(locFault 5)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)(eventFault 4)))
(get-value (ln))
(get-value ((loc 0)(loc 1)(loc 2)(loc 3)(loc 4)))
(get-value ((event 0)(event 1)(event 2)(event 3)))
(get-info :all-statistics)
(pop)
(push)
(assert (=> c0 (and (= (k 4) 2)(= lf 5))))
(check-sat c0 b0 b1 b2 b3 b4 a0 a1 a2 a3 a4 )
(echo "b0 b1 b2 b3 b4 a0 a1 a2 a3 a4 ")
(get-value (lf))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)(locFault 5)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)(eventFault 4)))
(get-value (ln))
(get-value ((loc 0)(loc 1)(loc 2)(loc 3)(loc 4)(loc 5)))
(get-value ((event 0)(event 1)(event 2)(event 3)(event 4)))
(get-info :all-statistics)
(pop)