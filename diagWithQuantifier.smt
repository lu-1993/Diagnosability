; model

(set-option :produce-unsat-cores true)

;declare data structure to store transitions as follows:
;the first arguement stores the source state, the second for destination state, and the third for the event

(declare-datatypes (T1) ((Pair (mk-pair (first T1) (second T1) (third T1)))))

;read all transitions of systems (finite automaton) from model.txt
;for example, the first transition is from state 1 to state 2 with event 1

(declare-fun trS (Int) (Pair Int))
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

;define event (events of normal path) and eventFault (events of faulty path)

(declare-fun event (Int) Int)
(declare-fun eventFault (Int) Int)

;function to check whether a given event on the faulty/normal path is faulty (event 6) or normal (events 1-5)

(define-fun existF((fau Int)) Bool
  (if (= (eventFault fau) 6)
  true false))

(define-fun notF((nor Int)) Bool
  (if(and (>= (event nor) 1) (<= (event nor) 5)) true false))

;some functions to computer k-value on the specific transition (k represents the number of steps after the fault)

(define-fun ifault((fau Int)) Int
  (if (= (eventFault fau) 6)
  1 0))
(assert (=(ifault -1)0))

(declare-fun isfault (Int) Int)
(assert (=(isfault -1)0))

(declare-fun k (Int) Int)

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
(declare-const lnn Int)
(assert (= ln (+ lnn 1)))


;declare two arrays obsn/obsf: arrays to store all observable events on the normal/faulty path;

(declare-const obsn (Array Int Int))
(declare-const obsf (Array Int Int))

;declare constants count/countf to represent the index of the obsn/obsf and initialization

(declare-fun count (Int) Int)
(assert (= (count 0) 0))
(declare-fun countf (Int) Int)
(assert (= (countf 0) 0))

;construct a normal path with bound
(assert (!(exists ((j Int)) (and (>= j 1) (<= j 8) (= (first (trS j)) (loc 0))(= (event 0) (third (trS j))) (= (loc (+ 0 1)) (second (trS j))))):named np0))
(assert (!(exists ((j Int)) (and (>= j 1) (<= j 8) (= (first (trS j)) (loc 1))(= (event 1) (third (trS j))) (= (loc (+ 1 1)) (second (trS j))))):named np1))
(assert (!(exists ((j Int)) (and (>= j 1) (<= j 8) (= (first (trS j)) (loc 2))(= (event 2) (third (trS j))) (= (loc (+ 2 1)) (second (trS j))))):named np2))
(assert (!(exists ((j Int)) (and (>= j 1) (<= j 8) (= (first (trS j)) (loc 3))(= (event 3) (third (trS j))) (= (loc (+ 3 1)) (second (trS j))))):named np3))
(assert (!(exists ((j Int)) (and (>= j 1) (<= j 8) (= (first (trS j)) (loc 4))(= (event 4) (third (trS j))) (= (loc (+ 4 1)) (second (trS j))))):named np4))
(assert (!(exists ((j Int)) (and (>= j 1) (<= j 8) (= (first (trS j)) (loc 5))(= (event 5) (third (trS j))) (= (loc (+ 5 1)) (second (trS j))))):named np5))


;construct a faulty path with bound
(assert (!(exists ((jf Int)) (and (>= jf 1) (<= jf 8) (= (first (trS jf)) (locFault 0))(= (eventFault 0) (third (trS jf))) (= (locFault (+ 0 1)) (second (trS jf))))):named fp0))
(assert (!(exists ((jf Int)) (and (>= jf 1) (<= jf 8) (= (first (trS jf)) (locFault 1))(= (eventFault 1) (third (trS jf))) (= (locFault (+ 1 1)) (second (trS jf))))):named fp1))
(assert (!(exists ((jf Int)) (and (>= jf 1) (<= jf 8) (= (first (trS jf)) (locFault 2))(= (eventFault 2) (third (trS jf))) (= (locFault (+ 2 1)) (second (trS jf))))):named fp2))
(assert (!(exists ((jf Int)) (and (>= jf 1) (<= jf 8) (= (first (trS jf)) (locFault 3))(= (eventFault 3) (third (trS jf))) (= (locFault (+ 3 1)) (second (trS jf))))):named fp3))
(assert (!(exists ((jf Int)) (and (>= jf 1) (<= jf 8) (= (first (trS jf)) (locFault 4))(= (eventFault 4) (third (trS jf))) (= (locFault (+ 4 1)) (second (trS jf))))):named fp4))
(assert (!(exists ((jf Int)) (and (>= jf 1) (<= jf 8) (= (first (trS jf)) (locFault 5))(= (eventFault 5) (third (trS jf))) (= (locFault (+ 5 1)) (second (trS jf))))):named fp5))


;check that at least one fault occur on the faulty path

(assert (!(exists ((i Int))(and(<= i lf)(> i 0)(existF i))):named fau))

;check that all transitions are labeled normal events on the normal path

(assert (not(exists ((i Int))(and(= (notF i) false)(> i 0)(<= i lnn)))))

;computer k value in each step

(assert (and(compk 0)(compk 1)(compk 2)(compk 3)(compk 4)))
(assert (and(midk 0)(midk 1)(midk 2)(midk 3)(midk 4)))

;lenght of the faulty path
(assert (exists ((i Int))(and(= (k i) 3)(= lf (+ i 1))(> lf 0)(<= lf 5))))

;array to store all observable events of the faulty path

(assert (ite (=(obs (eventFault 0)) true) (and (= (countf 1) (+ (countf 0) 1))(= (store obsf (countf 0) (eventFault 0)) obsf)) (= (countf 1)(countf 0))))

(assert (forall ((i Int))(implies (and (> i 0)(<= i lf)(=(obs (eventFault i)) true)(not(= (eventFault i)(eventFault (- i 1))))) (and (= (store obsf (countf i) (eventFault i))obsf) (= (countf (+ i 1))(+ (countf i) 1))))))
(assert (forall ((i Int))(implies (and (> i 0)(<= i lf)(or(=(obs (eventFault i)) false)(= (eventFault i)(eventFault (- i 1)))))(= (countf (+ i 1))(countf i)))))

;array to store all observable events of the normal path

(assert (ite (=(obs (event 0)) true) (and (= (count 1) (+ (count 0) 1))(= (store obsn (count 0) (event 0)) obsn)) (= (count 1)(count 0))))
(assert (forall ((i Int))(implies (and (> i 0)(<= i lnn)(=(obs (event i)) true)(not(= (event i)(event (- i 1))))) (and (= (store obsn (count i) (event i))obsn) (= (count (+ i 1))(+ (count i) 1))))))

(assert (forall ((i Int))(implies (and (> i 0)(<= i lnn)(or(=(obs (event i)) false)(= (event i)(event (- i 1)))))(= (count (+ i 1))(count i)))))
(assert (forall ((i Int))(implies (> i lnn)(= (store obsn (count i) 0) obsn))))

;check that two path(normal and fauly path) are the same observation

(assert (!(= obsn obsf):named eqv))
(assert (= (count lnn)(countf 5)))

(check-sat)
(get-value(ln))
(get-value(lf))
(get-value ((loc 0)(loc 1)(loc 2)(loc 3)(loc 4)(loc 5)))
(get-value ((locFault 0)(locFault 1)(locFault 2)(locFault 3)(locFault 4)(locFault 5)))
(get-value ((event 0)(event 1)(event 2)(event 3)(event 4)))
(get-value ((eventFault 0)(eventFault 1)(eventFault 2)(eventFault 3)(eventFault 4)))
(get-unsat-core)
(get-info :all-statistics)
