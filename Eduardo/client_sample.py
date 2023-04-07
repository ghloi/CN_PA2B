import socket
import time

WINDOW_SIZE = 4
PACKET_SIZE = 1024

def send_packets(socket, address, packets):
    seq_num = 0
    while seq_num < len(packets):
        # send packets in the window
        for i in range(seq_num, min(seq_num + WINDOW_SIZE, len(packets))):
            packet = str(seq_num).zfill(4).encode('utf-8') + packets[i]
            socket.sendto(packet, address)
            print(f'Sent packet {seq_num}: {packets[i]}')
            seq_num += 1

        # wait for ACKs for the packets in the window
        start_time = time.time()
        while True:
            socket.settimeout(0.1)
            try:
                ack_packet, ack_address = socket.recvfrom(PACKET_SIZE)
                ack_seq_num = int(ack_packet.decode('utf-8'))
                if ack_seq_num >= seq_num - WINDOW_SIZE and ack_seq_num < seq_num:
                    print(f'Received ACK {ack_seq_num}')
                    break
                else:
                    print(f'Received out-of-order ACK {ack_seq_num}')
            except socket.timeout:
                print('Timeout waiting for ACKs')
                seq_num -= WINDOW_SIZE
                break

def receive_packets(socket, address):
    expected_seq_num = 0
    received_packets = []
    while True:
        packet = str(expected_seq_num).zfill(4).encode('utf-8')
        socket.sendto(packet, address)
        print(f'Sent request for packet {expected_seq_num}')
        try:
            packet, sender_address = socket.recvfrom(PACKET_SIZE)
            seq_num = int(packet[:4].decode('utf-8'))
            if seq_num == expected_seq_num:
                print(f'Received packet {seq_num}: {packet[4:]}')
                received_packets.append(packet[4:])
                expected_seq_num += 1
            else:
                print(f'Received out-of-order packet {seq_num}')
        except socket.timeout:
            print('Timeout waiting for packet')
            break
        if len(received_packets) == WINDOW_SIZE:
            break
    return received_packets

def main():
    # create a UDP socket and connect it to the server address
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)
    client_socket.connect(server_address)

    # send packets and receive ACKs
    with open('data.txt', 'rb') as file:
        data = file.read()
    packets = [data[i:i+PACKET_SIZE] for i in range(0, len(data), PACKET_SIZE)]
    send_packets(client_socket, server_address, packets)

    # receive packets
    received_packets = receive_packets(client_socket, server_address)

    # close the socket
    client_socket.close()

if __name__ == '__main__':
    main()
