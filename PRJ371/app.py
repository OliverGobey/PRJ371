from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np

app = Flask(__name__)

# Global variable to store min and max values and average values
min_max_values = {}
average_values = {}

# Store the original uploaded data to reuse for simulation
original_data = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global min_max_values, average_values, original_data
    file = request.files['file']
    
    if file and file.filename.endswith('.csv'):
        # Read CSV file into DataFrame
        original_data = pd.read_csv(file)

        # Initialize min, max, and average values for numeric columns
        min_max_values = {col: (original_data[col].min(), original_data[col].max()) for col in original_data.select_dtypes(include=np.number).columns}
        average_values = {col: original_data[col].mean() for col in original_data.select_dtypes(include=np.number).columns}

        # Render the uploaded data
        return render_template('data_table.html', data=original_data.to_dict(orient='records'), columns=original_data.columns, simulated_data=None)

    return render_template('index.html', error="File not found or not a CSV")

@app.route('/simulate', methods=['POST'])
def simulate_data():
    global original_data
    random_data = []
    acceptance_results = []

    # Prepare an empty DataFrame for the simulated data
    simulated_data = pd.DataFrame(columns=original_data.columns)

    for col in min_max_values.keys():
        min_val, max_val = min_max_values[col]

        # Generate random values for each row of the column
        simulated_column = np.random.uniform(min_val, max_val, len(original_data))

        # Append the column to the simulated DataFrame
        simulated_data[col] = simulated_column.round(2)  # Rounded to 2 decimal places

    # Render both original and simulated data
    return render_template('data_table.html', data=original_data.to_dict(orient='records'), columns=original_data.columns, simulated_data=simulated_data.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)
