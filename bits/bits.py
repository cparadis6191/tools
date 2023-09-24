#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK


import argparse
import sys

_HAS_ARGCOMPLETE = True

try:
    import argcomplete
except ImportError:
    _HAS_ARGCOMPLETE = False


def _to_bits(byte_string):
    """
    >>> _to_bits("non-hexadecimal number")
    Traceback (most recent call last):
    ValueError: non-hexadecimal number found in fromhex() arg at position 0
    >>> _to_bits("")
    '00000000'
    >>> _to_bits("0")
    '00000000'
    >>> _to_bits("3")
    '00110000'
    >>> _to_bits("00")
    '00000000'
    >>> _to_bits("40")
    '01000000'
    >>> _to_bits("c0")
    '11000000'
    >>> _to_bits("a0")
    '10100000'
    >>> _to_bits("b0")
    '10110000'
    >>> _to_bits("02")
    '00000010'
    >>> _to_bits("01")
    '00000001'
    >>> _to_bits("deadbeef")
    '11011110101011011011111011101111'
    >>> _to_bits("deadbeefdeadbeef")
    '1101111010101101101111101110111111011110101011011011111011101111'
    """
    nibbles_to_pad = 2 - (len(byte_string) % 2)
    nibbles_to_pad = (
        0 if len(byte_string) != 0 and nibbles_to_pad == 2 else nibbles_to_pad
    )
    padded_byte_string = byte_string + "".zfill(nibbles_to_pad)

    return "".join(
        f"{byte:08b}" for byte in bytearray.fromhex(padded_byte_string)
    )


def _from_bits(bit_string):
    """
    >>> _from_bits("invalid literal")
    Traceback (most recent call last):
    ValueError: invalid literal for int() with base 2: 'invalid literal0'
    >>> _from_bits("")
    '00'
    >>> _from_bits("0")
    '00'
    >>> _from_bits("01")
    '40'
    >>> _from_bits("110")
    'c0'
    >>> _from_bits("1010")
    'a0'
    >>> _from_bits("10110")
    'b0'
    >>> _from_bits("00000010")
    '02'
    >>> _from_bits("00000001")
    '01'
    >>> _from_bits("11011110101011011011111011101111")
    'deadbeef'
    >>> _from_bits("1101111010101101101111101110111111011110101011011011111011101111")
    'deadbeefdeadbeef'
    """
    bits_to_pad = 8 - (len(bit_string) % 8)
    bits_to_pad = (
        0 if len(bit_string) != 0 and bits_to_pad == 8 else bits_to_pad
    )
    padded_bit_string = bit_string + "".zfill(bits_to_pad)

    return (
        int(padded_bit_string, 2)
        .to_bytes((len(padded_bit_string) + 7) // 8, "big")
        .hex()
    )


def _parse_args():
    argparser = argparse.ArgumentParser()

    to_from_group = argparser.add_mutually_exclusive_group()

    to_from_group.add_argument(
        "-f", "--from", action="store_true", dest="_from"
    )
    to_from_group.add_argument("-t", "--to", action="store_true")

    if _HAS_ARGCOMPLETE:
        argcomplete.autocomplete(argparser)

    return argparser.parse_args()


def main():
    args = _parse_args()

    stdin = sys.stdin.read().strip().replace(" ", "")

    if args.to or stdin.startswith("0x"):
        print(f"0b{_to_bits(stdin.removeprefix('0x'))}")
    elif args._from or stdin.startswith("0b") or not args.to:
        print(f"0x{_from_bits(stdin.removeprefix('0b'))}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
