
def calculate_crc(data):
    """Calculates the 16-bit CRC for SBF messages."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0x8408  # CRC-16-CCITT
            else:
                crc >>= 1
    return crc & 0xFFFF
