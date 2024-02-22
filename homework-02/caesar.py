import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            new_char_code = ord(char.upper()) + shift
            if new_char_code > ord('Z'):
                new_char_code -= 26
            new_char = chr(new_char_code)
            if char.isupper():
                ciphertext += new_char
            else:
                ciphertext += new_char.lower()
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            # определяем новый символ с учетом сдвига
            new_char_code = ord(char.upper()) - shift
            if new_char_code < ord('A'):
                new_char_code += 26
            new_char = chr(new_char_code)
            # сохраняем регистр символа
            if char.isupper():
                plaintext += new_char
            else:
                plaintext += new_char.lower()
        else:
            plaintext += char
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0
    max_word_matches = 0
    for shift in range(26):
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                new_char_code = ord(char.upper()) - shift
                if new_char_code < ord('A'):
                    new_char_code += 26
                new_char = chr(new_char_code)
                if char.isupper():
                    plaintext += new_char
                else:
                    plaintext += new_char.lower()
            else:
                plaintext += char
        word_matches = sum(word in dictionary for word in plaintext.split())
        if word_matches > max_word_matches:
            max_word_matches = word_matches
            best_shift = shift
    return best_shift
