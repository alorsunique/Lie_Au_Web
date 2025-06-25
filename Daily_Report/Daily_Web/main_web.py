from flask import Flask, render_template
from datetime import datetime


app = Flask(__name__)

# Specify the path to your text file here


@app.route('/')
def index():
    current_time = datetime.now().strftime('%H:%M')
    current_date = datetime.now().strftime('%d %B %Y')
    current_day_of_week = datetime.now().strftime('%A')

    try:
        # Read content from the specified text file
        with open(TEXT_FILE_PATH, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        content = "The specified file was not found."
    except Exception as e:
        content = f"An error occurred while reading the file: {e}"

    # Render the HTML template with the content
    return render_template('index.html', content=content, current_time=current_time, current_date=current_date, current_day_of_week=current_day_of_week)

if __name__ == '__main__':
    TEXT_FILE_PATH = r'D:\Projects\Resources\Lie_Au_Web Resources\Daily Report\daily_text.txt'
    app.run(debug=True)