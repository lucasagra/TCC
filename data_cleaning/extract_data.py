import csv
import json

# Open the CSV file
with open('../laudo_original.csv', 'r') as csv_file:
    # Read the contents of the CSV file
    csv_contents = csv.reader(csv_file)
    # Skip the header row
    header = next(csv_contents)
    # Create an empty list to hold the data
    data = []
    # Loop through the remaining rows
    for row in csv_contents:
        # Create a dictionary to hold the row data
        row_data = {}
        # Loop through the fields in the row
        for i in range(len(header)):
            # Add the field to the dictionary
            row_data[header[i]] = row[i]
        # Add the dictionary to the data list
        data.append(row_data)

# Open the JSON file
with open('extracted_data.json', 'w') as json_file:
    # Write the data to the JSON file with indentation
    json.dump(data, json_file, indent=2)