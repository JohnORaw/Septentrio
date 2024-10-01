import serial
import struct
import septentrio_constants

from modules.crc import calculate_crc

def parse(binary_data):

    # Check if the data starts with the sync pattern
    if binary_data[:2] != SBF_SYNC_PATTERN:
        print("Sync pattern not found. Invalid SBF message.")
        return None
    print("Found a valid SBF_SYNC")

    # Extract message length (16-bit unsigned integer)
    message_length = struct.unpack_from('<H', binary_data, 2)[0]  # Little-endian
    print(f"Message Length: {message_length} bytes")

    # Extract message ID (16-bit unsigned integer)
    message_id = struct.unpack_from('<H', binary_data, 4)[0]
    print(f"Message ID: {message_id}")

    # Extract time tag (32-bit unsigned integer)
    time_tag = struct.unpack_from('<I', binary_data, 6)[0]
    print(f"Time Tag: {time_tag}")

 # Extract payload
    payload_start = 10
    payload_end = payload_start + (message_length - 10)  # Subtract header length
    payload = binary_data[payload_start:payload_end]
    print(f"Payload (raw): {payload}")

    # Validate CRC (16-bit at the end of the message)
    crc_received = binary_data[-2:]
    crc_received_int = int.from_bytes(crc_received, "big")
    print("CRC", crc_received_int)
    crc_calculated = calculate_crc(binary_data[:message_length - 2])
    print(f"CRC Received: {crc_received}, CRC Calculated: {crc_calculated}")

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
                    print("Binary Data (raw):", binary_data)
                    print("Binary Data (hex):", binary_data.hex())  # Display in hex format
                    print("Binary Data (bytes):", list(binary_data))  # Display as a list of byte values
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
