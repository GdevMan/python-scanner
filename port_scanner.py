import socket
import argparse
import logging

parser = argparse.ArgumentParser(description="Simple port scanner")
parser.add_argument("--target", required=True, help="Target IP")
parser.add_argument("--start", type=int, default=20, help="Starting port")
parser.add_argument("--end", type=int, default=1000, help="End port")
parser.add_argument("--timeout", type=float, default=0.3, help="timeout in seconds")
parser.add_argument("--debug", action="store_true", help="enable debug")

args = parser.parse_args()
open_ports = []
if args.debug:
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.WARNING)

ip = args.target
logging.info(f"Target selected: {ip}")
ports = range(args.start, args.end + 1)

for p in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)
    try:
        s.connect((ip, p))
    except (ConnectionRefusedError, OSError, socket.timeout) as e:
        logging.info(f"Error : {e}")
        pass
    else:
        try:
            test_banner = s.recv(2000).decode(errors="ignore").strip()
            print(f"Port {p} is open, test banner : {test_banner}")
            open_ports.append(p)
        except:
            print(f"Port {p} is open")
            open_ports.append(p)
    finally:
        s.close()
if args.debug:
    print(open_ports)