import csv


class CSVFile:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def write_to_csv(self):
        with open(self.filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter='\n', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.data)
