import time

import numpy as np

import CRISPResso2Align as nw


def parse_input(path):
    seqs = []
    with open(path) as path_fh:
        line = path_fh.readline()
        while line:
            tokens = line.split('\t')
            seq1 = tokens[0]
            seq2 = tokens[1]
            seqs += [(seq1, seq2)]

            line = path_fh.readline()

    return seqs


if __name__ == '__main__':
    ALN_MATRIX = nw.read_matrix('EDNAFULL')
    SEQS = parse_input('../randtests.txt')
    SEQ1, SEQ2 = SEQS[0]
    NUM_REPEATS = 100
    times = []

    for _ in range(NUM_REPEATS):
        start = time.time()
        for seq1, seq2 in SEQS:
            gap_incentive = np.zeros(len(seq2) + 1, dtype=np.int)
            nw.global_align(
                seq1,
                seq2,
                matrix=ALN_MATRIX,
                gap_incentive=gap_incentive,
            )
        end = time.time()
        times += [end - start]

    print('Min: {0}'.format(min(times)))
    print('Mean: {0}'.format(sum(times) / len(times)))
    print('Max: {0}'.format(max(times)))
