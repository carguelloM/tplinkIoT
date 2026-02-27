#!/usr/bin/env python3

'''
This code is based on https://github.com/softScheck/tplink-smartplug
This is a simple script that returns the ip address of devices responding to the TP-LINK SMARTHOME discovery process
'''
import argparse
import socket
import psutil


def arg_parser():
    ## i just learned that python allows functions inside functions
    addrs = psutil.net_if_addrs()

    def valid_iface(iface_target: str): 
        addr_list = addrs.get(iface_target)
        if not addr_list:
            parser.error("Interface does not exist")

        for addr in addr_list:
            if addr.family.name == "AF_INET":
                return addr.address
                

    parser = argparse.ArgumentParser(usage="%(prog)s -i <if_name>")
    parser.add_argument("-i", "--interface", required=True, type=valid_iface)
    parser.add_argument("-t", "--timeout", default=1, required=False)
    return parser.parse_args()

def encrypt(string: str) -> bytes:
    """Encryption of TP-Link Smart Home Protocol.
    XOR Autokey Cipher with starting key = 171.
    """
    key = 171
    result = b""
    for i in string:
        a = key ^ ord(i)
        key = a
        result += bytes([a])
    return result


def main():
    myargs = arg_parser()
    print(f"Interface IPv4 : {myargs.interface}")
    cmd = '{"system":{"get_sysinfo":{}}}'
    ## send discovery command
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(int(myargs.timeout))
        sock.bind((myargs.interface, 0)) 
        sock.sendto(encrypt(cmd), ('255.255.255.255',9999)) ## broadcast and default port for tp link discovery
        responses = []
        while True:
            try:
                data, addr = sock.recvfrom(2048)
                responses.append((data,addr))
            except socket.timeout:
                break
        for data, addr in responses:
            print(f"Data from {addr[0]}")
    except OSError as e:
        print(e)


if __name__ == "__main__":
    main()
