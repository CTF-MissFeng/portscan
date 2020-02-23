import asyncio
import argparse
import time

async def PortScan(ip, port):
    try:
        reader, writer = await asyncio.open_connection(host=ip, port=port)
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        pass
    else:
        print(f'{ip} {port}')

async def action(ip, threads):
    ports = [PortScan(ip, port) for port in range(1, 65535)]
    n = int(threads)
    tasks = [ports[i:i + n] for i in range(0, len(ports), n)]
    for task in tasks:
        await asyncio.wait(task, timeout=5)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=('asyncio port scan'))
    parser.add_argument('-i', '--ip', help='待扫描的IP')
    parser.add_argument('-t', '--threads', type=int, help='扫描协程数，不能大于系统最大打开文件数')
    args = parser.parse_args()
    if args.ip and args.threads:
        start = time.time()
        asyncio.run(action(args.ip, args.threads))
        print(time.time()-start)

if __name__ == '__main__':
    main()