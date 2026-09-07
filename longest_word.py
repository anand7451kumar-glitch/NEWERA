def longest_word(sentence):
    words = sentence.split()

    longest = ""

    for word in words:
        if len(word) > len(longest):
            longest = word

    return longest

sentence = input("Enter a sentence:")

print("Longest word:", longest_word(sentence))
