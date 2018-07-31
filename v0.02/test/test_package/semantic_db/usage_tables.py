#######################################################################
# the semantic-db usage tables
# contains documentation for our built in operators, our sigmoids, and our worked examples
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 22/2/2018
# Update: 31/7/2018
# Copyright: GPLv3
#
# Usage:
#
#######################################################################

from semantic_db.functions import function_operators_usage, sequence_functions_usage, compound_table


# define our usage report function:
def usage(ops=None):
    if ops is None:  # print usage table
        s = 'Usage:\n'

        s += '  built in operators:\n'
        for key in sorted(built_in_table_usage):
            s += '    ' + key + '\n'

        s += '\n  sigmoids:\n'
        for key in sorted(sigmoid_table_usage):
            s += '    ' + key + '\n'

        s += '\n  operators:\n'
        for key in sorted(function_operators_usage):
            s += '    ' + key + '\n'

        s += '\n  sequence functions:\n'
        for key in sorted(sequence_functions_usage):
            s += '    ' + key + '\n'

        s += '\n  worked examples:\n'
        for key in sorted(examples_usage):
            s += '    ' + key + '\n'

    else:
        s = 'Usage:\n'
        for op in ops:
            if op in built_in_table_usage:
                s += 'built in operator:\n'
                s += '  ' + op + ':\n'
                s += built_in_table_usage[op] + '\n'

            if op in sigmoid_table_usage:
                s += 'sigmoid:\n'
                s += '  ' + op + ':\n'
                s += sigmoid_table_usage[op] + '\n'

            if op in function_operators_usage:
                s += 'operator:\n'
                s += '  ' + op + ':\n'
                s += function_operators_usage[op] + '\n'

            if op in sequence_functions_usage:
                s += 'sequence function:\n'
                s += '  ' + op + ':\n'
                s += sequence_functions_usage[op] + '\n'

            if op in examples_usage:
                s += 'worked example:\n'
                s += '  ' + op + ':\n'
                s += examples_usage[op] + '\n'

    print(s, end='')


# define our required dictionaries:
# operators built in to our ket/superposition/sequence classes that don't require parameters:
# eg: pick-elt sp
# see code.py
built_in_table = {}

# sigmoids that don't require parameters:
# by definition, sigmoids only change the coeff of kets, not the structure of the superposition/sequence
# eg: clean sp
# see sigmoids.py
sigmoid_table = {}

# related usage tables:
built_in_table_usage = {}
sigmoid_table_usage = {}
examples_usage = {}


# populate our usage tables:
# set invoke method:
built_in_table['pick-elt'] = 'pick_elt'
built_in_table['pick-an-element-from'] = 'pick_elt'
# set usage info:
built_in_table_usage['pick-elt'] = """
    description:
        pick-elt sp
        randomly pick an element from the given superposition, with equal probability
    
    alias: pick-an-element-from

    examples:
        pick-elt split |a b c d e>
        
    see also:
        weighted-pick-elt, spick-elt, sweighted-pick-elt    
"""
built_in_table_usage['pick-an-element-from'] = built_in_table_usage['pick-elt']


# set invoke method:
built_in_table['weighted-pick-elt'] = 'weighted_pick_elt'
# set usage info:
built_in_table_usage['weighted-pick-elt'] = """
    description:
        weighted-pick-elt sp
        randomly pick an element from the given superposition, weighted by the coefficients

    examples:
        weighted-pick-elt rank split |a b c d e>
    
    see also:
        pick-elt, spick-elt, sweighted-pick-elt
"""

# set invoke method:
built_in_table['spick-elt'] = 'spick_elt'
# set usage info:
built_in_table_usage['spick-elt'] = """
    description:
        spick-elt seq
        randomly pick a superposition from the given sequence, with equal probability

    examples:
        spick-elt (|a> + |b> + |c> . |d> . |e> + |f> . |g> + |h> + |i> + |j>)
            |e> + |f>

    see also:
        weighted-pick-elt, pick-elt, sweighted-pick-elt    
"""

# set invoke method:
compound_table['pick'] = ['pick', '', '']
# set usage info:
built_in_table_usage['pick'] = """
    description:
        pick[n] sp
        pick n kets from the given sp, with no duplication
        currently the order is not preserved, in future we may change this
        if n == 0, return |>

    examples:
        -- n is zero, so return don't know ket
        pick[0] range(|1>, |10>)
            |>
        
        pick[3] split |a b c d e f g h>
            |c> + |a> + |e>

        pick[10] range(|1>, |4096>)
            |1203> + |700> + |3564> + |198> + |3902> + |1609> + |3085> + |1368> + |104> + |854>

        ket-sort pick[10] range(|1>, |4096>)
            |688> + |708> + |1499> + |1569> + |1893> + |2988> + |3133> + |3144> + |3420> + |3644> 

    see also:
        pick-elt, spick-elt, weighted-pick-elt, ket-sort
"""

# set invoke method:
built_in_table['normalize'] = 'normalize'
compound_table['normalize'] = ['normalize', '', '']
# set usage info:
built_in_table_usage['normalize'] = """
    description:
        normalize sp
        normalize[t] sp
        normalize the coefficients of the given superposition so they sum to t
        if t is not specified, t defaults to 1

    examples:
        normalize split |a b c d e>
            0.2|a> + 0.2|b> + 0.2|c> + 0.2|d> + 0.2|e>

        normalize (2|a> + |b>)
            0.667|a> + 0.333|b>
        
        normalize[100] (2|a> + |b>)
            66.667|a> + 33.333|b>
    
    see also:
        rescale, snormalize, soft-max
"""

# set invoke method:
built_in_table['rescale'] = 'rescale'
compound_table['rescale'] = ['rescale', '', '']
# set usage info:
built_in_table_usage['rescale'] = """
    description:
        rescale sp
        rescale[t] sp
        rescale the coefficients of the given superposition so the coeff of the max element is t
        if t is not specified, t defaults to 1

    examples:
        rescale rank split |a b c d e f>
            0.167|a> + 0.333|b> + 0.5|c> + 0.667|d> + 0.833|e> + |f>

        rescale[100] rank split |a b c d e f>
            16.667|a> + 33.333|b> + 50|c> + 66.667|d> + 83.333|e> + 100|f>

    see also:
        srescale, normalize, snormalize, softmax
"""

# set invoke method:
built_in_table['softmax'] = 'softmax'
# set usage info:
built_in_table_usage['softmax'] = """
    description:
        softmax sp
        implement the softmax function
        
    algorithm:
        see: https://en.wikipedia.org/wiki/Softmax_function

    examples:
        -- let's consider a Gaussian:
        Gaussian[0.7] |age: 40>
            0.017|age: 36> + 0.047|age: 37> + 0.13|age: 38> + 0.36|age: 39> + |age: 40> + 0.36|age: 41> + 0.13|age: 42> + 0.047|age: 43> + 0.017|age: 44>
            
        bar-chart[50] Gaussian[0.7] |age: 40>
            ----------
            age: 36 :
            age: 37 : ||
            age: 38 : ||||||
            age: 39 : ||||||||||||||||||
            age: 40 : ||||||||||||||||||||||||||||||||||||||||||||||||||
            age: 41 : ||||||||||||||||||
            age: 42 : ||||||
            age: 43 : ||
            age: 44 :
            ----------
        
        -- now softmax it:
        softmax Gaussian[0.7] |age: 40>
            0.085|age: 36> + 0.087|age: 37> + 0.095|age: 38> + 0.12|age: 39> + 0.227|age: 40> + 0.12|age: 41> + 0.095|age: 42> + 0.087|age: 43> + 0.085|age: 44>

        bar-chart[50] softmax Gaussian[0.7] |age: 40>
            ----------
            age: 36 : ||||||||||||||||||
            age: 37 : |||||||||||||||||||
            age: 38 : ||||||||||||||||||||
            age: 39 : ||||||||||||||||||||||||||
            age: 40 : ||||||||||||||||||||||||||||||||||||||||||||||||||
            age: 41 : ||||||||||||||||||||||||||
            age: 42 : ||||||||||||||||||||
            age: 43 : |||||||||||||||||||
            age: 44 : ||||||||||||||||||
            ----------

        softmax (|a> + 2|b> + 3|c> + 4|d> + 5|e> + 6|f>)
            0.004|a> + 0.012|b> + 0.032|c> + 0.086|d> + 0.233|e> + 0.634|f>

    see also:
        rescale, srescale, normalize, snormalize 
"""


# set invoke method:
built_in_table['sdrop'] = 'sdrop'
# set usage info:
built_in_table_usage['sdrop'] = """
    description:
        sdrop seq
        sequence version of drop
        ie, drop all kets with coeff <= 0, and |>, from the given sequence

    examples:
        sdrop (|a> . 0|b> . -2|c> . 7.1|d>)
            |a> . 7.1|d>
        
        sdrop (|a> . |> . |b> . |> . |> . |c> . |>)
            |a> . |b> . |c>

    see also:
        drop
"""

# set invoke method:
built_in_table['drop'] = 'drop'
# set usage info:
built_in_table_usage['drop'] = """
    description:
        drop sp
        ie, drop all kets with coeff <= 0 from the given superposition

    examples:
        drop (|a> + 0|b> - 2|c> + 7.1|d>)
            |a> + 7.1|d>
            
    see also:
        drop-below, drop-above, sdrop
"""

