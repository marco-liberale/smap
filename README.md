# SMAP (Silent Map) Documentation

SMAP (Silent Map) is a port scanning tool that operates through the Tor network, allowing for anonymous scanning activities. It is designed to scan a range of ports on a target system to determine if they are open or closed.

## Installation Guide

### Prerequisites

Before installing SMAP, ensure you have the following prerequisites installed on your system:

- Python 3.x
- Git
- Tor ([with Control and socks port enabled](#enabling-control-port-and-socks-port-in-tor))

### Cloning the Repository

To get started with SMAP, you'll first need to clone its repository from GitHub. Open your terminal and execute the following command:

```bash
git clone https://github.com/marco-liberale/smap.git
```

### Setting Up the Environment (Debian/Ubuntu)

After cloning the repository, navigate to the SMAP directory:

```bash
cd smap
```

Next, you'll need to install the required Python libraries. SMAP's dependencies are listed in a `requirements.txt` file, which can be installed using `pip`. Run the following command to install them:

```bash
pip install -r requirements.txt
```
### Setting Up the Environment (Arch)

For fellow Arch users you can ether create a python virtual environment or do the following:

After cloning the repository, navigate to the SMAP directory:

```bash
cd smap
```
Next, you'll need to install the required Python libraries. In arch you will need to run the following command to install the dependencies globally:

```bash
sudo pacman -S python-stem python-colorama python-pysocks
```

## Usage

Once you have SMAP installed, you can begin using it to scan ports on your target system.

### Command-Line Arguments

SMAP accepts several command-line arguments to customize its behavior:

- `-t` or `--target`: Specify the target IP address or hostname.
- `-p` or `--port`: Define the target port or range of ports to scan (default is 1-1000).
- `-o` or `--timeout`: Set the timeout value in seconds for each port scan attempt (default is 3 seconds).
- `-v` or `--verbose`: Enable verbose output, showing detailed process information.

### Running SMAP

To run SMAP, use the following command structure:

```bash
python smap.py --target <target_ip> --port <target_port> --timeout <timeout> --verbose
```

Replace `<target_ip>`, `<target_port>`, and `<timeout>` with your desired values. The `--verbose` flag is optional.

## Example

Here's an example of how to run SMAP to scan ports 1 through 100 on a target system with IP address `192.168.1.1`:

```bash
python smap.py --target 192.168.1.1 --port 1-100 --verbose
```

### Enabling Control Port and SOCKS Port in Tor



To enable both the Control Port and SOCKS Port in Tor, you'll need to edit the Tor configuration file (`torrc`). Here's a step-by-step guide on how to do it:

1. **Locate the Tor Configuration File**

   The `torrc` file is usually found in `/etc/tor/` on Unix systems or in the Tor installation directory on Windows.

2. **Edit the Configuration File**

   Open the `torrc` file with a text editor. You might need administrative privileges to edit this file.

3. **Set the ControlPort Option**

   Look for the line that specifies `ControlPort`. If it's not there, you can add it. Set the `ControlPort` to the port number that you want Tor to listen on for control connections.
   
   ```
   ControlPort 9051
   ```

   This line tells Tor to accept control connections on port 9051.

4. **Configure the SOCKS Port**

   Similarly, find the `SOCKSPort` line or add it if it's missing. By default, Tor uses port 9050 for SOCKS connections. Specify the port like this:

   ```
   SOCKSPort 9050
   ```

   This line configures Tor to listen for SOCKS connections on port 9050.

5. **Save the Configuration File**

   After making the necessary changes to both `ControlPort` and `SOCKSPort`, save and close the `torrc` file.

6. **Restart Tor**

   For the changes to take effect, you need to restart the Tor service. On Unix systems, this can typically be done with a command like:

   ```
   sudo systemctl restart tor 
   ```

## Legal Disclamer
By using the repository, you acknowledge that you have read this [Disclaimer](https://github.com/marco-liberale/smap/blob/main/legal_disclamer.pdf) and agree to be bound by the terms hereof.
If you do not agree to abide by the above, please do not use the repository.

## Contributing

Contributions to SMAP are welcome. Please feel free to fork the repository, make changes, and submit pull requests.

## License

SMAP is released under the MIT License. For more details, see the `LICENSE` file in the repository.

## Support

For support or to report issues, please file an issue on the GitHub repository issue tracker.

---

This documentation provides a basic overview of installing and using SMAP. For more detailed information, refer to the source code and comments within the `smap.py` script.

enjoy :)
