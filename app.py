from flask import Flask, render_template, request
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['DEBUG'] = True

# Home route (analysis page)
@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    text = ''

    if request.method == 'POST':
        text = request.form.get('text', '')
        output = f"Analyzed: {text}"  # Replace with real NLP logic

    return render_template('index.html', output=output, text=text)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