# set invoke method:
compound_table['drop-below'] = ['drop_below', '', '']
# set usage info:
built_in_table_usage['drop-below'] = """
    description:
        drop-below[t] sp
        ie, drop all kets with coeff < t from the given superposition

    examples:
        drop-below[2] (- |a> + 0|b> + |c> + 2|d> + 3|e> + 4|f>) 
            2|d> + 3|e> + 4|f>

    see also:
        drop, drop-above, sdrop
"""

# set invoke method:
compound_table['drop-above'] = ['drop_above', '', '']
# set usage info:
built_in_table_usage['drop-above'] = """
    description:
        drop-above[t] sp
        ie, drop all kets with coeff > t from the given superposition

    examples:
        drop-above[2] (- |a> + 0|b> + |c> + 2|d> + 3|e> + 4|f>) 
            - |a> + 0|b> + |c> + 2|d>

    see also:
        drop, drop-above, sdrop
"""


# set invoke method:
built_in_table['sreverse'] = 'sreverse'
# set usage info:
built_in_table_usage['sreverse'] = """
    description:
        sreverse seq
        reverse the given sequence, leaving the order of the kets in the superpositions unchanged

    examples:
        sreverse (|a> . |b> . |c>)
            |c> . |b> . |a>
        
        sreverse (|a> + |b> . |c> + |d> . |e>)
            |e> . |c> + |d> . |a> + |b>
            
        -- reverse the order of the sequence of superpositions:
        long-display sreverse (|a> + |b> . |c> + |d> . |e>)
            seq |0> => |e>
            seq |1> => |c> + |d>
            seq |2> => |a> + |b>
            |e> . |c> + |d> . |a> + |b>
        
        -- reverse both the superpositions and the sequence:
        long-display sreverse reverse (|a> + |b> . |c> + |d> . |e>)
            seq |0> => |e>
            seq |1> => |d> + |c>
            seq |2> => |b> + |a>
            |e> . |d> + |c> . |b> + |a>
        
    see also:
        reverse
"""

# set invoke method:
built_in_table['reverse'] = 'reverse'
# set usage info:
built_in_table_usage['reverse'] = """
    description:
        reverse sp
        reverse the given superposition

    examples:
        reverse (|a> + |b> + |c>)
            |c> + |b> + |a>

        reverse (|a> + |b> . |c> + |d> . |e>)
            |b> + |a> . |d> + |c> . |e>

        -- reverse the order of the superpositions, but leave the sequence unchanged:
        long-display reverse (|a> + |b> . |c> + |d> . |e>)
            seq |0> => |b> + |a>
            seq |1> => |d> + |c>
            seq |2> => |e>
            |b> + |a> . |d> + |c> . |e>
      
        -- reverse both the superpositions and the sequence:
        long-display sreverse reverse (|a> + |b> . |c> + |d> . |e>)
            seq |0> => |e>
            seq |1> => |d> + |c>
            seq |2> => |b> + |a>
            |e> . |d> + |c> . |b> + |a>

    see also:
        sreverse
"""

# set invoke method:
built_in_table['coeff-sort'] = 'coeff_sort'
# set usage info:
built_in_table_usage['coeff-sort'] = """
    description:
        coeff-sort sp
        sort the given superposition by its coefficients

    examples:
        coeff-sort (6|f> + 5|e> + |a> + 2|b> + 4|d> + 3|c>)
            6|f> + 5|e> + 4|d> + 3|c> + 2|b> + |a>
        
        reverse coeff-sort (6|f> + 5|e> + |a> + 2|b> + 4|d> + 3|c>)
            |a> + 2|b> + 3|c> + 4|d> + 5|e> + 6|f>

    see also:
        ket-sort, shuffle, reverse
"""

# set invoke method:
built_in_table['ket-sort'] = 'ket_sort'
# set usage info:
built_in_table_usage['ket-sort'] = """
    description:
        ket-sort sp
        natural sort the given superposition by its ket labels

    examples:
        the-list-of |cities> => |Brisbane> + |Perth> + |Darwin> + |Hobart> + |Sydney> + |Melbourne> + |Adelaide>
        ket-sort the-list-of |cities>
            |Adelaide> + |Brisbane> + |Darwin> + |Hobart> + |Melbourne> + |Perth> + |Sydney>

    see also:
        coeff-sort, shuffle, reverse
"""

# set invoke method:
built_in_table['shuffle'] = 'shuffle'
# set usage info:
built_in_table_usage['shuffle'] = """
    description:
        shuffle sp
        shuffle the given superposition

    examples:
        shuffle rank split |a b c d e f>
            3|c> + 5|e> + 4|d> + 2|b> + 6|f> + |a>

    see also:
        ket-sort, coeff-sort
"""

# set invoke method:
compound_table['absolute-noise'] = ['absolute_noise', '', '']
# set usage info:
built_in_table_usage['absolute-noise'] = """
    description:
        absolute-noise[t] sp
        add noise to each ket in the superposition in range [0, t]

    examples:
        absolute-noise[100] split |a b c d e f>
            68.97|a> + 99.854|b> + 28.219|c> + 76.727|d> + 53.644|e> + 12.271|f>

        bar-chart[50] absolute-noise[100] split |a b c d e f>
            ----------
            a : ||||||||||||||||||||||
            b : ||||||||||||||||||||||||||||||||||||||||||||||
            c : ||||||||||||||||
            d : ||||||||||||||||||||||||||||||||||||||||||||||||||
            e : |||||||||||||||||||||||||||||||||||||||||||||||||
            f : ||||||||||||||||||||||||||||||||||||
            ----------
        
    see also:
        relative-noise
"""

# set invoke method:
compound_table['relative-noise'] = ['relative_noise', '', '']
# set usage info:
built_in_table_usage['relative-noise'] = """
    description:
        relative-noise[t] sp
        add noise to each ket in the superposition in range [0, t*max_coeff]

    examples:
        relative-noise[100] split |a b c d e f>
            87.604|a> + 28.21|b> + 7.666|c> + 45.833|d> + 52.395|e> + 58.717|f>

        bar-chart[50] relative-noise[100] split |a b c d e f>
            ----------
            a : |||||||
            b : ||||||||||||||||||||||
            c : ||||||||||||||||
            d : ||||||||||||||||||||||
            e : |||||||||||||||||||||||||||||||||||
            f : ||||||||||||||||||||||||||||||||||||||||||||||||||
            ----------

    see also:
        absolute-noise
"""


# set invoke method:
compound_table['select'] = ['select_range', '', '']
# set usage info:
built_in_table_usage['select'] = """
    description:
        select[k1, k2] sp
        select the k1'th to the k2'th elements from the given superposition
        indices start from 1, not 0

    examples:
        select[2,2] split |a b c d e f g h>
            |b>
        
        select[4,7] split |a b c d e f g h>
            |d> + |e> + |f> + |g>
            
    see also:
        sselect
"""

# set invoke method:
compound_table['sselect'] = ['sselect_range', '', '']
# set usage info:
built_in_table_usage['sselect'] = """
    description:
        sselect[k1, k2] seq
        select the k1'th to the k2'th elements from the given sequence
        indices start from 1, not 0

    examples:
        sselect[2,2] ssplit |abcdefgh>
            |b>

        sselect[2,3] (|a> + |b> . |c> + |d> . |e> . |f> + |g> + |h> . |i> + |j>)
            |c> + |d> . |e>

        sselect[4,7] ssplit[" "] |a b c d e f g h>
            |d> . |e> . |f> . |g>   

    see also:
        sselect
"""

# set invoke method:
compound_table['top'] = ['top', '', '']
# set usage info:
built_in_table_usage['top'] = """
    description:
        top[k] sp
        return the top k elements from the given sp
        indices start from 1, not 0
        if several elements all have the same coeff, then return all of them

    examples:
        top[3] rank split |a b c d e f g h>
            6|f> + 7|g> + 8|h>

    see also:
        select, sselect
"""

# set invoke method:
built_in_table['do-you-know'] = 'is_not_empty'
# set usage info:
built_in_table_usage['do-you-know'] = """
    description:
        do-you-know seq
        if seq is one of these: 
            don't know ket |>
            empty superposition
            empty sequence
        return |no>
        else, return |yes>

    examples:
        do-you-know |>
            |no>
        
        do-you-know |x>
            |yes>
        
        age |Fred> => |27>
        do-you-know age |Fred>
            |yes>
        
        do-you-know age |Sam>
            |no>
            
    see also:

"""

# set invoke method:
built_in_table['how-many'] = 'number_count'
# set usage info:
built_in_table_usage['how-many'] = """
    description:
        how-many sp
        returns the number of kets in a superposition

    examples:
        how-many |>
            |number: 0>
                    
        how-many split |a b c d e f g>
            |number: 7>
        
        -- learn some knowledge:
        friends |Fred> => |Jack> + |Harry> + |Ed> + |Mary> + |Rob> + |Patrick> + |Emma> + |Charlie>
        friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Rober> + |Frank> + |Julie>

        -- ask how many friends:
        how-many friends |Fred>
            |number: 8>
        
        how-many friends |Sam>
            |number: 7>

    see also:
        show-many, measure-currency
"""

