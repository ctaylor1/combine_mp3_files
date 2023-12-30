import os
import re
import logging
import configparser
from pydub import AudioSegment

# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Retrieve logging configuration from the configuration file
log_level = config['Logging']['LogLevel']
log_file_path = config['Logging']['LogFilePath']
log_file_mode = config['Logging']['LogFileMode']
log_format = config['Logging']['LogFormat']
date_format = config['Logging']['DateFormat']

# Ensure log directory exists
log_directory = os.path.dirname(log_file_path)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logging.basicConfig(level=log_level,
                    format=log_format,
                    datefmt=date_format,
                    filename=log_file_path,
                    filemode=log_file_mode)

def get_number_from_filename(filename):
    # ... [Your existing function code here]

def concatenate_mp3_files(input_directory, output_directory, output_size_mb):
    try:
        # Validate directories
        if not os.path.isdir(input_directory):
            raise ValueError(f"Input directory '{input_directory}' does not exist.")
        if not os.path.isdir(output_directory):
            raise ValueError(f"Output directory '{output_directory}' does not exist.")

        # Validate output_size_mb
        if output_size_mb <= 0:
            raise ValueError("output_size_mb must be greater than 0.")

        files = [f for f in os.listdir(input_directory) if f.endswith('.mp3')]
        sorted_files = sorted(files, key=lambda f: get_number_from_filename(f) or 0)

        combined = AudioSegment.empty()
        output_files = []
        current_size = 0

        # Get the first 15 characters of the input directory name
        input_dir_name = os.path.basename(input_directory)[:15]

        for file in sorted_files:
            try:
                sound = AudioSegment.from_mp3(os.path.join(input_directory, file))
                combined += sound
                current_size += len(sound.raw_data)
            except Exception as e:
                logging.error(f"Error processing file '{file}': {e}")
                continue

            # Check if the current combined size exceeds the limit
            if current_size >= output_size_mb * 1024 * 1024:
                output_files.append(combined)
                combined = AudioSegment.empty()
                current_size = 0

        if current_size > 0:
            output_files.append(combined)
        
        # Save the output files
        for i, output in enumerate(output_files):
            # Format the index as a two-digit number
            index_str = f'{i+1:02d}'

            # Use the input directory name in the output file name
            output_file_name = f'{input_dir_name}_output_{index_str}.mp3'
            output_file_path = os.path.join(output_directory, output_file_name)
            try:
                output.export(output_file_path, format='mp3')
                logging.info(f"Exported '{output_file_path}' successfully.")
            except Exception as e:
                logging.error(f"Failed to export '{output_file_path}': {e}")

    except Exception as e:
        logging.critical(f"Failed to concatenate MP3 files: {e}")

def main():
    # Extract parameters from the config file
    input_directory = config['Paths']['InputDirectory']
    output_directory = config['Paths']['OutputDirectory']
    output_size_mb = config['Settings'].getint('OutputSizeMB')

    concatenate_mp3_files(input_directory, output_directory, output_size_mb)

if __name__ == "__main__":
    main()
