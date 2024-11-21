import socket
import re
from typing import Tuple, Union


class Validator:
    def __init__(self):
        self.MIN_PORT = 1
        self.MAX_PORT = 65535
    
    def validate_ports(self, start_port: int, end_port: int) -> Tuple[bool, str]:
        try:
            # Convert entry to int if it's string
            start_port = int(start_port)
            end_port = int(end_port)

            # Check port range valdity
            if not (self.MIN_PORT <= start_port <= self.MAX_PORT):
                return False, f"Start port must be between {self.MIN_PORT} and {self.MAX_PORT}"
        
            if not (self.MIN_PORT <= end_port <= self.MAX_PORT):
                return False, f"End port must be between {self.MIN_PORT} and {self.MAX_PORT}"

            if start_port > end_port:
                return False, f"Start port must be equal or less than end port."
            
            return True, ""
        except ValueError:
            return False, "Port number must be an integer."

    # Validate the target
    def validate_target(self, target: str) -> Tuple[bool, str]:
        # Check for empty entries
        if not target:
            return False, "Target can't be empty."
        
        # Strip the entry hostname
        target = target.strip()

        # Check IP address
        if self.is_valid_ip(target):
            return True, ""
        
        # Check for hostname validity
        if self.is_valid_hostname(target):
            try:
                # Resolve hostname
                socket.gethostbyname(target)
                return True, ""
            # DNS error
            except socket.gaierror:
                return False, f"Hostname {target} can't be resolved."
            
        return False, f"Invalid target: {target}."
    
    # Check if the entry is valid IPv4
    def is_valid_ip(self, ip: str) -> bool:
        try:
            # Split IP address into its octets
            octets = ip.split(".")

            # Check if the entry has 4 octets
            if len(octets) != 4:
                return False

            # Validate each octet individually
            return all(0 <= int(octet) <= 255 for octet in octets)
        except(AttributeError, TypeError, ValueError):
            return False        
        
    # check hostname validity
    def is_valid_hostname(self, hostname: str) -> bool:
        # Check hostname length according to DNS specifications
        if len(hostname) > 255:
            return False

        # Check hostname regex pattern
        pattern = r'^[a-zA-Z0-9][-a-zA-Z0-9.]*[a-zA-Z0-9]$'
        if not re.match(pattern, hostname):
            return False

        # Check each label length
        for label in hostname.split("."):
            if len(label) > 63:
                return False
        return True

    # Validate the timeout
    def validate_timeout(self, timeout: Union[int, float]) -> Tuple[bool, str]:
        try:
            timeout = float(timeout)

            if timeout <= 0:
                return False, " Timeout must be between 1 and 30 seconds."

            if timeout > 30:
                return False, "Maximum timeout is 30 seconds" 
            return True, ""    

        except ValueError:
            return False, "Timeout must be a valid number."

    # Validate thread count
    def validate_thread_count(self, thread_count: int) -> Tuple[bool, str]:
        try:
            thread_count = int(thread_count)

            if thread_count < 1:
                return False, "Thread count must be at least 1."

            if thread_count > 500:
                return False, "Thread count can't exceed 500."           
            return True, ""
        except ValueError:
            return False, "Thread count must be a valid number."