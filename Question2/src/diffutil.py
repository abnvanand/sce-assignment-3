def _lcs(new_list, old_list, i, j, table):
    if i >= len(new_list) or j >= len(old_list):
        return []

    if table[i][j]:
        # cached info available
        return table[i][j]

    if new_list[i] == old_list[j]:
        return [new_list[i]] + _lcs(new_list, old_list, i + 1, j + 1, table)

    x = _lcs(new_list, old_list, i + 1, j, table)
    y = _lcs(new_list, old_list, i, j + 1, table)

    table[i][j] = x if len(x) > len(y) else y
    return table[i][j]


def _diff(old, new, subsequence):
    result = []
    while len(subsequence) > 0:
        sub_first = subsequence.pop(0)

        while len(new) > 0:
            new_first = new.pop(0)

            if new_first == sub_first:
                break

            result.append("+" + new_first)

        while len(old) > 0:
            old_first = old.pop(0)

            if old_first == sub_first:
                break

            result.append("-" + old_first)

        result.append(" " + sub_first)

    while len(new) > 0:
        new_first = new.pop(0)
        result.append("+" + new_first)

    while len(old) > 0:
        old_first = old.pop(0)
        result.append("-" + old_first)

    return result


def diff_helper(old, new):
    # FIXME: optimize memory usage
    new_list = open(new).readlines()
    orig_list = open(old).readlines()

    table = [["" for _ in range(len(orig_list))] for _ in range(len(new_list))]
    lcs = _lcs(new_list, orig_list, 0, 0, table)
    diffs = _diff(list(orig_list), list(new_list), list(lcs))

    print("lcs:", )
    for i in lcs:
        print(i, end='')

    print("diff:", )
    for i in diffs:
        print(i, end='')


if __name__ == "__main__":
    diff_helper("/home/abhinav/pintos.old/src/threads/synch.c", "/home/abhinav/pintos-anon/src/threads/synch.c")
    # diff_helper("temp/file1.txt", "temp/file2.txt")
