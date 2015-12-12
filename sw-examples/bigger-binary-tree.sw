
----------------------------------------
|context> => |context: bigger binary tree>

supported-ops |*> => |op: left-op> + |op: right-op> + |op: child>
left-op |*> #=> merge-labels(|_self> + |0>)
right-op |*> #=> merge-labels(|_self> + |1>)
child |*> #=> left |_self> + right |_self>

supported-ops |x> => |op: left> + |op: right>
left |x> => |0>
right |x> => |1>

supported-ops |0> => |op: left> + |op: right>
left |0> => |00>
right |0> => |01>

supported-ops |1> => |op: left> + |op: right>
left |1> => |10>
right |1> => |11>

supported-ops |00> => |op: left> + |op: right>
left |00> => |000>
right |00> => |001>

supported-ops |01> => |op: left> + |op: right>
left |01> => |010>
right |01> => |011>

supported-ops |10> => |op: left> + |op: right>
left |10> => |100>
right |10> => |101>

supported-ops |11> => |op: left> + |op: right>
left |11> => |110>
right |11> => |111>

supported-ops |000> => |op: left> + |op: right>
left |000> => |0000>
right |000> => |0001>

supported-ops |001> => |op: left> + |op: right>
left |001> => |0010>
right |001> => |0011>

supported-ops |010> => |op: left> + |op: right>
left |010> => |0100>
right |010> => |0101>

supported-ops |011> => |op: left> + |op: right>
left |011> => |0110>
right |011> => |0111>

supported-ops |100> => |op: left> + |op: right>
left |100> => |1000>
right |100> => |1001>

supported-ops |101> => |op: left> + |op: right>
left |101> => |1010>
right |101> => |1011>

supported-ops |110> => |op: left> + |op: right>
left |110> => |1100>
right |110> => |1101>

supported-ops |111> => |op: left> + |op: right>
left |111> => |1110>
right |111> => |1111>

supported-ops |0000> => |op: left> + |op: right>
left |0000> => |00000>
right |0000> => |00001>

supported-ops |0001> => |op: left> + |op: right>
left |0001> => |00010>
right |0001> => |00011>

supported-ops |0010> => |op: left> + |op: right>
left |0010> => |00100>
right |0010> => |00101>

supported-ops |0011> => |op: left> + |op: right>
left |0011> => |00110>
right |0011> => |00111>

supported-ops |0100> => |op: left> + |op: right>
left |0100> => |01000>
right |0100> => |01001>

supported-ops |0101> => |op: left> + |op: right>
left |0101> => |01010>
right |0101> => |01011>

supported-ops |0110> => |op: left> + |op: right>
left |0110> => |01100>
right |0110> => |01101>

supported-ops |0111> => |op: left> + |op: right>
left |0111> => |01110>
right |0111> => |01111>

supported-ops |1000> => |op: left> + |op: right>
left |1000> => |10000>
right |1000> => |10001>

supported-ops |1001> => |op: left> + |op: right>
left |1001> => |10010>
right |1001> => |10011>

supported-ops |1010> => |op: left> + |op: right>
left |1010> => |10100>
right |1010> => |10101>

supported-ops |1011> => |op: left> + |op: right>
left |1011> => |10110>
right |1011> => |10111>

supported-ops |1100> => |op: left> + |op: right>
left |1100> => |11000>
right |1100> => |11001>

supported-ops |1101> => |op: left> + |op: right>
left |1101> => |11010>
right |1101> => |11011>

supported-ops |1110> => |op: left> + |op: right>
left |1110> => |11100>
right |1110> => |11101>

supported-ops |1111> => |op: left> + |op: right>
left |1111> => |11110>
right |1111> => |11111>

supported-ops |00000> => |op: left> + |op: right>
left |00000> => |000000>
right |00000> => |000001>

supported-ops |00001> => |op: left> + |op: right>
left |00001> => |000010>
right |00001> => |000011>

supported-ops |00010> => |op: left> + |op: right>
left |00010> => |000100>
right |00010> => |000101>

supported-ops |00011> => |op: left> + |op: right>
left |00011> => |000110>
right |00011> => |000111>

supported-ops |00100> => |op: left> + |op: right>
left |00100> => |001000>
right |00100> => |001001>

supported-ops |00101> => |op: left> + |op: right>
left |00101> => |001010>
right |00101> => |001011>

supported-ops |00110> => |op: left> + |op: right>
left |00110> => |001100>
right |00110> => |001101>

supported-ops |00111> => |op: left> + |op: right>
left |00111> => |001110>
right |00111> => |001111>

supported-ops |01000> => |op: left> + |op: right>
left |01000> => |010000>
right |01000> => |010001>

supported-ops |01001> => |op: left> + |op: right>
left |01001> => |010010>
right |01001> => |010011>

supported-ops |01010> => |op: left> + |op: right>
left |01010> => |010100>
right |01010> => |010101>