# set invoke method:
built_in_table['show-many'] = 'snumber_count'
# set usage info:
built_in_table_usage['show-many'] = """
    description:
        show-many sp
        returns the number of superpositions in a sequence

    examples:
        show-many |>
            |number: 0>

        show-many ssplit[" "] |a b c d e f g>
            |number: 7>

        show-many (|a> . |b> + |c> + |d> . |e> + |f>)
            |number: 3>

    see also:
        how-many, measure-currency
"""

# set invoke method:
built_in_table['measure-currency'] = 'number_count_sum'
# set usage info:
built_in_table_usage['measure-currency'] = """
    description:
        measure-currency sp
        returns the sum of the coeffs in the given superposition
        in other words, the amount of currency used by that superposition
        
        eg, for a currency preserving operator, op, we have:
            measure-currency sp == measure-currency op sp
        for any superposition sp

    examples:
        measure-currency |>
            |number: 0>

        measure-currency split |a b c d e f g>
            |number: 7>

        measure-currency normalize split |a b c d e f g>
            |number: 1.0>

        measure-currency normalize[10] split |a b c d e f g>
            |number: 10>
                    
        measure-currency (0|a> + 2|b> + 3|c> + 5|d> + 7|e> + 11|f>)
            |number: 28>

    see also:
        how-many, show-many, normalize, rescale, smeasure-currency
"""

# set invoke method:
built_in_table['smeasure-currency'] = 'snumber_count_sum'
# set usage info:
built_in_table_usage['smeasure-currency'] = """
    description:
        smeasure-currency seq
        returns the sum of all the coeffs in the given sequence
        in other words, the amount of currency used by that sequence
        probably less useful than measure-currency

        eg, for a currency preserving operator, op, we have:
            measure-currency seq == measure-currency op seq
        for any sequence seq

    examples:
        smeasure-currency |>
            |number: 0>

        smeasure-currency ssplit[" "] |a b c d e f g>
            |number: 7>        

    see also:
        how-many, show-many, normalize, rescale, measure-currency
"""


# let's build the sigmoid_table_usage dictionary:
# set invoke method:
sigmoid_table['clean'] = 'clean'
# set usage info:
sigmoid_table_usage['clean'] = """
    description:
        clean ket
        clean the coefficients of the given superposition
        if x < 0, return 0
        else return 1

    examples:
        clean (3|a> + 2.2|b> - 3 |c> + |d>)
            |a> + |b> + 0|c> + |d>
    
    see also:
        set-to
"""

# set invoke method:
compound_table['threshold-filter'] = ['apply_sigmoid', 'threshold_filter', '']
# set usage info:
sigmoid_table_usage['threshold-filter'] = """
    description:
        threshold-filter[t] ket
        if x < t, return 0
        else return x

    examples:
        threshold-filter[2] (3|a> + 2.2|b> - 3 |c> + |d>)
            3|a> + 2.2|b> + 0|c> + 0|d>
    
    see also:
        not-threshold-filter
"""

# set invoke method:
compound_table['not-threshold-filter'] = ['apply_sigmoid', 'not_threshold_filter', '']
# set usage info:
sigmoid_table_usage['not-threshold-filter'] = """
    description:
        not-threshold-filter[t] ket
        if x <= t, return x
        else return 0

    examples:
        not-threshold-filter[2] (3|a> + 2.2|b> - 3 |c> + |d>)
            0|a> + 0|b> - 3|c> + |d>
    
    see also:
        threshold-filter
"""

# set invoke method:
sigmoid_table['binary-filter'] = 'binary_filter'
# set usage info:
sigmoid_table_usage['binary-filter'] = """
    description:
        binary-filter ket
        if x <= 0.96, return 0
        else return 1

    examples:
        binary-filter (2|a> + 0.9|b> -2|c>)
            |a> + 0|b> + 0|c>
            
    see also:
        not-binary-filter
"""

# set invoke method:
sigmoid_table['not-binary-filter'] = 'not_binary_filter'
# set usage info:
sigmoid_table_usage['not-binary-filter'] = """
    description:
        not-binary-filter ket
        if x <= 0.96, return 1
        else return 0

    examples:
        not-binary-filter (2|a> + 0.9|b> -2|c>)
            0|a> + |b> + |c>
        
    see also:
        binary-filter
"""

# set invoke method:
sigmoid_table['pos'] = 'pos'
# set usage info:
sigmoid_table_usage['pos'] = """
    description:
        pos ket
        positive filter
        if x <= 0, return 0
        else return x

    examples:
        pos (2|a> + 0.9|b> -2|c>)
            2|a> + 0.9|b> + 0|c>
    
    see also:
        abs
"""

# set invoke method:
sigmoid_table['abs'] = 'sigmoid_abs'
# set usage info:
sigmoid_table_usage['abs'] = """
    description:
        abs ket
        absolute value

    examples:
        abs (2|a> + 0.9|b> -3|c>)
            2|a> + 0.9|b> + 3|c>
    
    see also:
    
"""

# set invoke method:
compound_table['max-filter'] = ['apply_sigmoid', 'max_filter', '']
# set usage info:
sigmoid_table_usage['max-filter'] = """
    description:
        max-filter[t] ket
        if x <= t, return x
        else return t

    examples:
        max-filter[3] (|a> + 2|b> + 3|c> + 4|d> + 5|e>)
            |a> + 2|b> + 3|c> + 3|d> + 3|e>
            
    see also:

"""

# set invoke method:
sigmoid_table['NOT'] = 'NOT'
# set usage info:
sigmoid_table_usage['NOT'] = """
    description:
        NOT ket
        binary not
        if x <= 0.04, return 1
        else return 0

    examples:
        NOT (-1|a> + |b> + 2|c>)
            |a> + 0|b> + 0|c>

    see also:
    
"""

# set invoke method:
sigmoid_table['xor-filter'] = 'xor_filter'
# set usage info:
sigmoid_table_usage['xor-filter'] = """
    description:
        xor-filter ket
        xor
        if 0.96 <= x <= 1.04, return 1
        else return 0

    examples:
        xor-filter (0|a> + 0.98|b> + |c> + 1.02|d> + 2|e>)
            0|a> + |b> + |c> + |d> + 0|e>
        
    see also:
    
"""

# set invoke method:
compound_table['sigmoid-in-range'] = ['apply_sigmoid', 'sigmoid_in_range', '']
# set usage info:
sigmoid_table_usage['sigmoid-in-range'] = """
    description:
        sigmoid-in-range[a,b] ket
        the in-range sigmoid
        if a <= x <= b, return x
        else return 0

    examples:
        sigmoid-in-range[2,4] (|a> + 2|b> + 3|c> + 4|d> + 5|e>)
            0|a> + 2|b> + 3|c> + 4|d> + 0|e>

    see also:

"""

# set invoke method:
sigmoid_table['invert'] = 'invert'
# set usage info:
sigmoid_table_usage['invert'] = """
    description:
        invert ket
        multiplicative invert
        if x == 0, return 0
        else return 1/x

    examples:
        invert (0|x> + 3|y> - 0.5 |z>)
            0|x> + 0.333|y> - 2|z>
    
    see also:
    
"""

# set invoke method:
compound_table['set-to'] = ['apply_sigmoid', 'set_to', '']
# set usage info:
sigmoid_table_usage['set-to'] = """
    description:
        set-to[t] ket
        set all coefficients to t
        return t

    examples:
        set-to[7] (0|x> + 3|y> - 0.5|z>)
            7|x> + 7|y> + 7|z>

    see also:
    
"""

# set invoke method:
compound_table['subtraction-invert'] = ['apply_sigmoid', 'subtraction_invert', '']
# set usage info:
sigmoid_table_usage['subtraction-invert'] = """
    description:
        subtraction-invert[t] ket
        additive invert
        return t - x

    examples:
        subtraction-invert[0] (0|x> + 3|y> - 0.5|z>)
            0|x> - 3|y> + 0.5|z>

        subtraction-invert[2] (0|x> + 3|y> - 0.5|z>)
            2|x> - |y> + 2.5|z>

    see also:
    
"""

# set invoke method:
sigmoid_table['log'] = 'log'
compound_table['log'] = ['apply_sigmoid', 'log', '']
# set usage info:
sigmoid_table_usage['log'] = """
    description:
        log ket
        log[t] ket
        logarithm of x
        if x <= 0, return 0
        if t is None, return math.log(x)  (ie, base e)
        else, return math.log(x, t)       (ie, base t)

    examples:
        log 2.71828|e>
            1.0|e>

        log[10] 100000 |x>
            5|x>
    
    see also:
    
"""

# set invoke method:
sigmoid_table['log+1'] = 'log_1'
compound_table['log+1'] = ['apply_sigmoid', 'log_1', '']
# set usage info:
sigmoid_table_usage['log+1'] = """
    description:
        log+1 ket
        log+1[t] ket
        logarithm of 1 + x
        if x <= 0, return 0
        if t is None, return math.log(1 + x)  (ie, base e)
        else, return math.log(1 + x, t)       (ie, base t)

    examples:
        log+1 0|a>
            0|a>
        
    see also:
    
"""

