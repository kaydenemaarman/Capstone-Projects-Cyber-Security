# This program encodes a user-provided message using a Caesar Cipher by shifting
# each alphabetic character 15 positions forward.

def caesar_cipher_encode(message: str, shift: int) -> str:
    """
    Encode a message using a Caesar Cipher.

    Args:
        message (str): The plaintext message to encode.
        shift (int): The number of positions to shift each letter.

    Returns:
        str: The encoded message.
    """
    encoded_message = []

    for char in message:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            start = ord('A') if char.isupper() else ord('a')

            # Shift the character and wrap around the alphabet
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            encoded_message.append(shifted_char)
        else:
            # Non-alphabetic characters remain unchanged
            encoded_message.append(char)

    return ''.join(encoded_message)


# ---- Main program ----

# Ask the user for a message
message = input("Enter a message to encode: ")

# Encode using a fixed shift of 15
encoded = caesar_cipher_encode(message, 15)

# Print the encoded message
print("Encoded message:", encoded)
