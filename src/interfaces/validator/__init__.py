import re


def is_valid_document(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    def calc_digit(cpf, weights):
        return sum(int(cpf[i]) * weights[i] for i in range(len(weights))) % 11

    weights1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    digit1 = calc_digit(cpf, weights1)
    digit1 = 0 if digit1 < 2 else 11 - digit1

    weights2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    digit2 = calc_digit(cpf, weights2)
    digit2 = 0 if digit2 < 2 else 11 - digit2

    return cpf[-2:] == f'{digit1}{digit2}'
