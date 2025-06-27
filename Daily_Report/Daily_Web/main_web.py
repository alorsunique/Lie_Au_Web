from flask import Flask, render_template
from datetime import datetime



app = Flask(__name__)

# Specify the path to your text file here


@app.route('/')
def index():
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%d %B %Y')
    current_day_of_week = datetime.now().strftime('%A')

    # Try reading the daily report
    try:
        with open(TEXT_FILE_PATH, 'r', encoding='utf-8') as file:
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
        with open(COMPLETE_PATH, 'r', encoding='utf-8') as file:
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
    TEXT_FILE_PATH = r'D:\Projects\Resources\Lie_Au_Web Resources\Daily Report\daily_text.txt'
    WEATHER_PATH = r'D:\Projects\Resources\Lie_Au_Web Resources\Daily Report\daily_weather_text.txt'
    COMPLETE_PATH = r'D:\Projects\Resources\Lie_Au_Web Resources\Daily Report\complete_summary.txt'
    app.run(debug=True)