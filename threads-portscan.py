import concurrent.futures
import socket
import argparse
import time

def portscan(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f'{ip} {port}')
    except (socket.timeout, ConnectionResetError, OSError):
        pass

def main(ip, threads):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            result = {executor.submit(portscan, ip, port): port for port in range(1, 65535)}
            for future in concurrent.futures.as_completed(result, timeout=5):
                future.result()
    except:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=('threads port scan'))
    parser.add_argument('-i', '--ip', help='待扫描的IP')
    parser.add_argument('-t', '--threads', type=int, help='扫描线程数，不能大于系统最大打开文件数')
    args = parser.parse_args()
    if args.ip and args.threads:
        start = time.time()
        main(args.ip, args.threads)
        print(time.time() - start)