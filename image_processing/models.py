#
import csv
import re


def extract_specific_data(input_file, output_file):
    # Regular expression pattern to match URLs
    url_pattern = r'https?://[^\s]+\.jpg'

    # Initialize a list to store filtered URLs
    image_urls = []

    # Open the input CSV file
    with open(input_file, 'r', newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)

        # Iterate through each row in the CSV file
        for row in reader:
            # Concatenate all elements in the row to form a single string
            row_string = ' '.join(row)

            # Find all URLs in the row using regular expression
            urls = re.findall(url_pattern, row_string)

            # Filter URLs containing "pickup_car_front"
            pickup_car_front_urls = [url for url in urls if 'pickup_car_bonnet' in url]

            # Add filtered URLs to the list
            image_urls.extend(pickup_car_front_urls)

    # Write the filtered URLs to the output file
    with open(output_file, 'w') as outfile:
        # Write filtered URLs with each URL wrapped in quotes and separated by commas
        outfile.write("image_urls = [\n")
        outfile.write(',\n'.join(f'    "{url}"' for url in image_urls))
        outfile.write("\n]\n")


# Example usage:
input_file = '/home/mjasim/Downloads/b2b_client_photo_checkup_2024-02-23T12_43_18.650101+05_30(6).csv'
output_file = '/home/mjasim/Desktop/DriveU/image_processing/images.py'
extract_specific_data(input_file, output_file)
