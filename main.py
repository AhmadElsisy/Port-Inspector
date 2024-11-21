import argparse
import sys
from scanner.port_inspector import PortInspector
from utils.validator import Validator

def parse_arguments():
    """Parse CLI args
    """
    parser = argparse.ArgumentParser(
        description='Port Inspector - A simple port scanning tool.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog= '''Examples:
  python main.py -t example.com
  python main.py -t example.com -s 80 -e 443
  python main.py -t example.com --start-port 1 --end-port 1024
  python main.py -t example.com --start-port 1 --end-port 1024 --timeout 30 --threads 100


Disclaimer:
	This tool is intended for authorized use only.
    Scanning ports without the explicit permission of the target system's owner is a violation of cybersecurity laws and may result in legal consequences.
    Always ensure you have proper authorization before using this tool on any network or system.
    The developer is not responsible for any misuse or damage caused by this program.
    Use responsibly and ethically.'''
    )

    parser.add_argument(
        '-t', '--target',
        help= 'Target Host(e.g. example.com or IP address)',
        required=True
    )

    parser.add_argument(
        '-s', '--start-port',
        type=int,
        default=1,
        help='Start port number (Default: 1)'
    )

    parser.add_argument(
        '-e', '--end-port',
        type=int,
        default=1024,
        help='End port number (Default: 1024)'
    )

    parser.add_argument(
         '--timeout',
        type=int,
        default=30,
        help='Timeout value (Default: 30)'
    )

    parser.add_argument(
         '--threads',
        type=int,
        default=100,
        help='Threads count (Default: 100)'
    )

    return parser.parse_args()

def main():
    """
    Main function to run the port scanner
    """
    try:
        args = parse_arguments()

        # Initiate scanner and validator
        scanner = PortInspector()
        validator = Validator()

        # Check CLI args
        if len(sys.argv) == 1:

            while True:
                target = input("Enter the target host (e.g. example.com):")
                is_valid, error = validator.validate_target(target)
                if is_valid:
                    break
                print(f"Error: {error}")

            while True:
                try:
                    start_port = input("Enter start port (1 - 65535):")
                    end_port = input("Enter end port (1 - 65535): ")
                    is_valid, error = validator.validate_ports(start_port, end_port)
                    if is_valid:
                        break
                    print(f"Error: {error}")
                except ValueError:
                    print("Please enter a valid port number.")

            while True:
                try:
                    timeout = input("Enter timeout (1 - 30): ")
                    is_valid, error = validator.validate_timeout(timeout)
                    if is_valid:
                        break
                    print(f"Error: {error}")
                except ValueError:
                    print("Enter a valid timeout value.")

            while True:
                try:
                    thread_count = input("Enter threads count  (1 - 500): ")
                    is_valid, error = validator.validate_thread_count(thread_count)
                    if is_valid:
                        break
                    print(f"Error: {error}")
                except ValueError:
                    print("Entaer a valid threads count.")


        else:
            # Use CLI given commands
            target = args.target
            start_port = args.start_port
            end_port = args.end_port
            timeout = args.timeout
            thread_count = args.threads

            # Validate the inputs
            is_valid, error = validator.validate_target(target)
            if not is_valid:
                print(f"Error: {error}")
                return

            is_valid, error = validator.validate_ports(start_port, end_port)
            if not is_valid:
                print(f"Error: {error}")
                return

            is_valid, error = validator.validate_timeout(timeout)
            if not is_valid:
                print(f"Error: {error}")
                return

            is_valid, error = validator.validate_thread_count(thread_count)
            if not is_valid:
                print(f"Error: {error}")
                return


            # Run the scanning process
            results = scanner.scan_range(target, start_port, end_port)

            # Print detailed results if scan was successful
            if results and results['open_ports']:
                print("\nDetailed Results:")
                print("-" * 40)
            for port_info in results['open_ports']:
                print(f"Port: {port_info['port']}/TCP - Service: {port_info['service']}")

            if not results['open_ports']:
                print("No open ports were found.")


    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return

if __name__ == "__main__":
    main()

