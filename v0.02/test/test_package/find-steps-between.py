#!c:/Python34/python.exe

#######################################################################
# find steps between two nodes
#
# Author: Garry Morrison
# email: garry -at- semantic-db.org
# Date: 24/3/2018
# Update: 24/3/2018
# Copyright: GPLv3
#
# Usage: ./find-steps-between.py sw-examples/new-imdb.sw
#
#######################################################################

from semantic_db.code import *

if len(sys.argv) < 2:
    print("\nUsage: ./find-steps-between.py source.sw")
    sys.exit(1)

if len(sys.argv) >= 2:
    source = sys.argv[1]

logger.setLevel(logging.WARNING)

intervals = (
    ('weeks', 604800000),  # 1000 * 60 * 60 * 24 * 7
    ('days', 86400000),  # 1000 * 60 * 60 * 24
    ('hours', 3600000),  # 1000 * 60 * 60
    ('minutes', 60000),  # 1000 * 60
    ('seconds', 1000),  # 1000
    ('milliseconds', 1),
)


def display_time(seconds):
    ms = int(1000 * seconds)
    result = []

    for name, count in intervals:
        value = ms // count
        if value:
            ms -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    if len(result) == 0:
        return "0"
    return ', '.join(result)


def load_simple_sw_file(context, source):
    with open(source, 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0 and not line.startswith('supported-ops') and not line.startswith('--') and not line.startswith('|context'):
                try:
                    head, tail = line.split('> => ')
                    # print('head: %s' % head)
                    # print('tail: %s' % tail)
                    op, label = head.split(' |')
                    rule = superposition()
                    for piece in tail[:-1].split('> + '):
                        float_piece, string_piece = piece.split('|')
                        try:
                            float_piece = float(float_piece)
                        except:
                            float_piece = 1
                        rule.add(string_piece, float_piece)
                    # print('op: %s' % op)
                    # print('label: %s' % label)
                    # print('rule: %s' % str(rule))
                    context.learn(op, label, rule)
                except Exception as e:
                    print('Exception reason: %s' % e)
                    continue


def find_path_between(context, one, two):
    max_steps = 10                      # put a hard limit on the max number of operator steps
    one = one.to_sp()
    two = two.to_sp()

    path_ways = [[sequence([]), one]]
    for _ in range(max_steps):
        new_path_ways = []
        for seq, r in path_ways:
            for op in r.apply_op(context, 'supported-ops').to_sp():
                new_seq = seq + sequence(op)
                new_r = r.apply_op(context, op.label[4:])
                if len(new_r) > 0:
                    if test_subset(two, new_r):
                        return new_seq.apply_sigmoid(clean)
                    new_path_ways.append([new_seq, new_r])
        path_ways = new_path_ways
    return ket('path not found')


def find_steps_between(op_path, context, one, two):
    path_ways = [one]
    for op in op_path:
        new_path_ways = []
        for step in path_ways:
            seq = sequence(step)
            next_step = step.apply_op(context, op.label[4:]).to_sp()
            if test_subset(two, next_step):
                return seq + two
                # return (seq + two).apply_sigmoid(clean)
            for elt in next_step:
                if len(elt) > 0:
                    new_path_ways.append(seq + elt)
        path_ways = new_path_ways
    return ket('steps not found')


def main(source):
    context = NewContext('find steps between')
    load_simple_sw_file(context, source)            # NB: we use this instead of context.load(source) for speed reasons
    # context.print_universe()                      # also means it only handles literal superpositions
                                                    # so no sequences, stored_rules, etc
    while True:
        node1 = input('Enter first node: ')
        node1 = node1.strip()

        # exit the agent:
        if node1 in ['q', 'quit', 'exit']:
            break

        node2 = input('Enter second node: ')
        node2 = node2.strip()
        if len(node1) == 0 or len(node2) == 0:
            continue

        one = ket(node1)
        two = ket(node2)
        start_time = time.time()
        op_path = find_path_between(context, one, two)
        if type(op_path) is ket and op_path.label == 'path not found':
            print('\npath not found!\n')
            continue
        print('\npath found:\n%s\n' % str(op_path))
        steps = find_steps_between(op_path, context, one, two)
        print('%s\n' % str(steps))
        end_time = time.time()
        delta_time = end_time - start_time
        print("\n  Time taken: %s\n" % display_time(delta_time))

main(source)
