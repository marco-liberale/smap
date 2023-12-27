# Human Made Code
# AI Generated Comments
# Import necessary libraries
import socket
import socks
import optparse
import colorama
import time
from stem import Signal
from stem.control import Controller

# Function to check if an IP address is valid
def is_valid_ip(ip):
    # Check if it's a valid IP
    try:
        socket.inet_aton(input_string)
        return "Valid IP"
    except socket.error:
        # If it's not a valid IP, check if it's a valid domain
        pattern = "^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$"
        if re.match(pattern, input_string):
            return "Valid Domain"
    return "Invalid IP or Domain"


# Function to check if a port number is valid
def is_valid_port(port):
    return 0 <= port <= 65535  # Port numbers range from 0 to 65535

# Function to scan a port through the Tor network
def scan_port_through_tor(target, port, controller, timeout):
    # Set up a SOCKS5 proxy at localhost:9050 (default Tor settings)
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr='127.0.0.1', port=9050)
    sock = socks.socksocket()  # Create a new socket using the SOCKS proxy
    sock.settimeout(timeout=timeout)  # Set the timeout for the socket
    try:
        sock.connect((target, port))  # Try to connect to the target on the specified port
        return True
    except socket.timeout:
        return False
    except socket.error as e:
        return False
    finally:
        sock.close()  # Always close the socket

# Function to get a new Tor identity
def get_new_tor_identity(controller):
    controller.signal(Signal.NEWNYM)  # Send the NEWNYM signal to Tor

# Main function
def main():
    # Set up command-line argument parsing
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip")  # Target IP address
    parser.add_option("-p", "--port", dest="target_port", default="1-1000")  # Target port range
    parser.add_option("-o", "--timeout", dest="timeout", default=3, type="int")  # Timeout for each port scan
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)  # Verbose mode
    (options, args) = parser.parse_args()

    # Get the target IP address
    if options.target_ip is None:
        ip = input("Enter the Domain or IP Address of the Target: ")
    else:
        ip = options.target_ip

    # Check if the IP address is valid
    if not is_valid_ip(ip):
        print("Invalid IP address.")
        return

    # Parse the port range(s)
    ports = options.target_port.replace(" ", "").split(",")
    port_range = []
    for p in ports:
        if "-" in p:
            start, end = list(map(int, p.split("-")))
            port_range.extend(list(range(start, end + 1)))
        elif p:
            port_range.append(int(p))

    # Check if the port numbers are valid
    for port in port_range:
        if not is_valid_port(port):
            print(f"Invalid port: {port}")
            return

    # Initialize the results dictionary
    results = {}
    open = {}

    # Try to connect to the Tor service
    try:
        with Controller.from_port(port=9051) as controller:  # Connect to the Tor controller
            controller.authenticate()  # Authenticate with the Tor controller
            for port in port_range:  # For each port in the range
                try:
                    if options.verbose:  # If verbose mode is on
                        print(colorama.Fore.LIGHTYELLOW_EX + f"Scanning port {port}..." + colorama.Style.RESET_ALL)
                    get_new_tor_identity(controller)  # Get a new Tor identity
                    status = scan_port_through_tor(ip, port, controller, options.timeout)  # Scan the port
                    if status:  # If the port is open
                        print(colorama.Fore.LIGHTGREEN_EX + f"Port {port} is open" + colorama.Style.RESET_ALL)
                    else:  # If the port is closed
                        if options.verbose:  # If verbose mode is on
                            print(colorama.Fore.LIGHTRED_EX + f"Port {port} is closed" + colorama.Style.RESET_ALL)
                    results[port] = 'Open' if status else 'Closed'  # Add the result to the results dictionary
                    if status:  # If the port is open
                        open[port] = "Open"
                    time.sleep(1)  # Wait for a second before the next scan
                except KeyboardInterrupt:  # If the user presses Ctrl+C
                    print("Stopping...")
                    return
    except stem.SocketError as e:  # If there's an error connecting to the Tor service
        print(f"Error connecting to Tor service: {e}")
        return
    except KeyboardInterrupt:  # If the user presses Ctrl+C
        print("Stopping...")
        return

    print(f"Thanks for using Silent Map {colorama.Fore.LIGHTGREEN_EX}:)" + colorama.Style.RESET_ALL)

# If the script is being run directly (not imported as a module), call the main function
if __name__ == '__main__':
    main()
