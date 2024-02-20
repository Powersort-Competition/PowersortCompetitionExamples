import random
from typing import List


def random_permutation(n: int, random: random.Random = random.Random()) -> List[int]:
    """ returns the numbers from 0 to n in random order """
    A = list(range(n))
    random.shuffle(A)
    return A


def random_runs(n, expRunLen, random):
    """ returns the numbers from 0 to n in random order, with runs of expected length expRunLen """
    A = random_permutation(n, random)
    sort_random_runs(A, 0, n - 1, expRunLen, random)
    return A


def shuffle(A, left, right, random):
    for i in range(right, left, -1):
        j = random.randint(left, i)
        A[i], A[j] = A[j], A[i]


def sort_random_runs(A, left, right, expRunLen, random=random.Random()):
    i = left
    # for the whole input
    while i < right:
        l = 1

        # for a random duration, approximately expRunLen, increase the run size
        while random.randint(0, expRunLen - 1) != 0:
            l += 1

        # sort the elements into a run of length l
        j = min(right, i + l)
        A[i:j + 1] = sorted(A[i:j + 1])

        i = j + 1


def exponential_random_run_lengths(n, expRunLen, random=random.Random()):
    rl = []
    i = 0
    while i < n:
        l = 1
        while random.randint(0, expRunLen - 1) != 0:
            l += 1
        rl += [min(l, n - i)]
        i += l
    return rl


def timsort_drag_run_lengths(n):
    if n <= 3:
        return [n]
    else:
        nPrime = n // 2
        nPrimePrime = n - nPrime - (nPrime - 1)
        return timsort_drag_run_lengths(nPrime) + timsort_drag_run_lengths(nPrime - 1) + [
            nPrimePrime]


def fill_with_timsort_drag(A, minRunLen, random):
    N = len(A)
    n = N // minRunLen
    RTim = timsort_drag_run_lengths(n)
    fill_with_up_and_down_runs(A, RTim, minRunLen, random)


def tims_random_run_lengths(n_runs=10000, short_run_prob=0.80, short_run_range=(1, 100),
                            long_run_range=(1000, 10000), random=random.Random()):
    """ produces a mix of short and long runs, with p chance of a short run, and an inexact length """
    runs = []
    for i in range(n_runs):
        switch = random.random()
        if switch < short_run_prob:
            x = random.randrange(short_run_range[0], short_run_range[1])
        else:
            x = random.randrange(long_run_range[0], long_run_range[1])
        runs.append(x)
    return runs


def fill_with_up_and_down_runs(A, runLengths, runLenFactor, random):
    """Fills the given array A with a random input that runs of the given list of run
    lengths, alternating between ascending and descending runs.
    More precisely, the array is first filled with a random permutation
    of [1..n], and then for i=0..l-1 segments of runLengths.get(i) * runLenFactor
    are sorted ascending when i mod 2 == 0 and descending otherwise
    (where l = runLengths.size()).
    The sum of all lengths in runLengths times runLenFactor should be equal to the
    length of A.
    """
    n = len(A)
    assert sum(runLengths) * runLenFactor == n
    for i in range(n):
        A[i] = i + 1
    shuffle(A, 0, n - 1, random)
    reverse = False
    i = 0
    for l in runLengths:
        L = l * runLenFactor
        A[i:i + L] = sorted(A[i:i + L])
        if reverse:
            A[i:i + L] = reversed(A[i:i + L])
        reverse = not reverse
        i += L


def fill_with_asc_runs_high_to_low(A, runLengths, runLenFactor):
    """Fills the given array A with ascending runs of the given list of run
    lengths.
    More precisely, the array is first filled n, n-1, ..., 1
    and then for i=0..l-1 segments of runLengths.get(i) * runLenFactor
    are sorted ascending.
    The sum of all lengths in runLengths times runLenFactor should be equal to the
    length of A.
    """
    n = len(A)
    # raises a flag if this is false: testing only
    assert sum(runLengths) * runLenFactor == n

    # A lists the numbers from 1 to i, high to low
    for i in range(n):
        A[i] = n - i
    i = 0

    # sorts these runs low to high
    for l in runLengths:
        L = l * runLenFactor
        A[i:i + L] = sorted(A[i:i + L])
        i += L


def fill_with_asc_runs_same(A, runLengths, runLenFactor, use_n_as_last_entry=True):
    """Fills the given list with ascending runs, all starting at 1,2,3, but ending with n"""
    n = len(A)
    assert sum(runLengths) * runLenFactor == n
    i = 0
    for l in runLengths:
        L = l * runLenFactor
        A[i:i + L] = range(1, L + 1)
        if use_n_as_last_entry:
            A[i + L - 1] = n
        i += L


def fill_with_dups_desc(A, runLengths, runLenFactor):
    i = 0
    u = len(runLengths)
    for l in runLengths:
        L = runLenFactor * l
        for j in range(L):
            A[i] = u
            i += 1
        u -= 1


def random_uary_array(u, len, random=random.Random()):
    """return new array filled with iid uniform numbers in [1..u]"""
    res = [0] * len
    for i in range(len):
        res[i] = random.randint(1, u)
    return res


if __name__ == "__main__":
    import util


    def input_generator(n, RNG):
        p = 0.8
        short = (1, 100)
        long = (1000, 10000)
        print(round(10000 * (p * 0.5 * sum(short) + (1 - p) * 0.5 * sum(long))))
        nRuns = max(2, int(n / (p * 0.5 * sum(short) + (1 - p) * 0.5 * sum(long))))
        print(nRuns)
        run_lens = tims_random_run_lengths(nRuns, p, short, long, RNG)
        nn = sum(run_lens)
        print(nn)
        lst = [0] * nn
        fill_with_asc_runs_same(lst, run_lens, 1, use_n_as_last_entry=False)
        lst = util.rank_reduce_ties_desc(lst)
        return lst


    input_generator(10000000, random.Random())