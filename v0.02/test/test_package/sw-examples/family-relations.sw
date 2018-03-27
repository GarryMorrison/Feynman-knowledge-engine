-- family relations:
-- define: mother, father, son, daughter, wife, husband
-- and the rest follows

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

brother-in-law |*> #=> husband sister |_self> 
sister-in-law |*> #=> wife brother |_self>
mother-in-law |*> #=> mother wife |_self> + mother husband |_self>
father-in-law |*> #=> father wife |_self> + father husband |_self>

