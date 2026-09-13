def letter_combinations(digits):
    if not digits:
        return []
    
    phone = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz"
    }

    result = []

    def backtrack(index, current):
        if index == len(digits):
            result.append(current)
            return

        for char in phone[digits[index]]:
            backtrack(index + 1, current + char)

    backtrack(0, "")
    return result

digits = input("Enter digits (2-9): ")

print("Combinations:", letter_combinations(digits))
