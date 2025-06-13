from flask import Flask, render_template

app = Flask(__name__)

# Specify the path to your text file here
TEXT_FILE_PATH = '/path/to/your/textfile/content.txt'

@app.route('/')
def index():
    try:
        # Read content from the specified text file
        with open(TEXT_FILE_PATH, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        content = "The specified file was not found."
    except Exception as e:
        content = f"An error occurred while reading the file: {e}"

    # Render the HTML template with the content
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)