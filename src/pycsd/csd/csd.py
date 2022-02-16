"""
 Canonical Signed Digit Functions

 Handles:
  * Decimals
  *
  *

 eg, +00-00+000.0 or 0.+0000-00+
 Where: '+' is +1
        '-' is -1

 Harnesser
 License: GPL2
"""
from math import ceil, fabs, log


def to_csd(num: float, places: int) -> str:
    """
    Convert the argument `num` to a string in CSD Format.
    Parameters
    ----------
    num : scalar (integer or real)
              decimal value to be converted to CSD format
    places: integer
        number of fractional places. Default is places = 0 (integer number)
    Returns
    -------
    string
        containing the CSD value
    Original author: Harnesser
    https://sourceforge.net/projects/pycsd/
    License: GPL2
    """

    # figure out binary range, special case for 0
    if num == 0.0:
        return "0"
    
    absnum = fabs(num)
    n = 0 if absnum < 1.0 else cell(log(absnum * 1.5, 2))
    csd_str = "0" if absnum < 1.0 else ""
    pow2n = pow(2.0, n - 1)
    while n > -places:
        if n == 0:
            csd_str += '.'
        
        n -= 1
        # convert the number
        d = 1.5 * num
        if d > pow2n:
            csd_str += '+'
            num -= pow2n
        elif d < -pow2n:
            csd_str += '-'
            num += pow2n
        else:
            csd_str += '0'
        
        pow2n /= 2.0
    
    return csd_str


def to_decimal(csd_str: str) -> float:
    """ Convert the CSD string to a decimal """

    num: float = 0.0
    loc: int = 0
    for i, c in enumerate(csd_str):
        if c == '0':
            num *= 2.0
        elif c == '+':
            num = num * 2.0 + 1.0
        elif c == '-':
            num = num * 2.0 - 1.0
        elif c == '.':
            loc = i + 1
        else:
            raise ValueError
    
    if loc != 0:
        num /= pow(2.0, len(csd_str) - loc)

    return num


def to_csdfixed(num: float, nnz: int) -> str:
    """ Convert the argument to CSD Format. """

    if num == 0.0:
        return "0"

    absnum = fabs(num)
    n = 0 if absnum < 1.0 else cell(log(absnum * 1.5, 2))
    csd_str = "0" if absnum < 1.0 else ""
    pow2n = pow(2.0, n - 1)
    while n > 0 or (nnz > 0 and fabs(num) > 1e-100):
        if n == 0:
            csd_str += '.'
        n -= 1
        d = 1.5 * num
        if d > pow2n:
            csd_str += '+'
            num -= pow2n
            nnz -= 1
        elif d < -pow2n:
            csd_str += '-'
            num += pow2n
            nnz -= 1
        else:
            csd_str += '0'
        
        pow2n /= 2.0
        if nnz == 0:
            num = 0.0
    return csd_str


if __name__ == "main":
    assert to_csd(28.5, 2) == "+00-00.+0"
    assert to_csd(-0.5, 2) == "0.-0"

    assert to_decimal("+00-00.+") == 28.5
    assert to_decimal("0.-") == -0.5

    assert to_csdfixed(28.5, 4) == "+00-00.+"
    assert to_csdfixed(-0.5, 4) == "0.-"
