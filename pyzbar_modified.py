from ctypes import string_at

from pyzbar import pyzbar
from pyzbar.pyzbar import _RANGEFN, Decoded
from pyzbar.locations import Point, bounding_box, convex_hull
from pyzbar.wrapper import (zbar_symbol_get_data, ZBarSymbol, zbar_symbol_get_loc_x, zbar_symbol_get_loc_y,
                            zbar_symbol_get_loc_size)


def _decode_symbols_modified(symbols):
    """Generator of decoded symbol information.

    Args:
        symbols: iterable of instances of `POINTER(zbar_symbol)`

    Yields:
        Decoded: decoded symbol
    """
    for symbol in symbols:
        data = string_at(zbar_symbol_get_data(symbol))
        # The 'type' int in a value in the ZBarSymbol enumeration
        symbol_type = ZBarSymbol(symbol.contents.type).name
        polygon = convex_hull(
            (
                zbar_symbol_get_loc_x(symbol, index),
                zbar_symbol_get_loc_y(symbol, index)
            )
            for index in _RANGEFN(zbar_symbol_get_loc_size(symbol))
        )

        # since 'polygon' is very misleading if one wants to detect the QR/bar
        # code position in order no matter how they appear in the scene
        polygon_upright = list(map(Point._make, (
            (
            zbar_symbol_get_loc_x(symbol, index),
            zbar_symbol_get_loc_y(symbol, index)
            )
        for index in _RANGEFN(zbar_symbol_get_loc_size(symbol))
        )))

        yield Decoded(
            data=data,
            type=symbol_type,
            rect=bounding_box(polygon),
            polygon=polygon_upright
        )


pyzbar._decode_symbols = _decode_symbols_modified
