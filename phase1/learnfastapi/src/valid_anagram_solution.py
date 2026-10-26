from collections import Counter
def isAnagram(s:str,t:str) -> bool:

    if len(s) == len(t):
        return Counter(s) == Counter(t)
    return False

print(isAnagram("ccac","aacc"))
print(isAnagram("bat","cat"))
print(isAnagram("racecar","carrace"))
print(isAnagram("tab","batt"))