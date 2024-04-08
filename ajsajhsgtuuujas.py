import serial
import time


ser = serial.Serial('COM20', 2400)  
time.sleep(2)  


with open('Data.txt', 'rb') as file:
    data_to_send = file.read()
    start_time_transmission = time.time()
    total_bytes_sent = 0
    print("Transmission from PC to MCU Started\n")
    for byte in data_to_send:
        ser.write(bytes([byte]))
        total_bytes_sent += 1
        elapsed_time_transmission = time.time() - start_time_transmission


        if elapsed_time_transmission > 0:
            transmission_speed = total_bytes_sent * 8 / elapsed_time_transmission
            print("Transmission Speed: {:.2f} bits/second".format(transmission_speed))
        else:
            continue

    print("\nAll data is transmitted from PC to MCU\n")


    ser.write(b"0\n1005\n")


    received_string = ""
    start_time = time.time()  
    while True:
        received_byte = ser.read()
        if not received_byte:
            continue
        received_char = received_byte.decode('utf-8', errors='replace')

        end_time = time.time()
        if received_char == '\n':
            break
        received_string += received_char
        if "currently" in received_string:
            break
        if end_time > start_time:
            speed = 8.0 / (end_time - start_time)
            print("Received character:", received_char.strip())  
            print("Reception speed:", speed)
        else:
            print("Received character:", received_char.strip())  
            print("Reception speed: Not available (elapsed time is zero)")
        start_time = end_time


    print("\nReceived string from MCU:", received_string)


ser.close()
