import csv
import json
import re 

with open('extracted_data.json', 'r') as f:
    data = json.load(f)

    # Erase unnecessary /n's 
    for item in data:

        # Remove useless characters.
        item['report'] = re.sub(r"\xa0", "", item['report'])
        item['report'] = re.sub(r"\u3000", "", item['report'])
        item['report'] = re.sub(r"\t+", " ", item['report'])
        # Remove multiple blankspaces
        item['report'] = re.sub(r" +", " ", item['report'])
        # Remove breaklines.
        item['report'] = re.sub(r"( \n)", "\n", item['report'])
        item['report'] = re.sub(r"\n+", " ", item['report'])
        # Remove breaklines from beginning and end.
        item['report'] = re.sub(r"(^\n|\n$)", "", item['report'])
        # Remove whitespaces from beginning and end.
        item['report'] = re.sub(r"(^ | $)", "", item['report'])

# Writes the JSON file
with open('cleaned_data.json', 'w') as json_file:
    # Write the data to the JSON file with indentation
    json.dump(data, json_file, indent=2)

# Writes the CSV file
with open('cleaned_data.csv', 'w', newline='') as csv_file:
    # Create a CSV writer
    writer = csv.writer(csv_file)
    writer.writerow(data[0].keys())
    # Write the data rows
    for row in data:
        writer.writerow(row.values())