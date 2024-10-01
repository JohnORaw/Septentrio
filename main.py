#!/usr/bin/env python

import serial
import struct
from septentrio_constants import SBF_SYNC_PATTERN

from modules.crc import calculate_crc

def parse(binary_data):
    # All data little endian

    # Check if the data starts with the sync pattern
    if binary_data[:2] != SBF_SYNC_PATTERN:
        print("Sync pattern not found. Invalid SBF message.")
        return None
    print("Found a valid SBF_SYNC")

    crc = struct.unpack_from('<H', binary_data, 2)[0]  # Little-endian
    print(f"2 byte CRC from packet: {crc}")

    block_id = struct.unpack_from('<H', binary_data, 4)[0]  # Little-endian
    block_id = block_id & 0xFFF
    print(f"2 byte block ID: {block_id}")

    block_length = struct.unpack_from('<H', binary_data, 6)[0]  # Little-endian
    if block_length % 4 == 0:
        print(f"2 byte block length: {block_length}")
    else:
        print("Bad block length, cannot process this block")
        return None
    
    TOW = struct.unpack_from('<I', binary_data, 8)[0]  # Little-endian
    print(f"4 byte TOW: {TOW}")
    
    WNc = struct.unpack_from('<H', binary_data, 12)[0]  # Little-endian
    print(f"2 byte GPS week number: {WNc}")
    
       
def read_serial_data(port='/dev/ttyAMA0', baudrate=115200, timeout=1):
    try:
        # Open the serial port with the specified parameters
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            print(f"Listening on {port} with baudrate {baudrate}. Press Ctrl+C to stop.")

            while True:  # Infinite loop to continuously read data
                # Read binary data from the serial port
                binary_data = ser.read(100)  # Adjust the number of bytes as needed

                if binary_data:
                    # Display the received binary data
                    #print("Binary Data (raw):", binary_data)
                    print("Binary Data (hex):", binary_data.hex())  # Display in hex format
                    #print("Binary Data (bytes):", list(binary_data))  # Display as a list of byte values
                    parse(binary_data)

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        read_serial_data('COM9', baudrate=115200, timeout=1)
    except KeyboardInterrupt:
        print("\nSerial reading stopped by user.")