supported-ops |01011> => |op: left> + |op: right>
left |01011> => |010110>
right |01011> => |010111>

supported-ops |01100> => |op: left> + |op: right>
left |01100> => |011000>
right |01100> => |011001>

supported-ops |01101> => |op: left> + |op: right>
left |01101> => |011010>
right |01101> => |011011>

supported-ops |01110> => |op: left> + |op: right>
left |01110> => |011100>
right |01110> => |011101>

supported-ops |01111> => |op: left> + |op: right>
left |01111> => |011110>
right |01111> => |011111>

supported-ops |10000> => |op: left> + |op: right>
left |10000> => |100000>
right |10000> => |100001>

supported-ops |10001> => |op: left> + |op: right>
left |10001> => |100010>
right |10001> => |100011>

supported-ops |10010> => |op: left> + |op: right>
left |10010> => |100100>
right |10010> => |100101>

supported-ops |10011> => |op: left> + |op: right>
left |10011> => |100110>
right |10011> => |100111>

supported-ops |10100> => |op: left> + |op: right>
left |10100> => |101000>
right |10100> => |101001>

supported-ops |10101> => |op: left> + |op: right>
left |10101> => |101010>
right |10101> => |101011>

supported-ops |10110> => |op: left> + |op: right>
left |10110> => |101100>
right |10110> => |101101>

supported-ops |10111> => |op: left> + |op: right>
left |10111> => |101110>
right |10111> => |101111>

supported-ops |11000> => |op: left> + |op: right>
left |11000> => |110000>
right |11000> => |110001>

supported-ops |11001> => |op: left> + |op: right>
left |11001> => |110010>
right |11001> => |110011>

supported-ops |11010> => |op: left> + |op: right>
left |11010> => |110100>
right |11010> => |110101>

supported-ops |11011> => |op: left> + |op: right>
left |11011> => |110110>
right |11011> => |110111>

supported-ops |11100> => |op: left> + |op: right>
left |11100> => |111000>
right |11100> => |111001>

supported-ops |11101> => |op: left> + |op: right>
left |11101> => |111010>
right |11101> => |111011>

supported-ops |11110> => |op: left> + |op: right>
left |11110> => |111100>
right |11110> => |111101>

supported-ops |11111> => |op: left> + |op: right>
left |11111> => |111110>
right |11111> => |111111>

supported-ops |000000> => |op: left> + |op: right>
left |000000> => |0000000>
right |000000> => |0000001>

supported-ops |000001> => |op: left> + |op: right>
left |000001> => |0000010>
right |000001> => |0000011>

supported-ops |000010> => |op: left> + |op: right>
left |000010> => |0000100>
right |000010> => |0000101>

supported-ops |000011> => |op: left> + |op: right>
left |000011> => |0000110>
right |000011> => |0000111>

supported-ops |000100> => |op: left> + |op: right>
left |000100> => |0001000>
right |000100> => |0001001>

supported-ops |000101> => |op: left> + |op: right>
left |000101> => |0001010>
right |000101> => |0001011>

supported-ops |000110> => |op: left> + |op: right>
left |000110> => |0001100>
right |000110> => |0001101>

supported-ops |000111> => |op: left> + |op: right>
left |000111> => |0001110>
right |000111> => |0001111>

supported-ops |001000> => |op: left> + |op: right>
left |001000> => |0010000>
right |001000> => |0010001>

supported-ops |001001> => |op: left> + |op: right>
left |001001> => |0010010>
right |001001> => |0010011>

supported-ops |001010> => |op: left> + |op: right>
left |001010> => |0010100>
right |001010> => |0010101>

supported-ops |001011> => |op: left> + |op: right>
left |001011> => |0010110>
right |001011> => |0010111>

supported-ops |001100> => |op: left> + |op: right>
left |001100> => |0011000>
right |001100> => |0011001>

supported-ops |001101> => |op: left> + |op: right>
left |001101> => |0011010>
right |001101> => |0011011>

supported-ops |001110> => |op: left> + |op: right>
left |001110> => |0011100>
right |001110> => |0011101>

supported-ops |001111> => |op: left> + |op: right>
left |001111> => |0011110>
right |001111> => |0011111>

supported-ops |010000> => |op: left> + |op: right>
left |010000> => |0100000>
right |010000> => |0100001>

supported-ops |010001> => |op: left> + |op: right>
left |010001> => |0100010>
right |010001> => |0100011>

supported-ops |010010> => |op: left> + |op: right>
left |010010> => |0100100>
right |010010> => |0100101>

supported-ops |010011> => |op: left> + |op: right>
left |010011> => |0100110>
right |010011> => |0100111>

supported-ops |010100> => |op: left> + |op: right>
left |010100> => |0101000>
right |010100> => |0101001>

supported-ops |010101> => |op: left> + |op: right>
left |010101> => |0101010>
right |010101> => |0101011>

