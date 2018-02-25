-- see here for more details:
-- http://write-up.semantic-db.org/221-generating-random-grammatically-correct-sentences.html
-- reimplemented using v0.02 notation


frag |A> => |the woman saw>
frag |B> => |through the telescope>
frag |C> #=> spick-elt (|> . |young>)
frag |D> #=> spick-elt (|girl> . |boy>)
frag |E> #=> spick-elt (|> . |old> . |other>)
frag |F> #=> spick-elt (|man> . |woman> . |lady>)
frag |G> #=> frag (|E> . |F>)
frag |H> => |the>
frag |I> #=> frag (|H> . |C> . |D>)
frag |J> #=> frag (|H> . |E> . |F>)
frag |K> #=> frag spick-elt (|> . |I> . |J>)
frag |L> #=> frag (|A> . |K> . |B>)
frag |M> #=> frag spick-elt (|I> . |J>)
frag |N> => |saw>
frag |O> #=> frag (|M> . |N> . |K> . |B>)
frag |P> => |through the>
frag |Q> #=> spick-elt (|telescope> . |binoculars> . |night vision goggles>)
frag |R> #=> frag (|M> . |N> . |K> . |P> . |Q>)

sentence |*> #=> to-upper[1] smerge[" "] sdrop frag |R> _ |.>

