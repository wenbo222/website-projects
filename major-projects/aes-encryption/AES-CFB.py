# Advanced Encryption Standard (AES)
# Using full-block CFB method of encryption
# Overall Citation: https://medium.com/codex/aes-how-the-most-advanced-encryption-actually-works-b6341c44edb9
# https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
# https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf
# Wenbo

import math
import sys

# S-box table
table=[["63", "7c", "77", "7b", "f2", "6b", "6f", "c5", "30", "01", "67", "2b", "fe", "d7", "ab", "76"],
       ["ca", "82", "c9", "7d", "fa", "59", "47", "f0", "ad", "d4", "a2", "af", "9c", "a4", "72", "c0"],
       ["b7", "fd", "93", "26", "36", "3f", "f7", "cc", "34", "a5", "e5", "f1", "71", "d8", "31", "15"],
       ["04", "c7", "23", "c3", "18", "96", "05", "9a", "07", "12", "80", "e2", "eb", "27", "b2", "75"],
       ["09", "83", "2c", "1a", "1b", "6e", "5a", "a0", "52", "3b", "d6", "b3", "29", "e3", "2f", "84"],
       ["53", "d1", "00", "ed", "20", "fc", "b1", "5b", "6a", "cb", "be", "39", "4a", "4c", "58", "cf"],
       ["d0", "ef", "aa", "fb", "43", "4d", "33", "85", "45", "f9", "02", "7f", "50", "3c", "9f", "a8"],
       ["51", "a3", "40", "8f", "92", "9d", "38", "f5", "bc", "b6", "da", "21", "10", "ff", "f3", "d2"],
       ["cd", "0c", "13", "ec", "5f", "97", "44", "17", "c4", "a7", "7e", "3d", "64", "5d", "19", "73"],
       ["60", "81", "4f", "dc", "22", "2a", "90", "88", "46", "ee", "b8", "14", "de", "5e", "0b", "db"],
       ["e0", "32", "3a", "0a", "49", "06", "24", "5c", "c2", "d3", "ac", "62", "91", "95", "e4", "79"],
       ["e7", "c8", "37", "6d", "8d", "d5", "4e", "a9", "6c", "56", "f4", "ea", "65", "7a", "ae", "08"],
       ["ba", "78", "25", "2e", "1c", "a6", "b4", "c6", "e8", "dd", "74", "1f", "4b", "bd", "8b", "8a"],
       ["70", "3e", "b5", "66", "48", "03", "f6", "0e", "61", "35", "57", "b9", "86", "c1", "1d", "9e"],
       ["e1", "f8", "98", "11", "69", "d9", "8e", "94", "9b", "1e", "87", "e9", "ce", "55", "28", "df"],
       ["8c", "a1", "89", "0d", "bf", "e6", "42", "68", "41", "99", "2d", "0f", "b0", "54", "bb", "16"]]

# S-box inverse table
table_inv=[["52", "09", "6a", "d5", "30", "36", "a5", "38", "bf", "40", "a3", "9e", "81", "f3", "d7", "fb"],
           ["7c", "e3", "39", "82", "9b", "2f", "ff", "87", "34", "8e", "43", "44", "c4", "de", "e9", "cb"],
           ["54", "7b", "94", "32", "a6", "c2", "23", "3d", "ee", "4c", "95", "0b", "42", "fa", "c3", "4e"],
           ["08", "2e", "a1", "66", "28", "d9", "24", "b2", "76", "5b", "a2", "49", "6d", "8b", "d1", "25"],
           ["72", "f8", "f6", "64", "86", "68", "98", "16", "d4", "a4", "5c", "cc", "5d", "65", "b6", "92"],
           ["6c", "70", "48", "50", "fd", "ed", "b9", "da", "5e", "15", "46", "57", "a7", "8d", "9d", "84"],
           ["90", "d8", "ab", "00", "8c", "bc", "d3", "0a", "f7", "e4", "58", "05", "b8", "b3", "45", "06"],
           ["d0", "2c", "1e", "8f", "ca", "3f", "0f", "02", "c1", "af", "bd", "03", "01", "13", "8a", "6b"],
           ["3a", "91", "11", "41", "4f", "67", "dc", "ea", "97", "f2", "cf", "ce", "f0", "b4", "e6", "73"],
           ["96", "ac", "74", "22", "e7", "ad", "35", "85", "e2", "f9", "37", "e8", "1c", "75", "df", "6e"],
           ["47", "f1", "1a", "71", "1d", "29", "c5", "89", "6f", "b7", "62", "0e", "aa", "18", "be", "1b"],
           ["fc", "56", "3e", "4b", "c6", "d2", "79", "20", "9a", "db", "c0", "fe", "78", "cd", "5a", "f4"],
           ["1f", "dd", "a8", "33", "88", "07", "c7", "31", "b1", "12", "10", "59", "27", "80", "ec", "5f"],
           ["60", "51", "7f", "a9", "19", "b5", "4a", "0d", "2d", "e5", "7a", "9f", "93", "c9", "9c", "ef"],
           ["a0", "e0", "3b", "4d", "ae", "2a", "f5", "b0", "c8", "eb", "bb", "3c", "83", "53", "99", "61"],
           ["17", "2b", "04", "7e", "ba", "77", "d6", "26", "e1", "69", "14", "63", "55", "21", "0c", "7d"]]

