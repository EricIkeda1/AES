def KeyExpansion(key):
    w = [0] * 44  # Cria um vetor de 44 posições
    temp = 0

    # Preenche as primeiras 4 palavras (w[0] a w[3])
    for i in range(4):
        w[i] = (key[4*i], key[4*i+1], key[4*i+2], key[4*i+3])

    # Expande a chave para gerar as 44 palavras
    for i in range(4, 44):
        temp = w[i - 1]
        if i % 4 == 0:
            w[i] = w[i - 4]
        else:
            w[i] = temp

    return w
