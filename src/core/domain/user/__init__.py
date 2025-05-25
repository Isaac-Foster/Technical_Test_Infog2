import re
import string


class WeakPasswordError(Exception):
    def __init__(self, password, message: str = 'Senha é muito fraca'):
        self.message = message
        super().__init__(self.message)


def is_strong_pass(
    passwd: str,
    chars: int = 8,
    lowers: int = 3,
    uppers: int = 1,
    digits: int = 1,
):  # noqa
    is_strong = re.search(
        (
            '(?=^.{%i,}$)'
            '(?=.*[a-z]{%i,})'
            '(?=.*[A-Z]{%i})'
            '(?=.*[0-9]{%i,})'
            '(?=.*[%s}]+)'
        )
        % (chars, lowers, uppers, digits, re.escape(string.punctuation)),
        passwd,
    )

    if not is_strong:
        if len(passwd) < chars:
            return WeakPasswordError(
                passwd, f'A senha deve ter pelo menos {chars} caracteres'
            )
        if not any(char.isdigit() for char in passwd):
            return WeakPasswordError(
                passwd, 'A senha deve conter pelo menos um dígito'
            )
        if not any(char.isupper() for char in passwd):
            return WeakPasswordError(
                passwd, 'A senha deve conter pelo menos uma letra maiúscula'
            )
        if not any(char.islower() for char in passwd):
            return WeakPasswordError(
                passwd, 'A senha deve conter pelo menos uma letra minúscula'
            )
        if not any(char in string.punctuation for char in passwd):
            return WeakPasswordError(
                passwd, 'A senha deve conter pelo menos um caractere especial'
            )
    return True


class UserDomain:
    @classmethod
    def strong_password(self, password: str):
        return is_strong_pass(password)

    @classmethod
    def auth(self, data, hash_manager):
        return hash_manager.check(*data)
