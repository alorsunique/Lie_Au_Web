from flask import Flask, render_template
from datetime import datetime
from pathlib import Path
import yaml





app = Flask(__name__)





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












@app.route('/')
def index():
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%d %B %Y')
    current_day_of_week = datetime.now().strftime('%A')

    # Try reading the daily report
    try:
        with open(report_next_day_path, 'r', encoding='utf-8') as file:
            daily_text_content = file.read()
    except FileNotFoundError:
        daily_text_content = "Daily report file not found."
    except Exception as e:
        daily_text_content = f"Error reading daily report: {e}"

    # Try reading the weather report
    try:
        with open(WEATHER_PATH, 'r', encoding='utf-8') as file:
            weather_text_content = file.read()
    except FileNotFoundError:
        weather_text_content = "Weather report file not found."
    except Exception as e:
        weather_text_content = f"Error reading weather report: {e}"

    # Try reading the weather report
    try:
        with open(report_remain_month_path, 'r', encoding='utf-8') as file:
            complete_content = file.read()
    except FileNotFoundError:
        complete_content = "Weather report file not found."
    except Exception as e:
        complete_content = f"Error reading weather report: {e}"



    # Render the HTML template with the content
    return render_template(
        'index.html',
        content=daily_text_content,
        weather_content = weather_text_content,
        complete_summary = complete_content,
        current_time=current_time,
        current_date=current_date,
        current_day_of_week=current_day_of_week)

if __name__ == '__main__':
    config_file_name = 'Lie_Au_Web_config.yaml'
    script_path = Path(__file__).resolve()
    project_dir = find_project_root(script_path, config_file_name)

    config_file_path = project_dir / config_file_name

    with open(config_file_path, "r") as open_config:
        config_content = yaml.safe_load(open_config)

    resources_dir = Path(config_content['resources_dir'])
    daily_report_dir = resources_dir / "Daily Report"


    report_next_day_path = daily_report_dir / 'report_next_day_comeback.txt'
    report_remain_month_path = daily_report_dir / 'report_remain_month_comeback.txt'




    TEXT_FILE_PATH = r'D:\Projects\Resources\Lie_Au_Web Resources\Daily Report\daily_text.txt'
    WEATHER_PATH = r'D:\Projects\Resources\Lie_Au_Web Resources\Daily Report\daily_weather_text.txt'
    COMPLETE_PATH = r'D:\Projects\Resources\Lie_Au_Web Resources\Daily Report\complete_summary.txt'
    app.run(debug=True)