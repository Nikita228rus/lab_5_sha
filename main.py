from constants import *


def text_to_bin(text):
    return ''.join(format(x, '08b') for x in bytearray(text, 'utf-8'))


def text_bin(s: str) -> str:
    return "".join(f"{ord(i):08b}" for i in s)


message = 'hello'
message = text_to_bin(message)


def logic_and(a, b):
    result = ''
    for i in range(len(a)):
        result += str(int(a[i]) & int(b[i]))
    return result


def logic_not(a):
    result = ''
    for i in range(len(a)):
        if int(a[i]) == 1:
            result += '0'
        elif int(a[i]) == 0:
            result += '1'
    return result


def x_change(k, a: str) -> str:
    out_list = []

    for i in range(len(k)):
        out_list.append(str(pow(int(k[i]) + int(a[i]), 1, 2)))

    return "".join(out_list)


def Ch(x, y, z):
    return x_change(logic_and(x, y), logic_and(logic_not(x), z))


def Maj(x, y, z):
    return x_change(x_change(logic_and(x, y), logic_and(x, z)), logic_and(y, z))


def bin_to_dec(x):
    result = int()
    for i in range(len(x)):
        result += int(x[i]) * pow(2, len(x) - 1 - i)

    return result


def sig_0(x):
    return x_change(x_change(right_rows(x, 2), right_rows(x, 13)), right_rows(x, 22))


def sig_1(x):
    return x_change(x_change(right_rows(x, 6), right_rows(x, 11)), right_rows(x, 25))


def sigma_0(x):
    return x_change(x_change(right_rows(x, 7), right_rows(x, 18)), right(x, 3))


def sigma_1(x):
    return x_change(x_change(right_rows(x, 17), right_rows(x, 19)), right(x, 10))


def right_rows(row, x):
    for i in range(x):
        row = row[-1] + row[:len(row)-1]
    return row


def right(row, x):
    for i in range(x):
        row = '0' + row[:len(row)-1]
    return row


def bin_dec_4byte(x):
    if x[0] == '0':
        result = int()
        for i in range(len(x)):
            result += int(x[i]) * pow(2, len(x) - 1 - i)

        return result

    elif x[0] == '1':
        var = x
        x = x[:31]
        temp_list = []
        for i in range(len(x)):
            if x[i] == '1':
                temp_list.append('0')
            elif x[i] == '0':
                temp_list.append('1')

        x = ''.join(temp_list)
        x = int(x, 2)
        if var[-1] == '1':
            x = 2 * x + 1
        elif var[-1] == '0':
            x = 2 * x + 2
        x = (bin(x)[2:])
        result = int()
        for i in range(len(x)):
            result += int(x[i]) * pow(2, len(x) - 1 - i)

        return -result


def sha_256(M):
    l = len(M)
    k = pow(448 - l - 1, 1, 512)
    M = M + '1' + '0' * k
    M = M[:448]
    l = format(l, '0b')
    while len(l) != 64:
        l = '0' + l
    M = M + l
    W = []
    for i in range(len(M)):
        var = None
        if i % 32 == 0:
            var = M[i:i+32]
            W.append(var)
    while len(W) != 64:
        W = W + ['00000000000000000000000000000000']

    print(W)
    for i in range(16, 64, 1):
        s0 = sigma_0(W[i-15])
        s1 = sigma_1(W[i-2])
        W[i] = format(pow(int(W[i-16], 2) + int(s0, 2) + int(W[i - 7], 2) + int(s1, 2), 1, pow(2, 32)), '0b')
        while len(W[i]) != 32:
            W[i] = '0' + W[i]

    a = h_c_bin[0]
    b = h_c_bin[1]
    c = h_c_bin[2]
    d = h_c_bin[3]
    e = h_c_bin[4]
    f = h_c_bin[5]
    g = h_c_bin[6]
    h = h_c_bin[7]

    for t in range(0, 64):
        T1 = pow(int(h, 2) + int(sig_1(e), 2) + int(Ch(e, f, g,), 2) + int(k_c_bin[t], 2) + int(W[t], 2), 1, pow(2, 32))
        T2 = pow(int(sig_0(a), 2) + int(Maj(a, b, c), 2), 1, pow(2, 32))
        h = g
        g = f
        f = e
        e = bin(pow(int(d, 2) + T1, 1, pow(2, 32)))[2:].zfill(32)
        d = c
        c = b
        b = a
        a = bin(pow(T1 + T2, 1, pow(2, 32)))[2:].zfill(32)

    result = [None] * 8
    result[0] = bin(pow(int(h_c_bin[0], 2) + int(a, 2), 1, pow(2, 32)))[2:].zfill(32)
    result[1] = bin(pow(int(h_c_bin[1], 2) + int(b, 2), 1, pow(2, 32)))[2:].zfill(32)
    result[2] = bin(pow(int(h_c_bin[2], 2) + int(c, 2), 1, pow(2, 32)))[2:].zfill(32)
    result[3] = bin(pow(int(h_c_bin[3], 2) + int(d, 2), 1, pow(2, 32)))[2:].zfill(32)
    result[4] = bin(pow(int(h_c_bin[4], 2) + int(e, 2), 1, pow(2, 32)))[2:].zfill(32)
    result[5] = bin(pow(int(h_c_bin[5], 2) + int(f, 2), 1, pow(2, 32)))[2:].zfill(32)
    result[6] = bin(pow(int(h_c_bin[6], 2) + int(g, 2), 1, pow(2, 32)))[2:].zfill(32)
    result[7] = bin(pow(int(h_c_bin[7], 2) + int(h, 2), 1, pow(2, 32)))[2:].zfill(32)

    for i in range(len(result)):
        result[i] = hex(int(result[i], 2))[2:]

    return ''.join(result)


sha_256(test_m)
