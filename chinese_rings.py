#!/usr/bin/env python3
# Wentao Han (wentao.han@gmail.com)
# Chinese Rings Puzzle Solver

import argparse
import sys


def solve(prefix, source, target):
    length = len(source)
    for i in range(length):
        if source[i] != target[i]:
            prefix2 = prefix + source[:i]
            source2 = source[i + 1:]
            target2 = '1' + '0' * (len(source2) - 1) if source2 else ''
            num_steps1 = solve(prefix2 + source[i], source2, target2)
            print('{0} -> {1}'.format(prefix2 + source[i] + target2, prefix2 + target[i] + target2))
            source2 = target2
            target2 = target[i + 1:]
            num_steps2 = solve(prefix2 + target[i], source2, target2)
            return num_steps1 + 1 + num_steps2
    else:
        return 0


def main():
    parser = argparse.ArgumentParser('Solve Chinese rings puzzle.')
    parser.add_argument('-n', '--rings',
                        type=int,
                        default=0,
                        help='the number of rings')
    parser.add_argument('-s', '--source',
                        default='',
                        help='the initial state')
    parser.add_argument('-t', '--target',
                        default='',
                        help='the target state')
    args = parser.parse_args()
    if ((args.rings and args.source and args.rings != len(args.source)) or
            (args.rings and args.target and args.rings != len(args.target)) or
            (args.source and args.target and len(args.source) != len(args.target))):
        raise ValueError('lengths not matched')
    if (not all(c in '01' for c in args.source) or
            not all(c in '01' for c in args.target)):
        raise ValueError('invalid state')
    if not args.rings and not args.source and not args.target:
        args.rings = 9
    elif not args.rings and args.source and not args.target:
        args.rings = len(args.source)
    elif not args.rings and not args.source and args.target:
        args.rings = len(args.target)

    source = args.source if args.source else '1' * args.rings
    target = args.target if args.target else '0' * args.rings
    num_steps = solve('', source, target)
    print('Total steps: {0}'.format(num_steps))


if __name__ == '__main__':
    sys.exit(main())