# set invoke method:
sigmoid_table['square'] = 'square'
# set usage info:
sigmoid_table_usage['square'] = """
    description:
        square ket
        square the coefficients
        return x^2

    examples:
        square (0.2|x> + 3|y> - 5|z>)
            0.04|x> + 9|y> + 25|z>
    
    see also:
        sqrt
"""

# set invoke method:
sigmoid_table['sqrt'] = 'sqrt'
# set usage info:
sigmoid_table_usage['sqrt'] = """
    description:
        sqrt ket
        square root the coefficients
        return x^(1/2)

    examples:
        sqrt (9|x> + 25|y> + 49|z>)
            3|x> + 5|y> + 7|z>

        sqrt square (0.2|x> + 3|y> - 5|z>)
            0.2|x> + 3|y> + 5|z>
    
    see also:
        square, abs
"""

# set invoke method:
sigmoid_table['floor'] = 'floor'
# set usage info:
sigmoid_table_usage['floor'] = """
    description:
        floor ket
        return math.floor(x)

    examples:
        floor (2.3|x> + 7.9|y>)
            2|x> + 7|y>
    
    see also:
        ceiling
"""

# set invoke method:
sigmoid_table['ceiling'] = 'ceiling'
# set usage info:
sigmoid_table_usage['ceiling'] = """
    description:
        ceiling ket
        return math.ceil(x)

    examples:
        ceiling (2.3|x> + 7.9|y>)
            3|x> + 8|y>
    
    see also:
        floor
"""

# set invoke method:
sigmoid_table['increment'] = 'increment'
# set usage info:
sigmoid_table_usage['increment'] = """
    description:
        increment ket
        increment the coefficient by one
        return x + 1

    examples:
        increment |x>
            2|x>

        increment^7 0|x>
            7|x>
    
    see also:
        decrement
"""

# set invoke method:
sigmoid_table['decrement'] = 'decrement'
# set usage info:
sigmoid_table_usage['decrement'] = """
    description:
        decrement ket
        decrement the coefficient by one
        return x - 1

    examples:
        decrement |x>
            0|x>

        decrement^10 0|x>
            - 10|x>
    
    see also:
        increment
"""




# some worked examples:
examples_usage['numbers-to-words'] = """
    description:
        convert integers into English words
      
    code:
        ones |0> #=> |>
        ones |1> => |one>
        ones |2> => |two>
        ones |3> => |three>
        ones |4> => |four>
        ones |5> => |five>
        ones |6> => |six>
        ones |7> => |seven>
        ones |8> => |eight>
        ones |9> => |nine>

        tens |10> => |ten>
        tens |11> => |eleven>
        tens |12> => |twelve>
        tens |13> => |thirteen>
        tens |14> => |fourteen>
        tens |15> => |fifteen>
        tens |16> => |sixteen>
        tens |17> => |seventeen>
        tens |18> => |eighteen>
        tens |19> => |nineteen>

        ten |20> => |twenty>
        ten |30> => |thirty>
        ten |40> => |forty>
        ten |50> => |fifty>
        ten |60> => |sixty>
        ten |70> => |seventy>
        ten |80> => |eighty>
        ten |90> => |ninety>

        tens |*> #=> smerge[" "] sdrop ( ten times-by[10] int-divide-by[10] |_self> . ones mod[10] |_self> )
        hundreds-rule |*> #=> smerge[" and "] (hundreds int-divide-by[100] mod[1000] |_self> . tens mod[100] |_self>)
        thousands-rule |*> #=> thousands int-divide-by[1000] mod[1000000] |_self>
        millions-rule |*> #=> millions int-divide-by[1000000] mod[1000000000] |_self>

        hundreds |0> #=> |>
        hundreds |*> #=> ones |_self> __ |hundred>

        thousands |0> #=> |>
        thousands |*> #=> hundreds-rule |_self> __ |thousand>

        millions |0> #=> |>
        millions |*> #=> hundreds-rule |_self> __ |million>

        n2w |0> => |zero>
        n2w |*> #=> smerge[", "] sdrop (millions-rule |_self> . thousands-rule |_self> . hundreds-rule |_self>)

    examples:
        n2w |0>
            |zero>

        n2w |3>
            |three>

        n2w |15>
            |fifteen>

        n2w |53>
            |fifty three>

        n2w |735>
            |seven hundred and thirty five>

        n2w |12000>
            |twelve thousand>

        n2w |12500>
            |twelve thousand, five hundred>

        n2w |987654321>
            |nine hundred and eighty seven million, six hundred and fifty four thousand, three hundred and twenty one>

        -- or all at once:
        table[number, n2w] split |0 3 15 53 735 12000 987654321>
            +-----------+----------------------------------------------------------------------------------------------------------+
            | number    | n2w                                                                                                      |
            +-----------+----------------------------------------------------------------------------------------------------------+
            | 0         | zero                                                                                                     |
            | 3         | three                                                                                                    |
            | 15        | fifteen                                                                                                  |
            | 53        | fifty three                                                                                              |
            | 735       | seven hundred and thirty five                                                                            |
            | 12000     | twelve thousand                                                                                          |
            | 987654321 | nine hundred and eighty seven million, six hundred and fifty four thousand, three hundred and twenty one |
            +-----------+----------------------------------------------------------------------------------------------------------+

    source code:
        load numbers-to-words.sw
      
    see also:
        big-numbers-to-words
"""

examples_usage['big-numbers-to-words'] = """
    description:
        convert integers into English words

    code:
        ones |1> => |one>
        ones |2> => |two>
        ones |3> => |three>
        ones |4> => |four>
        ones |5> => |five>
        ones |6> => |six>
        ones |7> => |seven>
        ones |8> => |eight>
        ones |9> => |nine>

        tens |10> => |ten>
        tens |11> => |eleven>
        tens |12> => |twelve>
        tens |13> => |thirteen>
        tens |14> => |fourteen>
        tens |15> => |fifteen>
        tens |16> => |sixteen>
        tens |17> => |seventeen>
        tens |18> => |eighteen>
        tens |19> => |nineteen>

        ten |20> => |twenty>
        ten |30> => |thirty>
        ten |40> => |forty>
        ten |50> => |fifty>
        ten |60> => |sixty>
        ten |70> => |seventy>
        ten |80> => |eighty>
        ten |90> => |ninety>

        tens |*> #=> smerge[" "] sdrop ( ten times-by[10] int-divide-by[10] |_self> . ones mod[10] |_self> )
        hundreds-rule |*> #=> smerge[" and "] (hundreds int-divide-by[100] mod[1000] |_self> . tens mod[100] |_self>)

        hundreds |0> #=> |>
        hundreds |*> #=> ones |_self> __ |hundred>

        thousands |0> #=> |>
        thousands |*> #=> hundreds-rule |_self> __ |thousand>

        millions |0> #=> |>
        millions |*> #=> hundreds-rule |_self> __ |million>

        billions |0> #=> |>
        billions |*> #=> hundreds-rule |_self> __ |billion>

        trillions |0> #=> |>
        trillions |*> #=> hundreds-rule |_self> __ |trillion>

        op |seq> => |op: hundreds-rule> . |op: thousands> . |op: millions> . |op: billions> . |op: trillions>

        n2w |0> => |zero>
        n2w |*> #=> smerge[", "] sreverse op-zip(op |seq>, split-num |_self>)

        split-num |*> #=> process-if if(is-less-than[1000] |_self>, |less than 1000:> __ |_self>, |greater than 1000:> __ |_self>)
        process-if |less than 1000: *> #=> remove-leading-category |_self>
        process-if |greater than 1000: *> #=> mod[1000] remove-leading-category |_self> . split-num int-divide-by[1000] remove-leading-category |_self>

    examples:
        n2w |123456789012345>
            |one hundred and twenty three trillion, four hundred and fifty six billion, seven hundred and eighty nine million, twelve thousand, three hundred and forty five>

    source code:
        load big-numbers-to-words.sw
      
    see also:
        numbers-to-words      
"""

examples_usage['bottles-of-beer'] = """
    description:
        sing the bottles of beer song

    code:
        n-1 |*> #=> arithmetic(|_self>, |->, |1>)

        bottles |0> => |no more bottles>
        bottles |1> => |1 bottle>
        bottles |*> #=> |_self> __ |bottles>

        first-line |*> #=> to-upper[1] bottles |_self> __ |of beer on the wall,> __ bottles |_self> __ |of beer.>

        second-line |*> #=> |Take one down and pass it around,> __ bottles n-1 |_self> __ |of beer on the wall.>
        second-line |0> #=> |Go to the store and buy some more,> __ bottles max |bottles> __ |of beer on the wall.>

        row |*> #=> first-line |_self> . second-line |_self> . |>

        max |bottles> => |10>
        sing |*> #=> smerge["\n"] row sp2seq reverse range(|0>, max |bottles>)

        -- alternate version:
        -- NB: tidy is purposely not defined, so 'sdrop tidy seq' returns |> for all sequences seq
        sing2 |*> #=> sdrop tidy print row sp2seq reverse range(|0>, max |bottles>)

    examples:
        max |bottles> => |4>
        sing
            |4 bottles of beer on the wall, 4 bottles of beer.
            Take one down and pass it around, 3 bottles of beer on the wall.
    
            3 bottles of beer on the wall, 3 bottles of beer.
            Take one down and pass it around, 2 bottles of beer on the wall.
    
            2 bottles of beer on the wall, 2 bottles of beer.
            Take one down and pass it around, 1 bottle of beer on the wall.
    
            1 bottle of beer on the wall, 1 bottle of beer.
            Take one down and pass it around, no more bottles of beer on the wall.
    
            No more bottles of beer on the wall, no more bottles of beer.
            Go to the store and buy some more, 4 bottles of beer on the wall.
            >

    source code:
        load bottles-of-beer.sw
    
    see also:
    
"""

