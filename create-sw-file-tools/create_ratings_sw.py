#!/opt/python3/bin/python3

#source_data = "votes-ratings-title.txt"
source_data = "movie-only-votes-ratings-title.txt"
dest_sw = "imdb-ratings.sw"
#voting_threshold = 10000  # minimum number of votes for a movie to consider it interesting enough to keep.
voting_threshold = 0

with open(source_data,'r') as f:
  for line in f:
    try:
      votes,rating,movie = line.split(" ",2)
      if int(votes) >= voting_threshold:
        votes_ket = "|votes: " + votes + ">"
        rating_ket = "|rating: " + rating + ">"
        movie_ket = "|movie: " + movie.rstrip() + ">"   # NB: need to be sure this is identical to in imdb.sw else useless!
        print("imdb-votes " + movie_ket + " => " + votes_ket)
        print("imdb-votes-self " + movie_ket + " => " + votes + movie_ket)
        print("imdb-rating " + movie_ket + " => " + rating_ket)
        print("imdb-rating-self " + movie_ket + " => " + rating + movie_ket)
    except:
      continue
