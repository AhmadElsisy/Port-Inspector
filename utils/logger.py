import logging
import os
import sys
from datetime import datetime
from typing import Optional


class Logger:
    def __init__(self, log_level: str = "INFO",
                  log_file: Optional[str] = None,
                  log_to_console: bool = True):
        """
        Initialize the logger with specified configuration
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for logging. If None, only console logging is used
            log_to_console: Whether to output logs to console
        """
       
          
        # Create logger instance
        self.logger = logging.getLogger("PortInspector")
        self.logger.setLevel(self.get_log_level(log_level))

        # Clear any existed handlers to prevent duplication
        self.logger.handlers.clear()

        # Set logging formatter
        console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        
        file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        
        # Add logging to console if it requested
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

        # Add file handler
        if log_file:
            # Creates logs directory
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir)
                except OSError as e:
                    self.logger.error(f"Failed to create log directory: {e}")
                    log_to_console = True

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)   
    
    # Convert logging level to logging constants
    def get_log_level(self, level: str) -> int:
        return getattr(logging, level.upper(), logging.INFO)
    
    # Define start scan to log scan start info
    def start_scan(self, target: str, start_port: int, end_port: int) -> None:
        self.logger.info(f"Starting scan on {target} (ports {start_port} - {end_port})")

    # Define end scan to log scan completion info
    def end_scan(self, target: str, duration: float) -> None:
        self.logger.info(f"Scan on {target} completed in {duration:.2f} seconds.")

    # Define port status to log port scan result
    def port_stat(self, port: int, status: str, service: str = "") -> None:
        if status.lower() == "open":
            if service:
                self.logger.info(f"Port {port} is open (service = {service})")
            else:
                self.logger.info(f"Port {port} is open.")
        else:
            self.logger.debug(f"Port {port} is {status}")

    # Log error messages
    def error(self, message: str, exc_info: bool = False) -> None:
        self.logger.error(message, exc_info=exc_info)   

    # Log warning messages
    def warning(self, message: str) -> None:
        self.logger.warning(message)

    # Log debug messages
    def debug(self, message: str) -> None:
        self.logger.debug(message)

    # Log info message
    def info(self, message: str) -> None:
        self.logger.info(message)

    # Log validation error message
    def validation_error(self, component: str, message: str) -> None:
        self.logger.error(f"Validation error in ({component}): {message}")

    # Log scan progress
    def scan_progress(self, scanned: int, total: int) -> None:
        percent = (scanned / total) * 100
        self.logger.debug(f"Scan progress: {percent:.1f}% ({scanned}/{total} ports)") 

    # Log connection error
    def conn_error(self, target: str, error: str) -> None:
        self.logger.error(f"Connection error to {target}: {error}")

    # Log threading information
    def threading_info(self, thread_count: int) -> None:
        self.logger.debug(f"Using {thread_count} threads for scanning.")


