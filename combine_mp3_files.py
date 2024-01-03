import os
import re
import logging
import configparser
from pydub import AudioSegment

def load_config(file_path='config.ini'):
    """
    Load and validate the configuration from a file.
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    required_sections = {'Logging', 'Paths', 'Settings'}
    if not required_sections.issubset(config.sections()):
        raise ValueError(f"Missing required sections in config: {required_sections}")
    return config

def setup_logging(config):
    """
    Configure logging based on the provided configuration.
    """
    log_level = config['Logging']['LogLevel']
    log_file_path = config['Logging']['LogFilePath']
    log_file_mode = config['Logging']['LogFileMode']
    log_format = config['Logging']['LogFormat']
    date_format = config['Logging']['DateFormat']

    log_directory = os.path.dirname(log_file_path)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logging.basicConfig(level=log_level,
                        format=log_format,
                        datefmt=date_format,
                        filename=log_file_path,
                        filemode=log_file_mode)

def get_number_from_filename(filename):
    try:
        # Try to find a 3-digit number, then a 2-digit number
        for pattern in [r'\d{3}', r'\d{2}']:
            match = re.search(pattern, filename)
            if match:
                return int(match.group())
        return None
    except Exception as e:
        logging.error(f"Error processing filename '{filename}': {e}")
        return None

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
        
        # Get the parent directory of the last component
        parent_directory_path = os.path.dirname(input_directory)

        # Now get the last part of this parent directory path
        parent_directory_name = os.path.basename(parent_directory_path)

        # Get the first 15 characters of the input directory name
        input_dir_name = os.path.basename(parent_directory_name)[:15]
        print (input_dir_name)

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

            # Construct the output file name using the directory name and index
            output_file_name = f'{input_dir_name}_{index_str}.mp3'
            output_file_path = os.path.join(output_directory, output_file_name)
            try:
                output.export(output_file_path, format='mp3')
                logging.info(f"Exported '{output_file_path}' successfully.")
            except Exception as e:
                logging.error(f"Failed to export '{output_file_path}': {e}")

    except Exception as e:
        logging.critical(f"Failed to concatenate MP3 files: {e}")

def main():
    config = load_config()
    setup_logging(config)
    
    # Extract parameters from the config file
    input_directory = config['Paths']['InputDirectory']
    output_directory = config['Paths']['OutputDirectory']
    output_size_mb = config['Settings'].getint('OutputSizeMB')

    concatenate_mp3_files(input_directory, output_directory, output_size_mb)

if __name__ == "__main__":
    main()
