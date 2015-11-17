comments-per-diary |*> #=> round[1] arithmetic(comments |_self>,|/>,diaries |_self>)
comments-per-day |*> #=> round[2] arithmetic(comments|_self>,|/>,|30>)
diaries-per-day |*> #=> round[2] arithmetic(diaries|_self>,|/>,|30>)
comment-delta |*> #=> arithmetic(comments |_self>,|->,previous-comments |_self>)
diary-delta |*> #=> arithmetic(diaries |_self>,|->,previous-diaries |_self>)
comment-delta-is-greater-0 |*> #=> is-greater-than[0] comment-delta |_self>
diary-delta-is-greater-0 |*> #=> is-greater-than[0] diary-delta |_self>
-- percent-total-comments |*> #=> round[2] times[100] arithmetic(comments|_self>,|/>,|2042>)
-- percent-total-diaries |*> #=> round[2] times[100] arithmetic(diaries|_self>,|/>,|197>)

 |t1> #=> rank-table[kuron,comments,comment-delta,comments-per-day,comments-per-diary] select[1,20] reverse sort-by[comments] "" |list>

 |t2> #=> rank-table[kuron,diaries,diary-delta,diaries-per-day] select[1,20] reverse sort-by[diaries] "" |list>

 |t3> #=> strict-rank-table[kuron,comments-per-diary] reverse sort-by[comments-per-diary] "" |list>

 |s1> #=> rank-table[kuron,comments,previous-comments,comment-delta,comments-per-day,comments-per-diary] select[1,20] reverse sort-by[comments] "" |list>

 |s2> #=> rank-table[kuron,diaries,previous-diaries,diary-delta,diaries-per-day] select[1,20] reverse sort-by[diaries] "" |list>

 |s3> #=> rank-table[kuron,comments,previous-comments,comment-delta] select[1,20] reverse sort-by[comment-delta] such-that[comment-delta-is-greater-0] "" |list>

 |s4> #=> rank-table[kuron,diaries,previous-diaries,diary-delta] select[1,20] reverse sort-by[diary-delta] such-that[diary-delta-is-greater-0] "" |list>

 |u1> #=> rank-table[kuron,comments,percent-total-comments] select[1,20] reverse sort-by[comments] "" |list>

 |u2> #=> rank-table[kuron,diaries,percent-total-diaries] select[1,20] reverse sort-by[diaries] "" |list>


|total comments> => pop-float comments "" |list>
|total diaries> => pop-float diaries "" |list>

percent-total-comments |*> #=> round[2] times[100] arithmetic(comments|_self>,|/>,push-float "" |total comments>)
percent-total-diaries |*> #=> round[2] times[100] arithmetic(diaries|_self>,|/>,push-float "" |total diaries>)

