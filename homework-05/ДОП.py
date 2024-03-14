with open('cipher.txt', 'r') as file:
    ciphertext = file.read()

import numpy as np

def calculate_ic(text):
    text = text.replace(" ", "")  # Удаляем пробелы
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    ic = 0
    n = len(text)
    for count in freq.values():
        ic += count * (count - 1)
    ic /= n * (n - 1)
    return ic

def find_key_length(ciphertext):
    possible_lengths = np.arange(1, len(ciphertext)//2 + 1)
    ic_values = []
    for length in possible_lengths:
        subtexts = [ciphertext[i::length] for i in range(length)]
        ic_average = np.mean([calculate_ic(subtext) for subtext in subtexts])
        ic_values.append(ic_average)
    return possible_lengths[np.argmax(ic_values)]

key_length = find_key_length(ciphertext)
print("Длина ключа:", key_length)

def decrypt_vigenere(ciphertext, key_length):
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    decrypted_text = ''
    for i in range(key_length):
        subtext = ciphertext[i::key_length]
        frequencies = {}
        for char in alphabet:
            frequencies[char] = subtext.count(char)
        most_frequent_char = max(frequencies, key=frequencies.get)
        key_char = alphabet.index(most_frequent_char)
        for char in subtext:
            decrypted_char = alphabet[(alphabet.index(char) - key_char) % len(alphabet)]
            decrypted_text += decrypted_char
    return decrypted_text

decrypted_text = decrypt_vigenere(ciphertext, key_length)
print("Расшифрованный текст:")
print(decrypted_text)



