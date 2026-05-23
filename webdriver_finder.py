import psutil


def check_running_chrome():
    # Get the list of all running processes
    running_processes = psutil.process_iter(['pid', 'name', 'cmdline'])

    # Create a list to store Chrome process information
    chrome_processes = []

    # Iterate through all running processes
    for process in running_processes:
        try:
            # Check if the process name contains 'chrome'
            if 'chrome' in process.info['name'].lower():
                chrome_processes.append({
                    'pid': process.info['pid'],
                    'name': process.info['name'],
                    'cmdline': process.info['cmdline']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue  # Process has exited or access denied

    # Display the found Chrome processes
    if chrome_processes:
        print("Found the following Chrome processes:")
        for chrome in chrome_processes:
            print(f"PID: {chrome['pid']}, Command: {chrome['cmdline']}")
    else:
        print("No Chrome processes found.")

    return chrome_processes


def terminate_chrome_processes(chrome_processes):
    for chrome in chrome_processes:
        try:
            process = psutil.Process(chrome['pid'])
            process.terminate()  # You can use process.kill() for a forceful termination
            print(f"Terminated Chrome process with PID: {chrome['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print(f"Could not terminate process with PID: {chrome['pid']} (it may no longer exist).")


if __name__ == "__main__":
    chrome_processes = check_running_chrome()

    # Prompt user to terminate Chrome processes if any are found
    if chrome_processes:
        terminate = input("Do you want to terminate these Chrome processes? (yes/no): ").strip().lower()

        if terminate in ['yes', 'y']:
            terminate_chrome_processes(chrome_processes)
        else:
            print("No processes were terminated.")