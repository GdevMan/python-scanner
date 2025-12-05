import socket, argparse, logging, threading
from colorama import *
init(autoreset=True)

vuln = [
    "OpenSSH_2.3.0",
    "OpenSSH_7.2p2",
    "OpenSSH_3.6.1p2"
]

parser = argparse.ArgumentParser(description="Simple port scanner")
parser.add_argument("-t", "--target", required=True, help="Target IP")
parser.add_argument("-s", "--start", type=int, default=20, help="Starting port")
parser.add_argument("-e", "--end", type=int, default=1000, help="End port")
parser.add_argument("-T", "--timeout", type=float, default=0.3, help="timeout in seconds")
parser.add_argument("-d", "--debug", action="store_true", help="enable debug")

args = parser.parse_args()

logging.basicConfig(level=logging.INFO if args.debug else logging.WARNING)

def scan_port(p):
    http_banner = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)

    try:
        s.connect((args.target, p))
    except Exception as e:
        logging.info(Fore.RED + f"{p}/tcp closed or filtered: {e}")
        return

    try:
        if p == 80:
            request = f"GET / HTTP/1.1\r\nHost: {args.target}\r\n\r\n"
            s.send(request.encode())
            http_banner = s.recv(2000).decode(errors="ignore").strip()

        banner = s.recv(2000).decode(errors="ignore").strip()
        if banner == "":
            banner = http_banner

        print(Fore.GREEN + f"Port {p} is open, banner: {banner}")

        if any(v in banner for v in vuln):
            print(Fore.RED + "!!! Vulnerable version detected !!!")

    except:
        print(f"Port {p} is open (no banner)")
    finally:
        s.close()


threads = []

for p in range(args.start, args.end + 1):
    t = threading.Thread(target=scan_port, args=(p,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
