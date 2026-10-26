from collections import defaultdict, Counter

def group_anagram(strs: list[str]) -> list[list[str]]:
    res = defaultdict(list)
    for s in strs:
        key = tuple(sorted(Counter(s).items()))
        res[key].append(s)
        return list(res.values())