# rc table
table_rc=["00", "01", "02", "04", "08", "10", "20", "40", "80", "1b", "36"]

# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-represents-a-number-float-or-int
def is_number(s): # Determine whether the input is a number or not
    """
    is_number(string) -> boolean

    If string can be converted into float, returns True; otherwise, returns False.
    """
    
    try:
        float(s)
        return True # If s is a number, return True
    except (ValueError, TypeError):
        return False # Otherwise, return False


def input_a_number(): # Input a number and direct the user to change nonnumber inputs
    """
    input_a_number() -> float

    Ask the user for a float input; if the user input is not a number, asks the user to input again until the input is a number.
    Returns the float inputted.
    """
    
    s=input().lower().strip("!.,? ")
    while is_number(s)==False:
        if s=="pi" or s=="π":
            return math.pi
        elif s=="e":
            return math.e
        print("Please enter a number: ")
        s=input().lower().strip("!.,? ")
    return float(s)


def gmul(a, b):
    """
    guml(int, int) -> int

    Multiply two integers together in GF(2^8).
    """
    
    p=0x00
    for _ in range(8):
        if (b&1)!=0:
            p=p^a
        h=(a&0x80)!=0
        a=a<<1
        if h:
            a=a^0x1b
        b=b>>1
        
    return p%256


def gmul2(a):
    """
    gmul(int) -> int

    Multiply by 2 in GF(2^8).
    """
    
    h=a&0x80
    b=a<<1
    if h==0x80:
        b=b^0x1b
        
    return b%256


def gmul3(a):
    """
    gmul3(int) -> int

    Multiply by 3 in GF(2^8)
    """
    
    return (a^gmul2(a))%256


def decimal_to_16(n, flag):
    """
    decimal_to_16(int, int) -> string

    Converts a decimal to a hexadecimal, and returns the result.
    If the length of the string is smaller than the second integer, add "0"s until the length match.
    """
    
    result=""
    quotient=n
    while quotient!=0:
        r=quotient%16
        if r>=10:
            r=chr(r+87)
        result=str(r)+result
        quotient//=16
    
    while len(result)<flag:
        result="0"+result
    return result


def encrypt(text, key, iv, rounds):
    """
    encrypt(string/list, string, string, int) -> string

    Returns the encrypted message.
    """
    
    blocks=get_blocks(text, iv, False) # Plaintext
    new_blocks=get_blocks(text, iv, False) # Ciphertext
    keys=get_keys(key, rounds)
    
    for i in range(1, len(new_blocks)):
        # First round (0th round)
        new_blocks[i]=add_round_key(keys[0], new_blocks[i-1])

        # Remaining rounds (1th to rounds-2'th rounds)
        for j in range(1, rounds-1):
            new_blocks[i]=sub_bytes(new_blocks[i])
            new_blocks[i]=shift_rows(new_blocks[i])
            new_blocks[i]=mix_columns(new_blocks[i])                                                                                                                                                                     
            new_blocks[i]=add_round_key(keys[j], new_blocks[i])

        # Last round (round-1'th round)
        new_blocks[i]=sub_bytes(new_blocks[i])
        new_blocks[i]=shift_rows(new_blocks[i])
        new_blocks[i]=add_round_key(keys[rounds-1], new_blocks[i])
        
        # XOR the plaintext
        new_blocks[i]=add_round_key(blocks[i], new_blocks[i])
        
    ciphertext=reassemble(new_blocks[1:], True)
    return ciphertext


