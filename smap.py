# Importing necessary libraries
import socket
import socks
import optparse
import colorama
import re
import time
from stem import Signal, SocketError
from stem.control import Controller

# Function to check if the given IP address is valid
def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        pattern = "^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$"
        if re.match(pattern, ip):
            return True
    return False

# Function to check if the given port number is valid
def is_valid_port(port):
    return 0 <= port <= 65535

# Function to scan a specific port through Tor
def scan_port_through_tor(target, port, controller, timeout):
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr='127.0.0.1', port=9050)
    sock = socks.socksocket()
    sock.settimeout(timeout=timeout)
    try:
        sock.connect((target, port))
        return True
    except socket.timeout:
        return False
    except socket.error as e:
        return False
    finally:
        sock.close()

# Function to get a new Tor identity
def get_new_tor_identity(controller):
    controller.signal(Signal.NEWNYM)

# Main function
def main():
    try:
        print("Made By Marco Liberale")
        parser = optparse.OptionParser()
        parser.add_option("-t", "--target", dest="target_ip", help="Specify the target IP address or domain name.")
        parser.add_option("-p", "--port", dest="target_port", default="1-1000",
                          help="Specify the target port or range of ports. Default is 1-1000.")
        parser.add_option("-o", "--timeout", dest="timeout", default=3, type="int",
                          help="Specify the timeout for each port scan. Default is 3 seconds. (Anything below 3 seconds will cause inaccurate results)")
        parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,
                          help="Enable verbose mode.")

        (options, args) = parser.parse_args()

        if options.target_ip is None:
            ip = input("Enter the Domain or IP Address of the Target: ")
        else:
            ip = options.target_ip

        if not is_valid_ip(ip):
            print("Invalid IP address.")
            return

        ports = options.target_port.replace(" ", "").split(",")
        port_range = []
        parser = optparse.OptionParser()
        parser.add_option("-t", "--target", dest="target_ip")
        parser.add_option("-p", "--port", dest="target_port", default="1-1000")
        parser.add_option("-o", "--timeout", dest="timeout", default=3, type="int")
        parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)
        for p in ports:
            if "-" in p:
                start, end = list(map(int, p.split("-")))
                port_range.extend(list(range(start, end + 1)))
            elif p:
                port_range.append(int(p))

        for port in port_range:
            if not is_valid_port(port):
                print(f"Invalid port: {port}")
                return

        results = {}
        open = {}

        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                for port in port_range:
                    try:
                        if options.verbose:
                            print(colorama.Fore.LIGHTYELLOW_EX + f"Scanning port {port}..." + colorama.Style.RESET_ALL)
                        get_new_tor_identity(controller)
                        status = scan_port_through_tor(ip, port, controller, options.timeout)
                        if status:
                            print(colorama.Fore.LIGHTGREEN_EX + f"Port {port} is open" + colorama.Style.RESET_ALL)
                        else:
                            if options.verbose:
                                print(colorama.Fore.LIGHTRED_EX + f"Port {port} is closed" + colorama.Style.RESET_ALL)
                        results[port] = 'Open' if status else 'Closed'
                        if status:
                            open[port] = "Open"
                        time.sleep(1)
                    except KeyboardInterrupt:
                        print("Stopping...")
                        return
                    except SocketError as e:
                        print(f"Error connecting to Tor service: {e}")
                        return
        except KeyboardInterrupt:
            print("Stopping...")
            return

        print(f"Thanks for using Silent Map {colorama.Fore.LIGHTGREEN_EX}:)" + colorama.Style.RESET_ALL + "\nBlog: https://uwu.blog\nEmail: marco@marcoliberale.com")
    except KeyboardInterrupt:
        print("\nStopping...")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")


# Running the main function
if __name__ == '__main__':
    main()
