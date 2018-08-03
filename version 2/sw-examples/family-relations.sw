-- family relations:
-- define only: mother, father, son, daughter, wife, husband, age
-- and the rest follows

-- define our not operator:
not |yes> => |no>
not |no> => |yes>
not |don't know> => |don't know>


child |*> #=> son |_self> + daughter |_self>
parent |*> #=> mother |_self> + father |_self>
sibling |*> #=> drop (clean child parent |_self> - |_self>)
brother |*> #=> drop (clean son parent |_self> - |_self>)
sister |*> #=> drop (clean daughter parent |_self> - |_self>)
brother-and-sister |*> #=> sibling |_self>

half-brother |*> #=> drop (son mother |_self> - son father |_self> ) + drop (son father |_self> - son mother |_self> )
half-sister |*> #=> drop (daughter mother |_self> - daughter father |_self> ) + drop (daughter father |_self> - daughter mother |_self> )

grand-parent |*> #=> parent parent |_self>
grand-mother |*> #=> mother parent |_self>
grand-father |*> #=> father parent |_self>
grand-child |*> #=> child child |_self>
grand-son |*> #=> son child |_self>
grand-daughter |*> #=> daughter child |_self>
great-grand-child |*> #=> child child child |_self>
great-grand-son |*> #=> son child child |_self>
great-grand-daughter |*> #=> daughter child child |_self>
great-grand-parent |*> #=> parent parent parent |_self>
great-grand-mother |*> #=> mother parent parent |_self>
great-grand-father |*> #=> father parent parent |_self>

uncle |*> #=> brother parent |_self> 
aunt |*> #=> sister parent |_self>
aunt-and-uncle |*> #=> aunt |_self> + uncle |_self>
great-uncle |*> #=> brother grand-parent |_self>
great-aunt |*> #=> sister grand-parent |_self>
great-aunt-and-uncle |*> #=> great-aunt |_self> + great-uncle |_self>

cousin |*> #=> clean child aunt-and-uncle |_self>
niece |*> #=> daughter brother-and-sister |_self>
nephew |*> #=> son brother-and-sister |_self>

-- brother-in-law |*> #=> husband sister |_self>
-- sister-in-law |*> #=> wife brother |_self>
brother-in-law |*> #=> brother wife |_self> + brother husband |_self> + husband sister |_self>
sister-in-law |*> #=> sister wife |_self> + sister husband |_self> + wife brother |_self>
mother-in-law |*> #=> mother wife |_self> + mother husband |_self>
father-in-law |*> #=> father wife |_self> + father husband |_self>
spouse |*> #=> wife |_self> + husband |_self>
is-married |*> #=> do-you-know spouse |_self>
not |yes> => |no>
not |no> => |yes>
is-not-married |*> #=> not do-you-know spouse |_self>


-- now a collection of is-a-x rules:
is-a-father |*> #=> is-mbr(|_self>, clean father child |_self>)
is-a-mother |*> #=> is-mbr(|_self>, clean mother child |_self>)
is-a-parent |*> #=> do-you-know child |_self>
is-a-son |*> #=> is-mbr(|_self>, clean son parent |_self>)
is-a-daughter |*> #=> is-mbr(|_self>, clean daughter parent |_self>)

is-a-grand-mother |*> #=> is-mbr(|_self>, clean mother parent child child |_self>)
is-a-grand-father |*> #=> is-mbr(|_self>, clean father parent child child |_self>)
is-a-grand-parent |*> #=> do-you-know child child |_self>

is-a-great-grand-mother |*> #=> is-mbr(|_self>, clean mother parent parent child child child |_self>)
is-a-great-grand-father |*> #=> is-mbr(|_self>, clean father parent parent child child child |_self>)
is-a-great-grand-parent |*> #=> do-you-know child child child |_self>

is-a-male |*> #=> or(is-a-son |_self>, is-a-father |_self>)
is-a-female |*> #=> or(is-a-daughter |_self>, is-a-mother |_self>)

is-an-uncle |*> #=> and(is-a-male |_self>, do-you-know child sibling |_self>)
is-an-aunt |*> #=> and(is-a-female |_self>, do-you-know child sibling |_self>)

is-a-husband |*> #=> and(is-a-male |_self>, do-you-know wife |_self>)
is-a-wife |*> #=> and(is-a-female |_self>, do-you-know husband |_self>)

is-a-brother |*> #=> and(is-a-male |_self>, do-you-know sibling |_self>)
is-a-sister |*> #=> and(is-a-female |_self>, do-you-know sibling |_self>)


-- define some is-a-x rules that require knowledge of age:
is-a-child |*> #=> is-in-range[0,17] age |_self>
is-a-teenager |*> #=> is-in-range[13,19] age |_self>
is-an-adult |*> #=> not is-in-range[0,17] age |_self>
is-a-man |*> #=> and(is-a-male |_self>, is-an-adult |_self>)
is-a-woman |*> #=> and(is-a-female |_self>, is-an-adult |_self>)
is-a-boy |*> #=> and(is-a-male |_self>, not is-an-adult |_self>)
is-a-girl |*> #=> and(is-a-female |_self>, not is-an-adult |_self>)
is-male-or-female |*> #=> or(is-a-male |_self>, is-a-female |_self>)
is-a-senior-citizen |*> #=> not is-in-range[0,59] age |_self>


-- now a collection of have-a-x rules:
have-a-child |*> #=> do-you-know child |_self>
have-a-brother |*> #=> do-you-know brother |_self>
have-a-sister |*> #=> do-you-know sister |_self>
have-a-wife |*> #=> do-you-know wife |_self>
have-a-husband |*> #=> do-you-know husband |_self>
have-an-uncle |*> #=> do-you-know uncle |_self>
have-an-aunt |*> #=> do-you-know aunt |_self>
have-a-cousin |*> #=> do-you-know cousin |_self>
have-a-niece |*> #=> do-you-know niece |_self>
have-a-nephew |*> #=> do-you-know nephew |_self>


-- now a collection of how-many rules:
how-many-children |*> #=> how-many child |_self>
how-many-grand-children |*> #=> how-many child child |_self>
how-many-great-grand-children |*> #=> how-many child child child |_self>
how-many-brothers |*> #=> how-many brother |_self>
how-many-sisters |*> #=> how-many sister |_self>
how-many-uncles |*> #=> how-many uncle |_self>
how-many-aunts |*> #=> how-many aunt |_self>
how-many-cousins |*> #=> how-many cousin |_self>
how-many-nieces |*> #=> how-many niece |_self>
how-many-nephews |*> #=> how-many nephew |_self>


-- some more rules about number of children:
have-1-child |*> #=> is-equal[1] how-many-children |_self>
have-2-children |*> #=> is-equal[2] how-many-children |_self>
have-3-children |*> #=> is-equal[3] how-many-children |_self>

have-k-children (*,*) #=> is-equal(|number:> __ |_self1>, how-many-children |_self2>)

