import csv
from datetime import datetime
import os


class ReportWriter:
    def __init__(self):
        # Get the project root directory
        self.project_root = self.get_project_root()

        # Define reports path
        self.reports_dir = os.path.join(self.project_root, "reports")

        # Create directory if it isn't existed
        self.ensure_dir()

    def get_project_root(self):
        """Get the absolute path to the root directory"""
        # Get the current directory where this script is loaded
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go up to the root directory
        return os.path.dirname(current_dir)   

    def ensure_dir(self):
        """Create the necessary directory if not existed"""
        try:
            os.makedirs(self.reports_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory {self.reports_dir}: {e}")

    def write_report(self, scan_results):
        if not scan_results:
            return

        # Generate time stamps to make every file unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_name = scan_results['target'].replace('.', '_')

        try:
            # Write CSV report
            self.write_csv_report(scan_results, f"{target_name}_{timestamp}")
            # Write TXT report
            self.write_txt_report(scan_results, f"{target_name}_{timestamp}")
        except Exception as e:
            print(f"Error writing report: {e}")

    def write_csv_report(self, scan_results, filename):
        csv_path = os.path.join(self.reports_dir, f"{filename}.csv")
        try:
            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)   

                # Write header information
                writer.writerow(['Scan Report'])
                writer.writerow(['Target', scan_results['target']])
                writer.writerow(['IP Address', scan_results['target_ip']])
                writer.writerow(['Scan Start', scan_results['start_time']])
                writer.writerow(['Scan End', scan_results['end_time']])
                writer.writerow(['Duration (seconds)', f"{scan_results['duration']:.2f}"])
                writer.writerow(['Ports Scanned', scan_results['ports_scanned']])
                writer.writerow([]) 

                # Write open ports
                writer.writerow(['port', 'service'])
                for port_info in scan_results['open_ports']:
                    writer.writerow([port_info['port'], port_info['service']])
                    
                print(f"CSV report saved: {csv_path}") 

        except IOError as e:
            print(f"Error writing CSV report to {csv_path}: {e}")         


    def write_txt_report(self, scan_results, filename):
        txt_path = os.path.join(self.reports_dir, f"{filename}.txt")
        try:
            with open(txt_path, 'w') as txtfile:
                txtfile.write("PORT INSPECTOR SCAN REPORT\n")
                txtfile.write("=" * 30 + "\n\n")

                # Write scan information
                txtfile.write(f"Target Host: {scan_results['target']}\n")
                txtfile.write(f"IP Address: {scan_results['target_ip']}\n")
                txtfile.write(f"Scan Start: {scan_results['start_time']}\n")
                txtfile.write(f"Scan End: {scan_results['end_time']}\n")
                txtfile.write(f"Duration: {scan_results['duration']:.2f} seconds\n")
                txtfile.write(f"Total Ports Scanned: {scan_results['ports_scanned']}\n\n")

                # Write open ports
                txtfile.write(f"OPEN PORTS ({len(scan_results['open_ports'])} found)\n")
                txtfile.write("-" * 30 + "\n")

                if scan_results['open_ports']:
                    for port_info in scan_results['open_ports']:
                        txtfile.write(f"Port {port_info['port']}/TCP\t- Service: {port_info['service']}\n")
                else:
                    txtfile.write("No open ports found.\n")
                
                print(f"Text report saved: {txt_path}")
        except IOError as e:
            print(f"Error writing text report to {txt_path}: {e}")        

        


    
