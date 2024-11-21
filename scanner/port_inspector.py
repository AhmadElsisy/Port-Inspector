import pyfiglet
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from utils.logger import Logger
from utils.validator import Validator
from reports.report_writer import ReportWriter



# CLI aesthetics
ascii_banner = pyfiglet.figlet_format("PORT INSPECTOR")
print(ascii_banner)
print("_" * 40)

# Define port scanning class
class PortInspector:
    def __init__(self):
        self.open_ports= []
        self.scan_results = {}
        self.default_timeout = 1.0
        self.logger = Logger(log_level="INFO",
                    log_file="logs/port_inspector.log",
                    log_to_console=True)
        self.validator = Validator()
        self.report_writer = ReportWriter()

    # Define a function to scan the port at the target and return result
    def scan_single_port(self, target: str, port: int, timeout: float = 1.0) -> tuple:

        try:
            # Create a socket to initiate the connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                # Connection attempt
                result = sock.connect_ex((target, port))
                if result == 0:
                    # Port is open -- identify the service
                    try:
                        service_name = socket.getservbyport(port)
                    except(OSError, socket.error):
                        service_name = "unknown"
                    return port, True, service_name
                return port, False, None
        except socket.gaierror: # For DNS issues
            print(f"Hostname could not be resolved: {target}")
            return port, False, None
        except socket.error as e: # For any other errors
            print(f"Could not connect to {target}: {e}")
            return port, False, None

 # Define a function to scan range of ports at the target and return result
    def scan_range(self, target: str, start_port: int = 1, end_port = 1024) -> dict:
        if not self.validator.validate_target(target):
            self.logger.error(f"Invalid target: {target}")
            return None
        if not self.validator.validate_ports(start_port, end_port):
            self.logger.error(f"Invalid port range: {start_port}-{end_port}")
            return None
        try:
        # Resolve hostname
            target_ip = socket.gethostbyname(target)
            print(f"\nStart scanning on host: {target} ({target_ip})")
            print(f"port range {start_port}-{end_port}")

            scan_start_time = datetime.now()
            self.open_ports = []  # Reset open ports list
            ports_scanned = 0

            total_ports = end_port - start_port + 1

            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(self.scan_single_port, target_ip, port) for port in range(start_port, end_port + 1)]

            # Show the scanning progress
                for future in futures:
                    port, is_open, service = future.result()
                    ports_scanned += 1
                    if ports_scanned % 250 == 0:
                        print(f"Progress: {ports_scanned}/{total_ports} scanned.")

                if is_open:
                    self.open_ports.append({
                        "port": port,
                        "service": service
                    })
                    print(f"Found open port {port}/TCP - service: {service}")
         # Calculate scanning duration
            scan_end_time = datetime.now()
            duration = (scan_end_time - scan_start_time).total_seconds()

        # Prepare results
            self.scan_results = {
                "target": target,
                "target_ip": target_ip,
                "start_time": scan_start_time,
                "end_time": scan_end_time,
                "duration": duration,
                "ports_scanned": total_ports,
                "open_ports": self.open_ports
            }

        # Print scan summary
            print(f"\nScan completed in {duration: .2f} seconds.")
            print(f"Found {len(self.open_ports)} open ports.")

            # Add logging
            self.logger.info(f"Scan started for {target}")

            # After scan completes
            self.report_writer.write_report(self.scan_results)

            return self.scan_results

        except socket.gaierror:
            print(f"Hostname {target} can't be reolved.")
            return None
        except KeyboardInterrupt:
            print("\nScan interupted by user")
            return None
        except Exception as e:
            print(f"An error occured: {str(e)}")
            return None


def main():
    scanner = PortInspector()
    validator = Validator()

    # example scan

    while True:
        target = input("Enter target host (e.g., example.com): ")
        is_valid, error = validator.validate_target(target)
        if is_valid:
            break
        print(f"Error: {error}")

    while True:
        try:
            start_port = int(input("Enter start port (1-65535): "))
            end_port = int(input("Enter end port (1-65535): "))
            is_valid, error = validator.validate_ports(start_port, end_port)
            if is_valid:
                break
            print(f"Error: {error}")
        except ValueError:
            print("Error: Please enter valid numbers")


    results = scanner.scan_range(target, start_port, end_port)

    if results and results['open_ports']:
        print("\nDetailed Results: ")
        print("-" * 40)
        for port_info in results ['open_ports']:
            print(f"Port: {port_info['port']} / TCP - service:{port_info['service']}")

if __name__ == "__main__":
    main()