examples_usage['eat-from-can'] = """
    description:
        use consume-reaction to open and then eat from a can
      
    code:
        current |state> => words-to-list |closed can and hungry>
        learn-state (*) #=> learn(|op: current>, |state>, |_self>)
        use |can opener> #=> learn-state consume-reaction(current |state>, |can opener> + |closed can>, |can opener> + |open can>)
        eat-from |can> #=> learn-state consume-reaction(current |state>, |open can> + |hungry>, |empty can> + |not hungry>)

    examples:
        -- start without a can-opener:
        current |state>
            |closed can> + |hungry>

        -- trying to use a can opener doesn't change our state, since we don't have one:
        use |can opener>
            |closed can> + |hungry>
        
        -- let's add a can opener:
        current |state> +=> |can opener>
      
        -- now we can open our can:
        use |can opener>
            |can opener> + |hungry> + |open can>

        -- now we can eat from the open can:
        eat-from |can>
            |can opener> + |empty can> + |not hungry>

    source code:
        load eat-from-can.sw
"""

examples_usage['greetings'] = """
    description:
        random greet a list of people      

    code:
        hello |*> #=> |Hello,> __ |_self> _ |!>
        hey |*> #=> |Hey Ho!> __ |_self> _ |.>
        wat-up |*> #=> |Wat up my homie!> __ |_self> __ |right?>
        greetings |*> #=> |Greetings fine Sir. I belive they call you> __ |_self> _ |.>
        howdy |*> #=> |Howdy partner!>
        good-morning |*> #=> |Good morning> __ |_self> _ |.>
        gday |*> #=> |G'day> __ |_self> _ |.>

        list-of |greetings> => |op: hello> + |op: hey> + |op: wat-up> + |op: greetings> + |op: howdy> + |op: good-morning> + |op: gday>
        greet (*) #=> apply(pick-elt list-of |greetings>, list-to-words |_self>)

        friends |Sam> => |Charlie> + |George> + |Emma> + |Jack> + |Robert> + |Frank> + |Julie>
        friends |Emma> => |Liz> + |Bob>

   examples:
        greet (|Sam> + |Jack>)
            |G'day Sam and Jack.>

        greet friends |Sam>
            |Hey Ho! Charlie, George, Emma, Jack, Robert, Frank and Julie.>

        greet friends |Emma>
            |Wat up my homie! Liz and Bob right?>

    source code:
        load greetings.sw
"""

examples_usage['fission-uranium'] = """
    description:
        another example of consume-reaction()
        this time a toy example of fissioning uranium 235

    code:
        -- would also be nice to have |MeV> in these rules too:
        fission-channel-1 |U: 235> => |Ba: 141> + |Kr: 92> + 3|n>
        fission-channel-2 |U: 235> => |Xe: 140> + |Sr: 94> + 2|n>
        fission-channel-3 |U: 235> => |La: 143> + |Br: 90> + 3|n>
        fission-channel-4 |U: 235> => |Cs: 137> + |Rb: 96> + 3|n>
        fission-channel-5 |U: 235> => |I: 131> + |Y: 89> + 16|n>

        -- a more realistic example would have probabilities, as coefficients, for each of the channels.
        list-of-fission-channels |U: 235> => |op: fission-channel-1> + |op: fission-channel-2> + |op: fission-channel-3> + |op: fission-channel-4> + |op: fission-channel-5>

        fission |*> #=> apply(weighted-pick-elt list-of-fission-channels |_self>, |_self>)

        fission-uranium-235 (*) #=> consume-reaction(|_self>, |n> + |U: 235>, fission |U: 235>)

    examples:
        fission |U: 235>
            |Xe: 140> + |Sr: 94> + 2|n>

        fission |U: 235>
            |La: 143> + |Br: 90> + 3|n>

        fission |U: 235>
            |I: 131> + |Y: 89> + 16|n>

        fission-uranium-235 (|n> + 10|U: 235>)
            9|U: 235> + |Cs: 137> + |Rb: 96> + 3|n>

        fission-uranium-235^50 (|n> + 100|U: 235>)
            50|U: 235> + 12|Ba: 141> + 12|Kr: 92> + 237|n> + 11|I: 131> + 11|Y: 89> + 7|Xe: 140> + 7|Sr: 94> + 12|La: 143> + 12|Br: 90> + 8|Cs: 137> + 8|Rb: 96>

    source code:
        load fission-uranium.sw
"""

examples_usage['simple-adjective-sentence'] = """
    description:
        proof of concept of writing sentences
        in this case a simple adjective sentence
        obviously, the plan is to scale this up massively
        also, the plan is to eventually auto-learn adjectives from reading text
        but that is a ways off!!

    code:
        current |person> => |old man>
        learn-person |*> #=> learn(|op: current>, |person>, |_self>)

        adjectives |old man> => 10|crotchety> + 8|grumpy> + 5|friendly> + |kindly> + 0.2|sleepy>
        comma |old man> => |,>
      
        adjectives |old woman> => 2|kindly> + |sleepy> + |pleasant> + |strange>
        comma |old woman> => |,>
      
        adjectives |teenager> => |enthusiastic> + |energetic>
        comma |teenager> #=> |>

        pick-adjective (*) #=> clean weighted-pick-elt adjectives |_self>
        how-many-adjectives |*> #=> clean weighted-pick-elt (8|0> + 2|1> + 0.5|2> + 0.2|3>)


        insert-adjective |*> #=> |>
        insert-adjective |1> #=> ( pick-adjective _ comma ) current |person>
        insert-adjective |2> #=> ( pick-adjective . pick-adjective _ comma ) current |person>
        insert-adjective |3> #=> ( pick-adjective . pick-adjective . pick-adjective _ comma ) current |person>

        adjective-list |*> #=> smerge[", "] insert-adjective how-many-adjectives learn-person |_self>

        the-sentence |*> #=> smerge[" "] sdrop (|The> . adjective-list |_self> . |_self> _ |.>)
        sentence |*> #=> the-sentence pick-elt (|old man> + |old woman> + |teenager>)

    examples:
        sentence
            |The kindly, old man.>

        sentence
            |The old woman.>

        sentence
            |The teenager.>

        sentence
            |The strange, kindly, old woman.>

        sentence
            |The energetic teenager.>

    source code:
        load the-old-man.sw
"""

examples_usage['random-sentence'] = """
    description:
        learn some sentence fragments, and then produce a valid sentence
        motivated by this: http://write-up.semantic-db.org/221-generating-random-grammatically-correct-sentences.html

        in gm notation:
            A = {the.woman.saw}
            B = {through.the.telescope}
            C = {{}, young}
            D = {girl, boy}
            E = {{}, old, other}
            F = {man, woman, lady}
            G = E.F
            H = {the}
            I = H.C.D
            J = H.E.F
            K = {{},I,J}
    
            L = A.K.B
    
            M = {I,J}
            N = {saw}
            O = M.N.K.B
    
            P = {through.the}
            Q = {telescope, binoculars, night.vision.goggles}
    
            R = M.N.K.P.Q

    code:
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

    examples:
        sentence
            |The other lady saw the old woman through the telescope.>

        sentence
            |The young boy saw the young girl through the binoculars.>

        sentence
            |The old woman saw the other man through the telescope.>

        sentence
            |The young boy saw the young girl through the night vision goggles.>

    future:
        scale it up, and maybe write a gm-to-code converter?

    source code:
        load the-woman-saw.sw
"""

