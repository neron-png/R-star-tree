
###########
# Loading #
###########
def z_order(*pointCoords, maxBitLen = None) -> int:
    """Computes the z-order index from coordinates in n dimensions

    :param (x, y, z ...): n-dimensional integer coordinates of point
    :param maxBitLen: None | Default, maximum size of outgoing z-number
    :return: number. the distance from (0, 0) to the point (x, y)
    """
    n = len(pointCoords)
    z = 0
    maxBitLen = max([coord.bit_length() for coord in pointCoords])*n
    # maxBitLen = sum([coord.bit_length() for coord in pointCoords])

    for i in range(0, maxBitLen // n):
        for j in range(n):
            # Shifting each dimension coordinate `i` places and then giving it an offset
            z += ((pointCoords[j] >> i) & 1) << ((i * n) + j)

    return z

