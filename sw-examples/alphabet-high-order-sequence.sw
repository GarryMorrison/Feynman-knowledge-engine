full |range> => range(|1>,|65536>)
encode |a> => pick[10] full |range>
encode |b> => pick[10] full |range>
encode |c> => pick[10] full |range>
encode |d> => pick[10] full |range>
encode |e> => pick[10] full |range>
encode |f> => pick[10] full |range>
encode |g> => pick[10] full |range>
encode |h> => pick[10] full |range>
encode |i> => pick[10] full |range>
encode |j> => pick[10] full |range>
encode |k> => pick[10] full |range>
encode |l> => pick[10] full |range>
encode |m> => pick[10] full |range>
encode |n> => pick[10] full |range>
encode |o> => pick[10] full |range>
encode |p> => pick[10] full |range>
encode |q> => pick[10] full |range>
encode |r> => pick[10] full |range>
encode |s> => pick[10] full |range>
encode |t> => pick[10] full |range>
encode |u> => pick[10] full |range>
encode |v> => pick[10] full |range>
encode |w> => pick[10] full |range>
encode |x> => pick[10] full |range>
encode |y> => pick[10] full |range>
encode |z> => pick[10] full |range>


-- a b c d e f g h i j k l m n o p q r s t u v w x y z
sequence-number |node 0: *> => |sequence-0>
pattern |node 0: 0> => random-column[10] encode |a>
then |node 0: 0> => random-column[10] encode |b>

pattern |node 0: 1> => then |node 0: 0>
then |node 0: 1> => random-column[10] encode |c>

pattern |node 0: 2> => then |node 0: 1>
then |node 0: 2> => random-column[10] encode |d>

pattern |node 0: 3> => then |node 0: 2>
then |node 0: 3> => random-column[10] encode |e>

pattern |node 0: 4> => then |node 0: 3>
then |node 0: 4> => random-column[10] encode |f>

pattern |node 0: 5> => then |node 0: 4>
then |node 0: 5> => random-column[10] encode |g>

pattern |node 0: 6> => then |node 0: 5>
then |node 0: 6> => random-column[10] encode |h>

pattern |node 0: 7> => then |node 0: 6>
then |node 0: 7> => random-column[10] encode |i>

pattern |node 0: 8> => then |node 0: 7>
then |node 0: 8> => random-column[10] encode |j>

pattern |node 0: 9> => then |node 0: 8>
then |node 0: 9> => random-column[10] encode |k>

pattern |node 0: 10> => then |node 0: 9>
then |node 0: 10> => random-column[10] encode |l>

pattern |node 0: 11> => then |node 0: 10>
then |node 0: 11> => random-column[10] encode |m>

pattern |node 0: 12> => then |node 0: 11>
then |node 0: 12> => random-column[10] encode |n>

pattern |node 0: 13> => then |node 0: 12>
then |node 0: 13> => random-column[10] encode |o>

pattern |node 0: 14> => then |node 0: 13>
then |node 0: 14> => random-column[10] encode |p>

pattern |node 0: 15> => then |node 0: 14>
then |node 0: 15> => random-column[10] encode |q>

pattern |node 0: 16> => then |node 0: 15>
then |node 0: 16> => random-column[10] encode |r>

pattern |node 0: 17> => then |node 0: 16>
then |node 0: 17> => random-column[10] encode |s>

pattern |node 0: 18> => then |node 0: 17>
then |node 0: 18> => random-column[10] encode |t>

pattern |node 0: 19> => then |node 0: 18>
then |node 0: 19> => random-column[10] encode |u>

pattern |node 0: 20> => then |node 0: 19>
then |node 0: 20> => random-column[10] encode |v>

pattern |node 0: 21> => then |node 0: 20>
then |node 0: 21> => random-column[10] encode |w>

pattern |node 0: 22> => then |node 0: 21>
then |node 0: 22> => random-column[10] encode |x>

pattern |node 0: 23> => then |node 0: 22>
then |node 0: 23> => random-column[10] encode |y>

pattern |node 0: 24> => then |node 0: 23>
then |node 0: 24> => random-column[10] encode |z>


input-encode |*> #=> append-column[10] encode |_self>

step-1 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-2 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-3 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-4 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-5 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-6 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-7 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-8 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-9 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-10 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-11 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-12 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-13 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-14 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-15 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-16 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-17 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-18 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-19 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-20 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-21 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-22 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-23 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-24 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>
step-25 |*> #=> drop-below[0.05] similar-input[encode] extract-category then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] then drop-below[0.01] similar-input[pattern] input-encode |_self>

the-table |*> #=> table[ket,step-1,step-2,step-3,step-4,step-5,step-6,step-7,step-8,step-9,step-10,step-11,step-12,step-13,step-14,step-15,step-16,step-17,step-18,step-19,step-20,step-21,step-22,step-23,step-24,step-25] rel-kets[encode] |>

which-sequence |*> #=> sequence-number drop-below[0.5] 10 similar-input[pattern] input-encode |_self>

sequence-table |*> #=> table[ket,which-sequence] rel-kets[encode] |>