def decrypt(ciphertext, key, iv, rounds):
    """
    decrypt(string, string, string, int) -> string

    Returns the decrypted message.
    """
    
    blocks=get_blocks(ciphertext, iv, True) # Ciphertext
    new_blocks=get_blocks(ciphertext, iv, True) # Plaintext
    keys=get_keys(key, rounds)
    
    for i in range(1, len(new_blocks)):
        # First round (0th round)
        new_blocks[i]=add_round_key(keys[0], blocks[i-1])

        # Remaining rounds (1th to rounds-2'th rounds)
        for j in range(1, rounds-1):
            new_blocks[i]=sub_bytes(new_blocks[i])
            new_blocks[i]=shift_rows(new_blocks[i])
            new_blocks[i]=mix_columns(new_blocks[i])                                                                                                                                                                     
            new_blocks[i]=add_round_key(keys[j], new_blocks[i])

        # Last round (round-1'th round)
        new_blocks[i]=sub_bytes(new_blocks[i])
        new_blocks[i]=shift_rows(new_blocks[i])
        new_blocks[i]=add_round_key(keys[rounds-1], new_blocks[i])
        
        # XOR the ciphertext
        new_blocks[i]=add_round_key(blocks[i], new_blocks[i])
    
    text=reassemble(new_blocks[1:], False)
    return text


def get_blocks(text, iv, flag):
    """
    get_blocks(string, list, boolean) -> list

    Returns blocks based on the given text. The 0th block is the initialization vector.
    If the boolean is True, the text is in hexadecimal separated by spaces.
    """

    # If the input is hexadecimals, change them into normalt text first.
    if flag==True:
        letters=text.split()
        temp=""
        for letter in letters:
            temp+=chr(int(letter, base=16))
        text=temp

    # Calculate the number of iterations
    blocks=[]
##    if len(text)%16==0:
##        iterations=len(text)//16
##    else:
##        iterations=len(text)//16+1
    iterations=len(text)//16+1
    blocks.append(iv)
    
    # Break the text into blocks
    for i in range(iterations):
        temp=[]
        temp1=[]
        temp2=[]
        temp3=[]
        temp4=[]
        for j in range(i*16, (i+1)*16):
            character=""
            if j<len(text):
                character=text[j]
            else:
                # character=" "
                character=chr(0x10)
            if j%4==0:
                temp1.append(decimal_to_16(ord(character), 2))
            elif j%4==1:
                temp2.append(decimal_to_16(ord(character), 2))
            elif j%4==2:
                temp3.append(decimal_to_16(ord(character), 2))
            elif j%4==3:
                temp4.append(decimal_to_16(ord(character), 2))

        # Append the blocks
        temp.append(temp1)
        temp.append(temp2)
        temp.append(temp3)
        temp.append(temp4)
        blocks.append(temp)
    
    return blocks

        
def rotate(word):
    """
    rotate(string) -> string

    Returns the hexadecimal after doing a one-byte left circular shift.
    Note: only works on 4-byte hexadecimal.
    """

    temp=word[:2]
    return word[2:]+temp


def sub_word(word):
    """
    sub_word(string) -> int

    Returns the hexadecimal after applying AES S-box to each byte.
    Note: only works on 4-byte hexadecimal.
    """

    result=""
    for i in range(4):
        temp=word[2*i:2*(i+1)]
        result+=table[int(temp[0], base=16)][int(temp[1], base=16)]
        
    return int(result, base=16)


def rcon(i):
    """
    rcon(int) -> int

    Returns the hexadecimal after applying the rcon operation.
    """

    return int(table_rc[int(i)]+"000000", base=16)


