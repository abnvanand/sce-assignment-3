def _lcs(new_list, old_list):
    if len(new_list) == 0 or len(old_list) == 0:
        return []

    new_first, *new_rest = new_list
    old_first, *old_rest = old_list
    if new_first == old_first:
        return [new_first] + _lcs(new_rest, old_rest)

    x = _lcs(new_rest, old_list)
    y = _lcs(new_list, old_rest)

    return x if len(x) > len(y) else y


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
    orig_list = open(old).readlines()
    new_list = open(new).readlines()

    lcs = _lcs(new_list, orig_list)
    diffs = _diff(list(orig_list), list(new_list), list(lcs))

    # print("lcs:", )
    # for i in lcs:
    #     print(i, end='')

    print("diff:", )
    for i in diffs:
        print(i, end='')


if __name__ == "__main__":
    # diff_helper("/home/abhinav/pintos.old/src/threads/synch.c", "/home/abhinav/pintos-anon/src/threads/synch.c")
    diff_helper("temp/file1.txt", "temp/file2.txt")
