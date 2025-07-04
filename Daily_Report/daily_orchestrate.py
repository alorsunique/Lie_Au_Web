# This script should orchestrate the calling of the daily components

from pathlib import Path
import sys



def find_project_root(script_path, marker):
    current_path = script_path
    while not (current_path / marker).exists():
        # If block checks for parent of current path
        # If it cannot go up any further, base directory is reached
        if current_path.parent == current_path:
            raise FileNotFoundError(f"Could not find '{marker}' in any parent directories.")

        current_path = current_path.parent

    # If it exits the while loop, marker was found
    return current_path


if __name__ == "__main__":
    config_file_name = 'Lie_Au_Web_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)
    sys.path.append(str(project_dir))

    config_file_path = project_dir / config_file_name

    from Daily_Report import kpop_comeback_tracker
    from Daily_Report import kpop_comeback_reader
    from Daily_Report import weather_test
    from Daily_Report import daily_report

    kpop_comeback_tracker.main()
    kpop_comeback_reader.main()
    weather_test.main()
    daily_report.main()