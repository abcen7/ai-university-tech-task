def reverse_string(row_to_reverse: str) -> str:
    return row_to_reverse[::-1]

def is_palindrome(row: str) -> bool:
    return row == row[::-1]

print(reverse_string("abcd"), is_palindrome("abcd"))
print(reverse_string("abba"), is_palindrome("abba"))