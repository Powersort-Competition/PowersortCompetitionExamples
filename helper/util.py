def rank_reduce(lst):
    """ Returns a list of the same length as the input list, where each element
    is the rank of the corresponding element in the input list.
    """
    n = len(lst)

    # value, original index - sorted by value
    sorted_with_index = sorted([(lst[i], i) for i in range(n)])
    # return [sorted_with_index.index((lst[k], k)) for k in range(n)] # works, but slow

    # disregard elements - give only ranks
    rr = [0] * n
    for j, (_, index) in enumerate(sorted_with_index):
        rr[index] = j
    return rr


def rank_reduce_ties_desc(lst):
    """ Returns a list of the same length as the input list, where each element
    is the rank of the corresponding element in the input list.
    """
    n = len(lst)
    sorted_with_index = sorted([(lst[i], -i) for i in range(n)])
    # return [sorted_with_index.index((lst[k], k)) for k in range(n)] # works, but slow
    rr = [0] * n
    for j, (_, index) in enumerate(sorted_with_index):
        rr[-index] = j
    return rr


if __name__ == '__main__':
    import random

    A = [random.randint(1, 5) for _ in range(20)]
    print('\t'.join(map(str, A)))
    print('\t'.join(map(str, rank_reduce(A))))