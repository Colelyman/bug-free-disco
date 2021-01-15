import ctypes
import time

import numpy as np


def parse_aln_matrix(path):
    with open(path) as path_fh:
        headers = None
        while headers is None:
            header_line = path_fh.readline().strip()
            if header_line[0] == '#':
                continue
            headers = [ord(x) for x in header_line.split(' ') if x]
        mat_size = max(headers) + 1

        a = np.zeros((mat_size, mat_size), dtype=np.int32)

        for ai, line in enumerate(path_fh):
            weights = [int(x) for x in line[:-1].split(' ')[1:] if x]
            for ohidx, weight in zip(headers, weights):
                a[headers[ai], ohidx] = weight

        return a


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
    ALN_MATRIX = parse_aln_matrix('EDNAFULL')
    SEQS = parse_input('../randtests.txt')
    SEQ1, SEQ2 = SEQS[0]
    NUM_REPEATS = 100
    FUN = ctypes.CDLL('libfun.so')
    FUN.setup.argtypes = [np.ctypeslib.ndpointer(dtype=np.int32)]
    FUN.setup(ALN_MATRIX)
    FUN.global_align.argtypes = [
        ctypes.c_char_p,
        ctypes.c_char_p,
        np.ctypeslib.ndpointer(dtype=np.int32),
    ]
    FUN.global_align.restype = ctypes.c_char_p
    times = []

    for _ in range(NUM_REPEATS):
        start = time.time()
        for seq1, seq2 in SEQS:
            gap_incentive = np.zeros(len(seq2) + 1, np.int32)
            FUN.global_align(
                seq1.encode(),
                seq2.encode(),
                gap_incentive,
            )
        end = time.time()
        times += [end - start]

    FUN.done()

    print('Min: {0}'.format(min(times)))
    print('Mean: {0}'.format(sum(times) / len(times)))
    print('Max: {0}'.format(max(times)))