examples_usage['active-logic'] = """
    description:
        proof of concept using simple if-then machines
        in this case, concerning wet grass, the sprinkler and rain

    code:
        -- learn the meaning of not:
        not |no> => |yes>
        not |yes> => |no>
        not |don't know> => |don't know>

        -- define our if-then machines:
        pattern |node 1: 1> => |grass is wet> + |not rained last night>
        then |node 1: 1> => 2.0|sprinkler was on> + -1.0|rained last night> + -1.0|not grass is wet>

        pattern |node 2: 1> => |grass is wet> + |not sprinkler was on>
        then |node 2: 1> => 2.0|rained last night> + -1.0|sprinkler was on> + -1.0|not grass is wet>

        pattern |node 3: 1> => |sprinkler was on>
        then |node 3: 1> => |grass is wet> + -1.0|not sprinkler was on>

        pattern |node 3: 2> => |rained last night>
        then |node 3: 2> => |grass is wet> + -1.0|not rained last night>

        pattern |node 4: 1> => |not rained last night> + |not sprinkler was on>
        then |node 4: 1> => 2.0|not grass is wet> + -1.0|rained last night> + -1.0|sprinkler was on>


        -- learn state of activation:
        active |rained last night> => |don't know>
        active |not rained last night> #=> not active |rained last night>
        active |sprinkler was on> => |don't know>
        active |not sprinkler was on> #=> not active |sprinkler was on>
        active |grass is wet> => |don't know>
        active |not grass is wet> #=> not active |grass is wet>


        -- activation states we want to unlearn:
        the-unlearn |list> => |rained last night> + |sprinkler was on> + |grass is wet>


        -- unlearn operators:
        unlearn |*> #=> learn(|op: active>, |_self>, |don't know>)
        unlearn-everything |*> #=> unlearn the-unlearn |list>


        -- our 'active' operators:
        make-active |*> #=> learn(|op: active>, remove-prefix["not "] |_self>, not has-prefix["not "] |_self>)
        currently-active |*> #=> such-that[active] rel-kets[active] |>
        read-sentence |*> #=> make-active words-to-list |_self>


        -- define our conclude operators:
        conclude |*> #=> drop then similar-input[pattern] such-that[active] rel-kets[active] |>
        inverse-conclude |*> #=> pattern similar-input[then] such-that[active] rel-kets[active] |>


        -- define short-cuts for our tables:
        t |*> #=> table[state, unlearn-everything, read-sentence, currently-active, conclude, inverse-conclude] the-list-of |states>
        t2 |*> #=> table[state, unlearn-everything, read-sentence, currently-active, conclude] the-list-of |states>


        -- learn the list of states we want in our tables:
        the-list-of |states> => |grass is wet>
        the-list-of |states> +=> |sprinkler was on>
        the-list-of |states> +=> |rained last night>
        the-list-of |states> +=> |sprinkler was on and rained last night>
        the-list-of |states> +=> |grass is wet and not rained last night>
        the-list-of |states> +=> |grass is wet and not sprinkler was on>
        the-list-of |states> +=> |not rained last night>
        the-list-of |states> +=> |not sprinkler was on>
        the-list-of |states> +=> |not rained last night and not sprinkler was on>
        the-list-of |states> +=> |not grass is wet>

    examples:
        unlearn-everything
            3|don't know>

        read-sentence |grass is wet and not rained last night>
            |yes> + |no>

        currently-active
            |not rained last night> + |grass is wet>

        conclude
            |sprinkler was on>


        t2
            +------------------------------------------------+--------------------+---------------+---------------------------------------------+-----------------------------------------------+
            | state                                          | unlearn-everything | read-sentence | currently-active                            | conclude                                      |
            +------------------------------------------------+--------------------+---------------+---------------------------------------------+-----------------------------------------------+
            | grass is wet                                   | 3 don't know       | yes           | grass is wet                                | 0.50 sprinkler was on, 0.50 rained last night |
            | sprinkler was on                               | 3 don't know       | yes           | sprinkler was on                            | grass is wet                                  |
            | rained last night                              | 3 don't know       | yes           | rained last night                           | grass is wet                                  |
            | sprinkler was on and rained last night         | 3 don't know       | 2 yes         | rained last night, sprinkler was on         | grass is wet                                  |
            | grass is wet and not rained last night         | 3 don't know       | yes, no       | not rained last night, grass is wet         | sprinkler was on                              |
            | grass is wet and not sprinkler was on          | 3 don't know       | yes, no       | not sprinkler was on, grass is wet          | rained last night                             |
            | not rained last night                          | 3 don't know       | no            | not rained last night                       | 0.50 sprinkler was on, 0.50 not grass is wet  |
            | not sprinkler was on                           | 3 don't know       | no            | not sprinkler was on                        | 0.50 rained last night, 0.50 not grass is wet |
            | not rained last night and not sprinkler was on | 3 don't know       | 2 no          | not rained last night, not sprinkler was on | not grass is wet                              |
            | not grass is wet                               | 3 don't know       | no            | not grass is wet                            |                                               |
            +------------------------------------------------+--------------------+---------------+---------------------------------------------+-----------------------------------------------+

    source code:
        load improved-active-logic.sw
"""

examples_usage['temperature-conversions'] = """
    description:
        converting between Fahrenheit, Celsius and Kelvin

    code:
        to-Kelvin |K: *> #=> |_self>
        to-Celsius |K: *> #=> |C:> __ round[2] minus[273.15] extract-value |_self>
        to-Fahrenheit |K: *> #=> |F:> __ round[2] minus[459.67] times-by[9/5] extract-value |_self>

        to-Kelvin |C: *> #=> |K:> __ round[2] plus[273.15] extract-value |_self>
        to-Celsius |C: *> #=> |_self>
        to-Fahrenheit |C: *> #=> |F:> __ round[2] plus[32] times-by[9/5] extract-value |_self>

        to-Kelvin |F: *> #=> |K:> __ round[2] times-by[5/9] plus[459.67] extract-value |_self>
        to-Celsius |F: *> #=> |C:> __ round[2] times-by[5/9] minus[32] extract-value |_self>
        to-Fahrenheit |F: *> #=> |_self>

        to-K |*> #=> to-Kelvin |_self>
        to-C |*> #=> to-Celsius |_self>
        to-F |*> #=> to-Fahrenheit |_self>

    examples:
        to-F |C: 42>
            |F: 107.6>

        to-C |F: 50>
            |C: 10>

        to-K |C: 0>
            |K: 273.15>

        to-F |C: 100>
            |F: 212>

    source code:
        load temperature-conversion.sw
      
    see also:
        load distance-conversion.sw
"""

examples_usage['Fibonacci-and-factorial'] = """
    description:
        simple recursive Fibonacci and factorial
        NB: we use !=> instead of #=>
        ie, memoizing rules instead of plain stored-rules.
        otherwise this code gets very slow, very fast.

    code:
        fib |0> => |0>
        fib |1> => |1>
        fib |*> !=> arithmetic( fib minus[1] |_self>, |+>, fib minus[2] |_self>)
        fib-ratio |*> !=> arithmetic( fib |_self> , |/>, fib minus[1] |_self> )

        fact |0> => |1>
        fact |*> !=> arithmetic(|_self>, |*>, fact minus[1] |_self>)

    examples:
        table[number, fib, fib-ratio, fact] range(|1>, |30>)
            +--------+--------+--------------------+-----------------------------------+
            | number | fib    | fib-ratio          | fact                              |
            +--------+--------+--------------------+-----------------------------------+
            | 1      | 1      |                    | 1                                 |
            | 2      | 1      | 1.0                | 2                                 |
            | 3      | 2      | 2.0                | 6                                 |
            | 4      | 3      | 1.5                | 24                                |
            | 5      | 5      | 1.6666666666666667 | 120                               |
            | 6      | 8      | 1.6                | 720                               |
            | 7      | 13     | 1.625              | 5040                              |
            | 8      | 21     | 1.6153846153846154 | 40320                             |
            | 9      | 34     | 1.619047619047619  | 362880                            |
            | 10     | 55     | 1.6176470588235294 | 3628800                           |
            | 11     | 89     | 1.6181818181818182 | 39916800                          |
            | 12     | 144    | 1.6179775280898876 | 479001600                         |
            | 13     | 233    | 1.6180555555555556 | 6227020800                        |
            | 14     | 377    | 1.6180257510729614 | 87178291200                       |
            | 15     | 610    | 1.6180371352785146 | 1307674368000                     |
            | 16     | 987    | 1.618032786885246  | 20922789888000                    |
            | 17     | 1597   | 1.618034447821682  | 355687428096000                   |
            | 18     | 2584   | 1.6180338134001253 | 6402373705728000                  |
            | 19     | 4181   | 1.618034055727554  | 121645100408832000                |
            | 20     | 6765   | 1.6180339631667064 | 2432902008176640000               |
            | 21     | 10946  | 1.6180339985218033 | 51090942171709440000              |
            | 22     | 17711  | 1.618033985017358  | 1124000727777607680000            |
            | 23     | 28657  | 1.6180339901755971 | 25852016738884976640000           |
            | 24     | 46368  | 1.618033988205325  | 620448401733239439360000          |
            | 25     | 75025  | 1.618033988957902  | 15511210043330985984000000        |
            | 26     | 121393 | 1.6180339886704431 | 403291461126605635584000000       |
            | 27     | 196418 | 1.6180339887802426 | 10888869450418352160768000000     |
            | 28     | 317811 | 1.618033988738303  | 304888344611713860501504000000    |
            | 29     | 514229 | 1.6180339887543225 | 8841761993739701954543616000000   |
            | 30     | 832040 | 1.6180339887482036 | 265252859812191058636308480000000 |
            +--------+--------+--------------------+-----------------------------------+
"""

