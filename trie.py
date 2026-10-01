class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.end = True

    def search(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                return False

            node = node.children[char]

        return node.end

trie = Trie()

words = ["apple", "banana", "grape", "orange", "kiwi"]

for word in words:
    trie.insert(word)

word = input("Search word: ")

if trie.search(word):
    print(f"{word} is found in the trie.")
else:   
    print(f"{word} is not found in the trie.")