def get_keys(key, rounds):
    """
    get_keys(string, int) -> list

    Returns a list of round keys. The string must be the key in hexadecimal format.
    """
    
    k=[] # Represents 32-bit word of the original key
    w=[] # Represents the 32-bit words that are round keys
    n=rounds-7
    for i in range(0, n):
        k.append(key[i*8:(i+1)*8])
    
    for i in range(4*rounds):
        if i<n:
            w.append(k[i])
        elif i>=n and i%n==0:
            w.append(int(w[i-n], base=16)^sub_word(rotate(w[i-1]))^rcon(i//n))
            w[i]=decimal_to_16(w[i], 8)
        elif i>=n and n==8 and i%n==4:
            w.append(int(w[i-n], base=16)^sub_word(w[i-1]))
            w[i]=decimal_to_16(w[i], 8)
        else:
            w.append(int(w[i-n], base=16)^int(w[i-1], base=16))
            w[i]=decimal_to_16(w[i], 8)

    keys=[]
    for i in range(rounds):
##        temp=""
##        for j in range(4*i, 4*(i+1)):
##            temp+=w[j]
##        keys.append(temp)
        temp1=[]
        temp2=[]
        temp3=[]
        temp4=[]
        for j in range(4*i, 4*(i+1)):
            temp1.append(w[j][:2])
            temp2.append(w[j][2:4])
            temp3.append(w[j][4:6])
            temp4.append(w[j][6:])
        temp=[]
        temp.append(temp1)
        temp.append(temp2)
        temp.append(temp3)
        temp.append(temp4)
        keys.append(temp)
        
    return keys


def add_round_key(key, block):
    """
    add_round_key(list, list) -> list

    Add the round key (the string) to every hexadecimal in the list in GF(2^8), and return it.
    """

    temp=[]
    for i in range(4):
        temp1=[]
        for j in range(4):
            temp1.append(decimal_to_16(int(block[i][j], base=16)^int(key[i][j], base=16), 2))
        temp.append(temp1)
    return temp


def sub_bytes(block):
    """
    sub_bytes(list) -> list

    Complete the S-box operation to every hexadecimal in the list.
    Return the modified list.
    """
    
    for i in range(4):
        for j in range(4):
            block[i][j]=table[int(block[i][j][0], base=16)][int(block[i][j][1], base=16)]
    return block


def sub_bytes_inv(block):
    """
    sub_bytes_inv(list) -> list

    Complete the inverse S-box operation to every hexadecimal in the list.
    Return the modified list.
    """
    
    for i in range(4):
        for j in range(4):
            block[i][j]=table_inv[int(block[i][j][0], base=16)][int(block[i][j][1], base=16)]
    return block


def shift_rows(block):
    """
    shift_rows(list) -> list

    Shifts the second row left 1.
    Shifts the third row left 2.
    Shifts the fourth row left 3.
    Returns the modified list.
    """

    # Initializations
    temp=[]
    temp1=[]
    temp2=[]
    temp3=[]
    temp4=[]

    # Append according to patterns
    for i in range(4):
        temp1.append(block[0][i])
    for i in range(1, 4):
        temp2.append(block[1][i])
    temp2.append(block[1][0])
    for i in range(2, 4):
        temp3.append(block[2][i])
    temp3.append(block[2][0])
    temp3.append(block[2][1])
    temp4.append(block[3][3])
    for i in range(3):
        temp4.append(block[3][i])
    temp.append(temp1)
    temp.append(temp2)
    temp.append(temp3)
    temp.append(temp4)
    
    return temp


def shift_rows_inv(block):
    """
    shift_rows_inv(list) -> list

    Shifts the second row right 1.
    Shifts the third row right 2.
    Shifts the fourth row right 3.
    Returns the modified list.
    """

    # Initializations
    temp=[]
    temp1=[]
    temp2=[]
    temp3=[]
    temp4=[]

    # Append according to patterns
    for i in range(4):
        temp1.append(block[0][i])
    temp2.append(block[1][3])
    for i in range(3):
        temp2.append(block[1][i])
    temp3.append(block[2][2])
    temp3.append(block[2][3])
    for i in range(2):
        temp3.append(block[2][i])
    for i in range(1, 4):
        temp4.append(block[3][i])
    temp4.append(block[3][0])
    temp.append(temp1)
    temp.append(temp2)
    temp.append(temp3)
    temp.append(temp4)
    
    return temp


def mix_columns(block):
    """
    mix_columns(list) -> list

    Multiply by a fixed matrix, and return the list.
    """
    
    for j in range(4):
        # Get integer values
        a=int(block[0][j], base=16)
        b=int(block[1][j], base=16)
        c=int(block[2][j], base=16)
        d=int(block[3][j], base=16)

        # Multiply by matrix
        block[0][j]=decimal_to_16(gmul2(a)^gmul3(b)^c^d, 2)
        block[1][j]=decimal_to_16(a^gmul2(b)^gmul3(c)^d, 2)
        block[2][j]=decimal_to_16(a^b^gmul2(c)^gmul3(d), 2)
        block[3][j]=decimal_to_16(gmul3(a)^b^c^gmul2(d), 2)
        
    return block


def mix_columns_inv(block):
    """
    mix_columns_inv(list) -> list

    Multiply by a fixed matrix (inverse), and return the list.
    """
    
    for j in range(4):
        # Get integer values
        a=int(block[0][j], base=16)
        b=int(block[1][j], base=16)
        c=int(block[2][j], base=16)
        d=int(block[3][j], base=16)
        
        # Multiply by matrix
        block[0][j]=decimal_to_16(gmul(a, 14)^gmul(b, 11)^gmul(c, 13)^gmul(d, 9), 2)
        block[1][j]=decimal_to_16(gmul(a, 9)^gmul(b, 14)^gmul(c, 11)^gmul(d, 13), 2)
        block[2][j]=decimal_to_16(gmul(a, 13)^gmul(b, 9)^gmul(c, 14)^gmul(d, 11), 2)
        block[3][j]=decimal_to_16(gmul(a, 11)^gmul(b, 13)^gmul(c, 9)^gmul(d, 14), 2)

    return block


def reassemble(blocks, flag):
    """
    reassemble(list) -> string

    Change the list into a string.
    If flag is True, the string will be hexadecimals separated by spaces.
    Otherwise, the string will be real text.
    """
    
    text=""
    for block in blocks:
        for j in range(4):
            for i in range(4):
                if flag:
                    text+=block[i][j]+" "
                else:
                    if block[i][j]=="10": # Remove the effect of padding
                        return text
                    text+=chr(int(block[i][j], base=16))
    return text

def process_request(choice, message, rounds, raw_key, raw_iv):
    """
    process_request(string, string, int, string, string) -> string

    Processes the request to encrypt or decrypt the message.
    """
    
    key=""
    for i in range(len(raw_key)):
        key+=decimal_to_16(ord(raw_key[i]), 2)

    iv=[]
    temp1=[]
    temp2=[]
    temp3=[]
    temp4=[]
    for i in range(0, 16, 4):
        temp1.append(decimal_to_16(ord(raw_iv[i]), 2))
        temp2.append(decimal_to_16(ord(raw_iv[i+1]), 2))
        temp3.append(decimal_to_16(ord(raw_iv[i+2]), 2))
        temp4.append(decimal_to_16(ord(raw_iv[i+3]), 2))
    iv.append(temp1)
    iv.append(temp2)
    iv.append(temp3)
    iv.append(temp4)

    if choice=="encrypt":
        return encrypt(message, key, iv, rounds)
    else:
        return decrypt(message, key, iv, rounds)

if __name__=="__main__":
    if len(sys.argv)>1:
        # CLI Mode: choice, message, rounds, key, iv
        choice=sys.argv[1].lower()
        message=sys.argv[2]
        rounds=int(sys.argv[3])
        raw_key=sys.argv[4]
        raw_iv=sys.argv[5]
        print(process_request(choice, message, rounds, raw_key, raw_iv))
    else:
        # Interactive Mode
        # Choose encryption/decryption
        choice=input("Encrypt or decrypt? ").lower().strip("!,.? ")
        while choice not in ["encrypt", "decrypt"]:
            choice=input("Invalid input! Encrypt or decrypt? ").lower().strip("!,.? ")
        if choice=="encrypt":
            print("Note that encrypting only accpets real text (not hexadecimals).")
        else:
            print("Note that decrypting only accepts hexadecimals, separated by spaces.")
    
        # Enter message
        message=input("Enter the message you want to "+choice+": ")
        print("Choose the number of rounds you want to "+choice+": ")
        print("Note that AES-128 requires 11 rounds, AES-192 requires 13 rounds, and AES-256 requires 15 rounds.")
        rounds=int(input_a_number())
        while rounds not in [11, 13, 15]:
            print("Please input the correct number: ")
            rounds=int(input_a_number())
    
        # Input Key
        print("Please input the key: ")
        temp_key=input()
        if rounds==11:
            while len(temp_key)!=16:
                print("The key must be 16 characters long.")
                temp_key=input()
        elif rounds==13:
            while len(temp_key)!=24:
                print("The key must be 24 characters long.")
                temp_key=input()
        else:
            while len(temp_key)!=32:
                print("The key must be 32 characters long.")
                temp_key=input()
    
        # Input initialization vector
        print("Please input the initialization vector: (16 characters long)")
        temp_iv=input()
        while len(temp_iv)!=16:
            print("The initialization vector must be 16 characters long!")
            temp_iv=input()
    
        # Print out the ciphertext/plaintext
        result=process_request(choice, message, rounds, temp_key, temp_iv)
        if choice=="encrypt":
            print("Here is the ciphertext:", result)
        else:
            print("Here is the plaintext:", result)
