:- dynamic inCrest/3.
:- volatile inCrest/3.


%da implementare gli errori controllati
shadow(s0, s_0_0_1).
%shadow(s0, s_0_0_0).
shadow(s1, s_0_m1).
%shadow(s1, s_0_0).

shadow(z0, s_0_m1_m1).
shadow(z1, s_0_1).
%shadow(z1, s_0_0).

shadow(i0, s_0).
shadow(i1, s_0_0_0_0).

shadow(o0, s_0_0).

shadow(t0, s_0_0_0).
shadow(t1, s_0_1).
shadow(t2, s_0_m1_0).
shadow(t3, s_0_m1).

shadow(l0, s_0_0_0).
shadow(l1, s_0_m2).
shadow(l2, s_0_1_1).
shadow(l3, s_0_0).

shadow(j0, s_0_0_0).
shadow(j1, s_0_2).
shadow(j2, s_0_0_m1).
shadow(j3, s_0_0).



%cresta di prova
%inCrest(crest, s0, 0).
%inCrest(crest, s0, 1).
%inCrest(crest, s0, 2).
%inCrest(crest, s0, 3).
%inCrest(crest, s0, 4).
%inCrest(crest, s0, 5).
%inCrest(crest, s0, 6).
%inCrest(crest, s0, 7).
%inCrest(crest, s0, 8).
%inCrest(crest, s0, 9).

%inCrest(crest, s0_1, 0).
%inCrest(crest, s0_m2, 1).
%inCrest(crest, s0_2, 2).
%inCrest(crest, s0_2, 3).
%inCrest(crest, s0_m1, 4).
%inCrest(crest, s0_0, 5).
%inCrest(crest, s0_m1, 6).
%inCrest(crest, s0_1, 7).
%inCrest(crest, s0_m2, 8).

%inCrest(crest, s0_1_m1, 0).
%inCrest(crest, s0_m2_0, 1).
%inCrest(crest, s0_2_4, 2).
%inCrest(crest, s0_2_1, 3).
%inCrest(crest, s0_m1_m1, 4).
%inCrest(crest, s0_0_m1, 5).
%inCrest(crest, s0_m1_0, 6).
%inCrest(crest, s0_1_m1, 7).

%inCrest(crest, s0_1_m1_1, 0).
%inCrest(crest, s0_m2_0_2, 1).
%inCrest(crest, s0_2_4_3, 2).
%inCrest(crest, s0_2_1_1, 3).
%inCrest(crest, s0_m1_m1_m2, 4).
%inCrest(crest, s0_0_m1_0, 5).
%inCrest(crest, s0_m1_0_m2, 6).




%regola per il bestFit
bestFit(Shape, X):-
    shadow(Shape, Seq),
    inCrest(crest, Seq, X).


