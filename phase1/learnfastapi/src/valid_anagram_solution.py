def isAnagram(s,t):
    s_chars = [c for c in s]
    t_chars = [c for c in t]
    print(s_chars)
    print(t_chars)

    # if len(s_chars) == len(t_chars):
    #     for st in s_chars:
    #         if st not in t_chars:
    #             return False
    #     return True
    # return False

    s_chars, t_chars = s_chars.sort(), t_chars.sort()

    if s_chars == t_chars:
        return True
    return False
    

    # for st in s_chars:
    #     if st in t_chars:
    #         s_chars.remove(st)
    #         t_chars.remove(st)

    # if len(s_chars) != 0 and len(t_chars) != 0:
    #     return False
    
    # return True
        

print(isAnagram("ccac","aacc"))
print(isAnagram("bat","cat"))
print(isAnagram("racecar","carrace"))
print(isAnagram("tab","batt"))