# Definindo a S-Box
s_box = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

# Definindo a Rcon
Rcon = [
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f,
    0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4
]

# Função SubBytes
def SubBytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = s_box[state[i][j]]
    return state

# Função ShiftRows
def shift_rows(state):
    # Converte o vetor de 16 elementos em uma matriz 4x4
    matrix = [state[i:i + 4] for i in range(0, 16, 4)]
    
    # Rotaciona as linhas
    matrix[1] = matrix[1][1:] + matrix[1][:1]  # Rotaciona a segunda linha uma posição à esquerda
    matrix[2] = matrix[2][2:] + matrix[2][:2]  # Rotaciona a terceira linha duas posições à esquerda
    matrix[3] = matrix[3][3:] + matrix[3][:3]  # Rotaciona a quarta linha três posições à esquerda
    
    # Retorna a matriz achatada
    return [byte for row in matrix for byte in row]

# Função para multiplicar no campo finito (Galois Field)
def galois_mult(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80
        a <<= 1
        if carry:
            a ^= 0x1b
        b >>= 1
    return p & 0xff

# Função MixColumns corrigida
def MixColumns(state):
    for i in range(4):
        a = state[i]
        state[i] = [
            galois_mult(a[0], 2) ^ galois_mult(a[1], 3) ^ a[2] ^ a[3],
            a[0] ^ galois_mult(a[1], 2) ^ galois_mult(a[2], 3) ^ a[3],
            a[0] ^ a[1] ^ galois_mult(a[2], 2) ^ galois_mult(a[3], 3),
            galois_mult(a[0], 3) ^ a[1] ^ a[2] ^ galois_mult(a[3], 2)
        ]
    return state

# Função AddRoundKey
def AddRoundKey(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    return state

# Função SubWord
def SubWord(word):
    return [s_box[b] for b in word]

# Função RotWord
def RotWord(word):
    return word[1:] + word[:1]

# Função para converter a chave expandida em uma matriz 4x4
def KeyToMatrix(key):
    return [key[i:i+4] for i in range(0, len(key), 4)]

# Função de expansão de chave corrigida
def KeyExpansion(key):
    w = [0] * 44  # 44 palavras de 4 bytes para 11 rodadas
    
    # As 4 primeiras palavras são simplesmente a chave
    for i in range(4):
        w[i] = key[4 * i:4 * (i + 1)]
    
    # Expansão para as 40 palavras restantes
    for i in range(4, 44):
        temp = w[i - 1]
        
        if i % 4 == 0:
            temp = SubWord(RotWord(temp))
            temp[0] ^= Rcon[i // 4 - 1]
        
        w[i] = [(w[i - 4][j] ^ temp[j]) for j in range(4)]
    
    # Transformando em um array de 4x4 por rodada
    expanded_key = [w[i:i + 4] for i in range(0, len(w), 4)]
    return expanded_key

def print_table(label, state):
    print(f"\n{label}:")
    print("+----+----+----+----+")
    for col in range(4):
        print("| " + " | ".join(f"{state[row][col]:02x}" for row in range(4)) + " |")
        print("+----+----+----+----+")

def AES_encrypt(plaintext, key):
    # Convertendo o plaintext em matriz de estado 4x4
    state = KeyToMatrix(plaintext)
    
    # Expansão da chave
    expanded_key = KeyExpansion(key)
    
    # Adiciona a primeira rodada da chave
    state = AddRoundKey(state, expanded_key[0])
        
# 9 rodadas principais
    for round_num in range(1, 11):  # Mudado para 1 a 9
    # Imprime o estado no início da rodada
        print_table(f"Início da Rodada {round_num}", state)
    
    # Passo SubBytes
        state = SubBytes(state)
        print_table(f"Após SubBytes {round_num}", state)

    # Passo ShiftRows
        state = shift_rows(state)  # Correção aqui
        print_table(f"Após ShiftRows {round_num}", state)

    # Passo MixColumns (somente nas 9 primeiras rodadas)
        state = MixColumns(state)
        print_table(f"Após MixColumns {round_num}", state)

    # Chave da rodada
        round_key = expanded_key[round_num]
        print_table(f"Chave da Rodada {round_num}", round_key)

# Rodada final (sem MixColumns)
    state = SubBytes(state)
    state = shift_rows(state)  # Correção aqui
    final_round_key = expanded_key[10]
    state = AddRoundKey(state, final_round_key)

    print_table("Texto Cifrado Final", state)

    # Achatar a matriz de estado para obter a lista final de bytes
    return [state[row][col] for col in range(4) for row in range(4)]

# Função para converter string hexadecimal em lista de inteiros
def hex_to_bytes(hex_string):
    return [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]

# Definindo o plaintext e a chave em formato hexadecimal
plaintext_hex = "0123456789abcdeffedcba9876543210"
key_hex = "0f1571c947d9e8590cb7add6af7f6798"

# Convertendo o texto claro e a chave
plaintext = hex_to_bytes(plaintext_hex)
key = hex_to_bytes(key_hex)

# Chamar a função AES_encrypt para criptografar o texto
ciphertext = AES_encrypt(plaintext, key)

# Exibir o resultado da criptografia
print("Texto Cifrado:", ''.join(f'{byte:02x}' for byte in ciphertext))