supported-ops |010110> => |op: left> + |op: right>
left |010110> => |0101100>
right |010110> => |0101101>

supported-ops |010111> => |op: left> + |op: right>
left |010111> => |0101110>
right |010111> => |0101111>

supported-ops |011000> => |op: left> + |op: right>
left |011000> => |0110000>
right |011000> => |0110001>

supported-ops |011001> => |op: left> + |op: right>
left |011001> => |0110010>
right |011001> => |0110011>

supported-ops |011010> => |op: left> + |op: right>
left |011010> => |0110100>
right |011010> => |0110101>

supported-ops |011011> => |op: left> + |op: right>
left |011011> => |0110110>
right |011011> => |0110111>

supported-ops |011100> => |op: left> + |op: right>
left |011100> => |0111000>
right |011100> => |0111001>

supported-ops |011101> => |op: left> + |op: right>
left |011101> => |0111010>
right |011101> => |0111011>

supported-ops |011110> => |op: left> + |op: right>
left |011110> => |0111100>
right |011110> => |0111101>

supported-ops |011111> => |op: left> + |op: right>
left |011111> => |0111110>
right |011111> => |0111111>

supported-ops |100000> => |op: left> + |op: right>
left |100000> => |1000000>
right |100000> => |1000001>

supported-ops |100001> => |op: left> + |op: right>
left |100001> => |1000010>
right |100001> => |1000011>

supported-ops |100010> => |op: left> + |op: right>
left |100010> => |1000100>
right |100010> => |1000101>

supported-ops |100011> => |op: left> + |op: right>
left |100011> => |1000110>
right |100011> => |1000111>

supported-ops |100100> => |op: left> + |op: right>
left |100100> => |1001000>
right |100100> => |1001001>

supported-ops |100101> => |op: left> + |op: right>
left |100101> => |1001010>
right |100101> => |1001011>

supported-ops |100110> => |op: left> + |op: right>
left |100110> => |1001100>
right |100110> => |1001101>

supported-ops |100111> => |op: left> + |op: right>
left |100111> => |1001110>
right |100111> => |1001111>

supported-ops |101000> => |op: left> + |op: right>
left |101000> => |1010000>
right |101000> => |1010001>

supported-ops |101001> => |op: left> + |op: right>
left |101001> => |1010010>
right |101001> => |1010011>

supported-ops |101010> => |op: left> + |op: right>
left |101010> => |1010100>
right |101010> => |1010101>

supported-ops |101011> => |op: left> + |op: right>
left |101011> => |1010110>
right |101011> => |1010111>

supported-ops |101100> => |op: left> + |op: right>
left |101100> => |1011000>
right |101100> => |1011001>

supported-ops |101101> => |op: left> + |op: right>
left |101101> => |1011010>
right |101101> => |1011011>

supported-ops |101110> => |op: left> + |op: right>
left |101110> => |1011100>
right |101110> => |1011101>

supported-ops |101111> => |op: left> + |op: right>
left |101111> => |1011110>
right |101111> => |1011111>

supported-ops |110000> => |op: left> + |op: right>
left |110000> => |1100000>
right |110000> => |1100001>

supported-ops |110001> => |op: left> + |op: right>
left |110001> => |1100010>
right |110001> => |1100011>

supported-ops |110010> => |op: left> + |op: right>
left |110010> => |1100100>
right |110010> => |1100101>

supported-ops |110011> => |op: left> + |op: right>
left |110011> => |1100110>
right |110011> => |1100111>

supported-ops |110100> => |op: left> + |op: right>
left |110100> => |1101000>
right |110100> => |1101001>

supported-ops |110101> => |op: left> + |op: right>
left |110101> => |1101010>
right |110101> => |1101011>

supported-ops |110110> => |op: left> + |op: right>
left |110110> => |1101100>
right |110110> => |1101101>

supported-ops |110111> => |op: left> + |op: right>
left |110111> => |1101110>
right |110111> => |1101111>

supported-ops |111000> => |op: left> + |op: right>
left |111000> => |1110000>
right |111000> => |1110001>

supported-ops |111001> => |op: left> + |op: right>
left |111001> => |1110010>
right |111001> => |1110011>

supported-ops |111010> => |op: left> + |op: right>
left |111010> => |1110100>
right |111010> => |1110101>

supported-ops |111011> => |op: left> + |op: right>
left |111011> => |1110110>
right |111011> => |1110111>

supported-ops |111100> => |op: left> + |op: right>
left |111100> => |1111000>
right |111100> => |1111001>

supported-ops |111101> => |op: left> + |op: right>
left |111101> => |1111010>
right |111101> => |1111011>

supported-ops |111110> => |op: left> + |op: right>
left |111110> => |1111100>
right |111110> => |1111101>

supported-ops |111111> => |op: left> + |op: right>
left |111111> => |1111110>
right |111111> => |1111111>
----------------------------------------
