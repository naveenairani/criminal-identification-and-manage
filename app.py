from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
    run_detection()  # Call the function to run home.py

    return render_template('index.html')

# @app.route('/detect', methods=['GET', 'POST'])
# def detect():
#     if request.method == 'POST':
#         run_detection()  # Call the function to run home.py
#         flash('Detection completed')
#         return redirect(url_for('home'))
#     else:
#         return render_template('detect.html')

def run_detection():
    # Execute the logic from home.py here
    os.system('python home.py')  # Replace with the appropriate command or code

@app.route('/manage')
def manage():
    # Add logic for managing criminals here
    return render_template('manage.html')  # Assuming you have a manage.html template


if __name__ == '__main__':
    app.run(debug=True)
