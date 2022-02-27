import socket
import threading
import time

import termcolor
from IPy import IP

socket.setdefaulttimeout(.5)


def scan(target):
    global t
    convert_ip = check_ip(target)  # check for dns or ip and return ip
    print('\n' + '[+] Scanning Target ' + termcolor.colored(str(convert_ip), 'red'))
    for port in range(1, 500):
        t = threading.Thread(target=scan_port, args=(convert_ip, port,), daemon=True)
        t.start()
        time.sleep(.05)
        # scan_port(convert_ip, port) if without threading


def check_ip(ipaddress):
    try:
        IP(ipaddress)
        return ipaddress
    except ValueError:
        return socket.gethostbyname(ipaddress)


def get_banner(s):
    return s.recv(1024)


def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.settimeout(.5)
        sock.connect((ipaddress, port))
        try:
            banner = get_banner(sock)
            print(termcolor.colored("[+]Open Port " + str(port) + " : " + str(banner.decode().strip('\n'), 'green')))
        except:
            print(termcolor.colored("[+]Open Port " + str(port), 'green'))
    except:
        pass


if __name__ == '__main__':
    print(termcolor.colored('Program to scan ports from 1-500 and try to grab banner if any', 'blue'))
    targets = input("[+] Enter Target/s to start: (split multiple targets with ,):")
    start_time = time.time()
    if ',' in targets:
        for ip_add in targets.split(','):
            scan(ip_add.strip(' '))

    else:
        scan(targets)
    print('Finished scanning in ', termcolor.colored('%f' % (time.time() - start_time), 'blue'))
