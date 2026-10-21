def isAnagram(s,t):
    s_chars = [c for c in s]
    t_chars = [c for c in t]
    print(s_chars)
    print(t_chars)

    for st in s_chars:
        if st not in t_chars:
            return False
    return True

isAnagram("tab","bat")