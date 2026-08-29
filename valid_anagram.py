from collections import Counter

def is_anagram(s, t):
  return Counter(s) == Counter(t)

s = input("Enter first string: ").lower()
t = input("Enter second string: ").lower()

if is_anagram(s, t):
  print("The strings are anagrams.")
else:
  print("The strings are not anagrams.")