examples_usage['walking-a-grid'] = """
    description:
        a fun little insect with minimal intelligence.
        with current settings it heads mostly in a south direction (but this is easy to change)
        when it thinks it has hit the edge of the map, it changes its heading by turning right
        the numbers are how many time-steps the insect has been on that location
        ### is the current location of our insect

    code:
        -- learn map:
        |null> => learn-map[30,30]

        -- learn current location:
        current |cell> => |grid: 1: 22>

        -- define turn-right operator:
        turn-right |op: S> => |op: W>
        turn-right |op: SW> => |op: NW>
        turn-right |op: W> => |op: N>
        turn-right |op: NW> => |op: NE>
        turn-right |op: N> => |op: E>
        turn-right |op: NE> => |op: SE>
        turn-right |op: E> => |op: S>
        turn-right |op: SE> => |op: SW>

        -- define walk direction:
        heading |ops> => 0.25|op: SW> + |op: S> + 0.25|op: SE>
        -- heading |ops> => |op: S>
        next |*> #=> set-to[1] apply(weighted-pick-elt heading |ops>, |_self>)

        -- define turn-heading-right operator:
        turn-heading-right |*> #=> learn(|op: heading>, |ops>, turn-right heading |ops>)

        -- define step operator:
        step |*> #=> process-if if(do-you-know next |_self>, |valid step:> __ |_self>, |not valid step:> __ |_self>)
        process-if |valid step: *> #=> next remove-leading-category |_self>
        process-if |not valid step: *> #=> sselect[1,1] (remove-leading-category |_self> . turn-heading-right |>)
        -- process-if |not valid step: *> #=> sdrop (remove-leading-category |_self> . set-to[0] turn-heading-right |>)

        -- update-map operators (increment current spot, take a step, and display map):
        inc |*> #=> learn(|op: value>, current |cell>, plus[1] value current |cell>)
        n |*> #=> learn(|op: current>, |cell>, step current |cell>)
        d |*> #=> display-map[30,30]


        -- single map update:
        line |*> #=> inc |_self> . n |_self> . d |_self>

        -- set max steps:
        max |steps> => |30>

        -- walk max steps:
        walk |*> #=> sdrop set-to[0] line sp2seq range(|1>, max |steps>)

    examples:
        -- load the code:
        load walk-grid-v2.sw

        -- switch off info printing. 
        -- this is important if you want a clean display of the maps
        info off

        -- walk the map:
        walk
        walk
        walk
            h: 30
            w: 30
            1     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            2     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            3     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
            4     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            5     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            6     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            7     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            8     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
            9     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
            10    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
            11    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
            12    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
            13    2  1  1  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
            14    .  1  .  1  1  1  .  1  1  1  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
            15    .  .  1  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .
            16    .  1  .  .  .  .  .  .  .  .  .  1  1  1  1  1  1###  .  .  .  .  1  .  .  .  .  .  .  .
            17    .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            18    .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            19    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            20    2  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            21    1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            22    1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            23    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
            24    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
            25    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
            26    .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .
            27    .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            28    .  .  1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .
            29    .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  1  .  .  .  .  1  .  .  .  .  .  .  .  .
            30    .  .  2  1  2  1  1  1  1  1  1  1  2  .  1  .  .  1  1  1  2  3  .  .  .  .  .  .  .  .


        walk^5
            h: 30
            w: 30
            1     .  .  .  .  .  .  3  2  2  3  .  .  .  .  .  .  .  .  2  1  1  2  1  1  .  3  1  1  1  2
            2     .  .  .  .  .  .  .  .  .  1  1  1  1  .  .  .  .  .  1  2  1  2  .  .  1  .  .  .  .  1
            3     .  .  .  .  .  .  .  .  .  .  1  .  .  1  1  1  1  1  .  1  .  1  1  1  1  .  1  .  .  1
            4     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  1  .  .  .  1  .  1  1  .
            5     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  1  2
            6     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .  .
            7     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .  .
            8     .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
            9     .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
            10    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
            11    .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
            12    .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
            13    .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .  .
            14    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .  .
            15    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .  .
            16    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  .  .  1  .  .  .  .  .  .
            17    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .
            18    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
            19    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .
            20    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .  .  .
            21    .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .
            22    .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  1  .  .  .  1  .  .  .  .  .  .
            23    .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  .  .  1  .  .  .  .  .
            24    .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  .  .  1  .  .  .  .  .
            25    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  .  1  .  .  .  .  .
            26    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  .  1  .  .  .  .  .
            27    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .  .
            28    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  1  .  .  1  .  .  .  .  .
            29    .  .  .  .  .  .  .  .  .  .  .  1  .  .  .  .  .  .  .  .  .  .  1  .  1  .  .  .  .  .
            30    .  .  .  .  .###  1  1  2  1  1  2  .  .  .  .  .  .  .  .  .  .  2  1  1  2  .  .  .  .

    source code:
        load walk-grid-v2.sw
"""

