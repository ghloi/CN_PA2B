import socket
import time

WINDOW_SIZE = 4
PACKET_SIZE = 1024

def send_packets(socket, address, packets):
    seq_num = 0
    while seq_num < len(packets):
        # send packets in the window
        for i in range(seq_num, min(seq_num + WINDOW_SIZE, len(packets))):
            packet = packets[i]
            socket.sendto(packet, address)
            print(f'Sent packet {i}: {packet}')

        # wait for ACKs for the packets in the window
        start_time = time.time()
        while True:
            socket.settimeout(0.1)
            try:
                ack_packet, ack_address = socket.recvfrom(PACKET_SIZE)
                ack_seq_num = int(ack_packet.decode('utf-8'))
                if ack_seq_num == seq_num:
                    print(f'Received ACK {ack_seq_num}')
                    seq_num += 1
                    break
                else:
                    print(f'Received out-of-order ACK {ack_seq_num}')
            except socket.timeout:
                print('Timeout waiting for ACKs')
                break

def receive_packets(socket, address):
    expected_seq_num = 0
    received_packets = []
    while True:
        packet, sender_address = socket.recvfrom(PACKET_SIZE)
        seq_num = int(packet[:4].decode('utf-8'))
        if seq_num == expected_seq_num:
            print(f'Received packet {seq_num}: {packet[4:]}')
            received_packets.append(packet[4:])
            expected_seq_num += 1
            ack_packet = str(seq_num).encode('utf-8')
            socket.sendto(ack_packet, sender_address)
            print(f'Sent ACK {seq_num}')
        else:
            print(f'Received out-of-order packet {seq_num}')
        if len(received_packets) == WINDOW_SIZE:
            break
    return received_packets

def main():
    # create a UDP socket and bind it to a local address
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)
    server_socket.bind(server_address)

    # receive packets
    received_packets = receive_packets(server_socket, server_address)

    # send ACKs and receive packets
    send_packets(server_socket, server_address, received_packets)

    # close the socket
    server_socket.close()

if __name__ == '__main__':
    main()
