|context> => |context: George>

-- George is just some fictional character
spell |word: george> => |letter: g> . |letter: e> . |letter: o> . |letter: r> . |letter: g> . |letter: e>

|word: george> => |person: George>
age |person: George> => |age: 29>
dob |person: George> => |date: 1984-05-23>
hair-colour |person: George> => |hair-colour: brown>
eye-colour |person: George> => |eye-colour: blue>
gender |person: George> => |gender: male>
height |person: George> => |height: cm: 176>
wife |person: George> => |person: Beth>
occupation |person: George> => |occupation: car salesman>
friends |person: George> => |person: Fred> + |person: Jane> + |person: Liz> + |person: Andrew>
mother |person: George> => |person: Sarah>
father |person: George> => |person: David>
sisters |person: George> => |person: Emily>
brothers |person: George> => |person: Frank> + |person: Tim> + |person: Sam>

siblings |person: George> => brothers |_self> + sisters |_self>
parents |person: George> => mother |_self> + father |_self>
family |person: George> => parents |_self> + siblings |_self>
family-and-friends |person: George> => family |_self> + friends |_self>


email |person: George> => |email: george.douglas@gmail.com>
education |person: George> => |education: high-school>

-- an OK swimmer, but not a great one.
can-swim |person: George> => 0.7 |yes>

-- George's father is dead:
is-dead |person: David Douglas> => |yes>

-- define our find operators:
find-path (*) #=> find-path-between(|person: George>, |_self>)
find-steps (*) #=> find-steps-between(|person: George>, |_self>)