examples_usage['walking-ant'] = """
    description:
        a walking ant with minimal intelligence
        it is a much more complex version of 'walking-a-grid' and currently the most complex swc code yet written
        
        learn and randomly walk a grid
        keep a record of the pathway home
        if find food return home, leaving a scent trail
        once home, follow scent trail back to food (approximately)
        if find food again, return home, adding to the scent trail
        when reach home, store the food, switch off scent trail, and start randomly walking again

        ### is the current location of our ant

    code:
        -- learn map:
        |null> => learn-map[30, 30] |>
        
        -- learn current location:
        current |cell> => |grid: 10: 22>
        
        -- learn home location:
        home |cell> => current |cell>
        
        -- start with no food at home:
        stored-food home |cell> => 0| >
        
        -- learn path home:
        store-direction (*) #=>
            path |home> +=> |__self>
        
        -- find return path
        return-path |home> #=>
            invert-direction expand path |home>
        
        -- NB: |_self> works here, so don't need the slower |__self>
        invert-direction |*> #=>
            if(is-less-than[0] push-float |_self>, - |_self>, reverse-dir |_self> )
        
        
        -- learn the list of directions:
        list-of |directions> => |op: N> + |op: NE> + |op: E> + |op: SE> + |op: S> + |op: SW> + |op: W> + |op: NW>
        
        -- choose a heading when leaving the nest:
        heading |ops> => pick-elt list-of |directions>
        
        -- start by not carrying any food:
        carry |food> => 0| >
        
        -- start with scent trail off:
        lay |scent> => |no>
        
        -- start with random walk type:
        type |walk> => |op: random-walk>
        
        
        
        -- place some food:
        food |grid: 2: 2> => 3| >
        food |grid: 2: 3> => 3| >
        food |grid: 2: 4> => 3| >
        food |grid: 2: 5> => 3| >
        food |grid: 3: 5> => 3| >
        food |grid: 4: 5> => 3| >
        food |grid: 5: 6> => 3| >
        food |grid: 6: 6> => 3| >
        food |grid: 29: 29> => 20| >
        food |grid: 28: 3> => 20| >
        
        
        -- show food and stored-food operators:
        show-food |*> #=>
            display-map[30, 30, food] |>
        
        show-stored-food |*> #=>
            display-map[30, 30, stored-food] |>
        
        
        -- carry-the and drop-the food operators:
        -- currently assumes food current |cell> is greater than 0.
        carry-the |food> #=>
            food current |cell> => decrement food current |cell>
            carry |food> => increment carry |food>
        
        drop-the |food> #=>
            stored-food current |cell> +=> carry |food>
            carry |food> => 0| >
        
        
        -- if there is food at the current cell, and not already carrying food, then |found food>:
        if-find-food |*> #=>
            process-if if( and(is-greater-than[0] push-float food current |cell>, is-equal[0] push-float carry |food>), |found food>, |not found food> )
        
        process-if |found food> #=>
            -- carry the food:
            food current |cell> => decrement food current |cell>
            carry |food> => increment carry |food>
            lay |scent> => |yes>
            type |walk> => |op: return-home>
        
        process-if |not found food> #=>
            |>
        
        
        -- if reach home operator:
        -- ie, if current cell is home cell then |reached home>:
        if-reach-home |*> #=>
            process-if if(is-equal( current |cell>, home |cell>), |reached home>, |not reached home>)
        
        process-if |reached home> #=>
            -- drop and store any food you are carrying:
            stored-food current |cell> +=> carry |food>
            carry |food> => 0| >
            lay |scent> => |no>
            type |walk> => |op: random-walk>
            path |home> => |home>
        
        process-if |not reached home> #=>
            |>
        
        
        record-scent |*> #=>
            process-if if(lay |scent>, |yes to scent>, |no to scent>)
        
        process-if |yes to scent> #=>
            value current |cell> => plus[1] value current |cell>
        
        process-if |no to scent> #=>
            |>
        
        
        if-find-scent-change-heading |*> #=>
            process-if if(is-greater-than[0] value |_self>, |found scent> , |not found scent>)
        
        process-if |found scent> #=>
            heading |ops> => random-if-zero reverse-dir return-path |home>
        
        process-if |not found scent> #=>
            |>
        
        random-if-zero (*) #=>
            if(do-you-know sdrop |_self>, |_self>, pick-elt list-of |directions>)
        
        
        
        switch-on-random |*> #=>
            type |walk> => |op: random-walk>
        
        switch-on-return |*> #=>
            type |walk> => |op: return-home>
        
        
        take-a-step |*> #=>
            current |direction> => apply( type |walk>, current |cell>)
            path |home> +=> current |direction>
            current |cell> => apply( current |direction>, current |cell>)
            if-find-food |>
            if-reach-home |>
        
        
        
        -- random-walk input is a grid location:
        -- random-walk has to return a direction:
        random-walk |*> #=>
            if-find-scent-change-heading |__self>
        
            -- blur heading:
            heading |ops> => normalize ( 0.1 turn-left^2 + 0.25 turn-left + 15 + 0.25 turn-right + 0.1 turn-right^2 ) heading |ops>
        
            -- try a direction:
            try |direction> => clean weighted-pick-elt heading |ops>
        
            -- if valid direction, step, else turn right:
            process-if if(do-you-know apply( try |direction>, |__self>), |valid step>, |not valid step>)
        
        process-if |valid step> #=>
            try |direction>
        
        process-if |not valid step> #=>
            -- turn heading right:
            heading |ops> => pick-elt ( turn-right + turn-right^2 ) heading |ops>
            |op: id>
        
        
        -- define turn-heading-right operator:
        turn-heading-right |*> #=>
            heading |ops> => pick-elt ( turn-right + turn-right^2 ) heading |ops>
        
        -- define blur-heading operator:
        blur-heading |*> #=>
            heading |ops> => ( 0.1 turn-left^2 + 0.25 turn-left + 10 + 0.25 turn-right + 0.1 turn-right^2 ) heading |ops>
        
        
        -- return-home input is a grid location (which we ignore, instead making use of return-path |home>):
        -- return-home returns a direction one step closer to home:
        return-home |*> #=>
            clean weighted-pick-elt return-path |home>
        
        
        -- define identity direction operator:
        id |*> #=> |_self>
        
        -- define turn-right operators:
        turn-right |op: S> => |op: SW>
        turn-right |op: SW> => |op: W>
        turn-right |op: W> => |op: NW>
        turn-right |op: NW> => |op: N>
        turn-right |op: N> => |op: NE>
        turn-right |op: NE> => |op: E>
        turn-right |op: E> => |op: SE>
        turn-right |op: SE> => |op: S>
        
        -- define turn-left operators:
        turn-left |op: S> => |op: SE>
        turn-left |op: SW> => |op: S>
        turn-left |op: W> => |op: SW>
        turn-left |op: NW> => |op: W>
        turn-left |op: N> => |op: NW>
        turn-left |op: NE> => |op: N>
        turn-left |op: E> => |op: NE>
        turn-left |op: SE> => |op: E>
        
        -- define reverse operators:
        reverse-dir |op: S> => |op: N>
        reverse-dir |op: SW> => |op: NE>
        reverse-dir |op: W> => |op: E>
        reverse-dir |op: NW> => |op: SE>
        reverse-dir |op: N> => |op: S>
        reverse-dir |op: NE> => |op: SW>
        reverse-dir |op: E> => |op: W>
        reverse-dir |op: SE> => |op: NW>
        
        -- define expand operators:
        expand |op: S> => - |op: N>
        expand |op: SW> => - |op: N> - |op: E>
        expand |op: W> => - |op: E>
        expand |op: NW> => |op: N> - |op: E>
        expand |op: N> => |op: N>
        expand |op: NE> => |op: N> + |op: E>
        expand |op: E> => |op: E>
        expand |op: SE> => - |op: N> + |op: E>
        
        
        
        d |*> #=>
            display-map[30,30]
        
        -- single map update:
        update |*> #=>
            record-scent |>
            take-a-step |>
            d |>
            |>
        
        -- set max steps:
        max |steps> => |20>
        
        -- walk max steps:
        walk |*> #=>
            update range(|1>, max |steps>)


    examples:
        -- load the code:
        load walking-ant.swc
        
        -- show the starting locations of food:
        show-food
            h: 30
            w: 30
            1
            2        3  3  3  3
            3                 3
            4                 3
            5                    3
            6                    3
            7
            8
            9
            10                                                                 ###
            11
            12
            13
            14
            15
            16
            17
            18
            19
            20
            21
            22
            23
            24
            25
            26
            27
            28         20
            29                                                                                       20
            30
        
        -- walk a lot:
        walk^100
            h: 30
            w: 30
            1
            2        1  2  1  1  1  1  1  1
            3           1  1  4  3  2  1  2  2  1  1  1
            4                 3  2  3  3  3  3  2  2  1
            5                 2  3  2  2  2  3  1  3  3  2  1
            6                    2  1  2  2  3  1  2  3  4  3  2
            7                    1        1  3  3  3  2  3  3  4  3  2  1  1
            8                    1                 1  2  3  4  4  5  3  1  1
            9                    1  1  1  1  1              1  1  4  6  6  6  4  3
            10                               1  1  1  1  1  1  1  1  2  3  5  6
            11                                                 1  1  1  1  1  1  3
            12                                           1  1  1                 2
            13                                        1  1              1  1  2  2
            14                                        1                 1     1
            15                                        1        1  1  2  2  1  1
            16                                     1  1        1     1
            17                                     1           1     1
            18                                  1  1     1  1  1     1
            19                            1  1  1     2  2  1  1  1  1
            20                         1  1           2
            21  ###                    1        1  1  2
            22                         1        1     1
            23                         1     1  1     1
            24                         1  1  1     1  1
            25                   1  1  1  2  1  1  1
            26             1  1  2  2  2  2
            27          1  2  1  2  1
            28          3  2  1  1
            29
            30

        -- show remaining food:
            h: 30
            w: 30
            1
            2        2  2  3  3
            3
            4                 1
            5                    2
            6                    2
            7
            8
            9
            10
            11
            12
            13
            14
            15
            16
            17
            18
            19
            20
            21  ###
            22
            23
            24
            25
            26
            27
            28         17
            29                                                                                       20
            30
        
        -- show stored food:
            h: 30
            w: 30
            1
            2
            3
            4
            5
            6
            7
            8
            9
            10                                                                  12
            11
            12
            13
            14
            15
            16
            17
            18
            19
            20
            21  ###
            22
            23
            24
            25
            26
            27
            28
            29
            30
        
    source code:
        load walking-ant.swc
    
    see also:
        walking-a-grid
"""


examples_usage['finding-a-path-between-early-us-presidents'] = """
    description:
        a fun little application of find-path-between applied to early US presidents

    code:
        see find-path-between usage information
      
    examples:      
        -- load the knowledge:
        load early-us-presidents.sw
      
        -- switch off info statements:
        info off
      
        -- learn some relevant inverses:
        find-inverse[president-number, president-era, party, full-name]

        -- find the operator path between George Washington and John Adams:
        find-path-between(|person: George Washington>, |person: John Adams>)
            |op: inverse-full-name> . |op: president-era> . |op: inverse-president-era> . |op: full-name>
    
        -- now let's step through this operator sequence:
        inverse-full-name |person: George Washington>
            |Washington>
              
        president-era inverse-full-name |person: George Washington>
            |year: 1789> + |year: 1790> + |year: 1791> + |year: 1792> + |year: 1793> + |year: 1794> + |year: 1795> + |year: 1796> + |year: 1797>
      
        inverse-president-era president-era inverse-full-name |person: George Washington>
            9|Washington> + |Adams>
              
        full-name inverse-president-era president-era inverse-full-name |person: George Washington>
            9|person: George Washington> + |person: John Adams>      

      
      
        -- next example, find the operator path between George Washington and James Monroe:
        find-path-between(|person: George Washington>, |person: James Monroe>)
            |op: inverse-full-name> . |op: president-era> . |op: inverse-president-era> . |op: president-era> . |op: inverse-president-era> . |op: party> . |op: inverse-party> . |op: full-name>

        -- now let's step through this operator sequence:
        inverse-full-name |person: George Washington>
            |Washington>

        president-era inverse-full-name |person: George Washington>
            |year: 1789> + |year: 1790> + |year: 1791> + |year: 1792> + |year: 1793> + |year: 1794> + |year: 1795> + |year: 1796> + |year: 1797>

        inverse-president-era president-era inverse-full-name |person: George Washington>
            9|Washington> + |Adams>

        president-era inverse-president-era president-era inverse-full-name |person: George Washington>
            9|year: 1789> + 9|year: 1790> + 9|year: 1791> + 9|year: 1792> + 9|year: 1793> + 9|year: 1794> + 9|year: 1795> + 9|year: 1796> + 10|year: 1797> + |year: 1798> + |year: 1799> + |year: 1800> + |year: 1801>

        inverse-president-era president-era inverse-president-era president-era inverse-full-name |person: George Washington>
            82|Washington> + 14|Adams> + |Jefferson>

        party inverse-president-era president-era inverse-president-era president-era inverse-full-name |person: George Washington>
            82|party: Independent> + 14|party: Federalist> + |party: Democratic-Republican>

        inverse-party party inverse-president-era president-era inverse-president-era president-era inverse-full-name |person: George Washington>
            82|Washington> + 14|Adams> + |Jefferson> + |Madison> + |Monroe> + |Q Adams>

        full-name inverse-party party inverse-president-era president-era inverse-president-era president-era inverse-full-name |person: George Washington>
            82|person: George Washington> + 14|person: John Adams> + |person: Thomas Jefferson> + |person: James Madison> + |person: James Monroe> + |person: John Quincy Adams>


        -- next example, find the operator path between George Washington and number 6:
        find-path-between(|person: George Washington>, |number: 6>)
            |op: inverse-full-name> . |op: president-era> . |op: inverse-president-era> . |op: president-era> . |op: inverse-president-era> . |op: party> . |op: inverse-party> . |op: president-number>

        -- this is almost identical to the example above, so we only need to change the last step 'president-number':
        president-number inverse-party party inverse-president-era president-era inverse-president-era president-era inverse-full-name |person: George Washington>
            82|number: 1> + 14|number: 2> + |number: 3> + |number: 4> + |number: 5> + |number: 6>


    source code:
        load early-us-presidents.sw
    
    see also:
        find-path-between
"""