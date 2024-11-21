# **Port Inspector**

## **Description:**

 Port Inspector is a Python-based port scanning tool that allows users to scan network ports on target hosts, identify  open ports, and generate detailed reports of the findings.
 This project was created as a final project for CS50x, implementing security best practices and providing both  command-line and interactive interfaces.

## **Features**

- Scan single or range of ports on specified targets.
- Automatic service identification for open ports.
- Multi-threaded scanning for improved performance.
- Input validation for all user inputs.
- Detailed logging system.
- Report generation in both CSV and TXT formats.
- Command-line interface and interactive mode.
- Built-in timeout and thread management.
- Comprehensive error handling.

## **Project Structure**

port-inspector/
├── main.py               # Main entry point and CLI interface
├── scanner/
│   └── port_inspector.py # Core scanning functionality
├── utils/
│   ├── validator.py      # Input validation
│   ├── logger.py         # Logging functionality
│   └── report_writer.py  # Report generation
├── logs/                 # Directory for log files
├── reports/              # Directory for generated reports
└── README.md             # Project documentation

## **Technologies Used**

- Python 3.11 and Vs code.
- ***Standard Library Modules:***
  - `socket` for network operations.
  - `argparse` for CLI argument parsing.
  - `concurrent.futures` for multi-threading.
  - `logging` for event logging.
  - `csv` for report generation.
  - `datetime` for timestamps.
- ***Third-party Libraries:***
  - `pyfiglet` for ASCII art banner.
  - `pycodestyle` for syntax linting.

## **Usage**

### Command Line Interface

```bash
python main.py -t example.com -s 80 -e 443   # Scan ports 80-443 on example.com
python main.py -t example.com                # Scan default ports (1-1024)
```

### Interactive Mode

```bash
python main.py
```

Follow the prompts to enter:

- Target host: (domain name or IP address)
- Start port number: 1 - 65535
- End port number: 1 - 65535
- Timeout: 1 - 30
- Threads: 1 - 500

## **Security Features**

- Input validation for all user inputs.
- Proper error handling and logging.
- Clear warning messages about unauthorized scanning.
- Rate limiting through timeout settings.
- Thread count limitations.

## **Design Choices**

1. **Modular Architecture**:
 The project is split into separate modules for better organization and maintainability:
    - `port_inspector.py`: Core scanning logic.
    - `validator.py`: Input validation for target, ports, timeout, and thread count entries.
    - `logger.py`: Logging functionality using timestamps for unique identificattion.
    - `report_writer.py`: Report generation in CSV and TXT for more readable report.

2. **Multi-threading**:
 Implemented using ThreadPoolExecutor to improve scanning speed while maintaining control over resource usage.

3. **Comprehensive Validation**:
  All inputs are validated to prevent errors and ensure secure operation:
     - Port range validation (1-65535).
     - Hostname/IP validation.
     - Thread count and timeout validation.

4. **Detailed Reporting**:
 Two report formats (CSV and TXT) provide flexibility in analyzing results.

## **Areas for Improvement**

 1. Add support for UDP port scanning.
 2. Create a GUI for a more friendly UI for non-techs.
 3. Include it as part of a wide-spectrum vulnerability scanner.
 4. Include vulnerability database integration.
 5. Add support for IPv6 addresses.
 6. Adding multiple scanning with request rate limiting.
 7. Add export options for different report formats.

## **How to Test**

1. Basic scan:

```bash
python main.py -t localhost -s 80 -e 100
```

2. Full range scan:

```bash
python main.py -t example.com -s 1 -e 1024 --timeout 30 --threads 500
```

3. Interactive mode:

```bash
python main.py
```

## **Credits and Acknowledgements**

- CS50x course staff and community, especially David J Malan.

## **Useful resources**

- Python Programming documentation and communities.
- CS50P course by David J. Malan.
- PYPI the Python packages index.
- ChatGPT for brainstorming, arranging project phases, and some code reviews for logger file.
- Claude AI for scientific explanation, and establishing of this readme file.
- CS Duck as my first assistant and enhancer of my code.
- NeuralNine channel on YouTube for learning socket programming and general Python programming topics.
- Data Camp website for socket programming.
- Grammarly for grammar review of this file.
- stack overflow and geeks for geeks blogs for various research.

## **License**

This project is released under the MIT License. See the LICENSE file for details.

## Author

[Ahmed Ibraheem]
GitHub: [@AhmadElsisy]

## **Disclaimer**

This tool is intended for authorized use only.
Scanning ports without explicit permission from the target system's owner may be illegal.
Always ensure proper authorization before scanning any network or system.
The developer is not responsible for any misuse or damage caused by this program.
