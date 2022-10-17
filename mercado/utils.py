
MATRIX_X86_64 = ('x86_64', 'amd64')


def is_valid_architecture(expected: str, actual: str) -> bool:
    '''
    Equalize architectures that their name does not necessarily match
    '''
    if expected in MATRIX_X86_64:
        for arch in MATRIX_X86_64:
            if arch in actual:
                return True

    return expected in actual
