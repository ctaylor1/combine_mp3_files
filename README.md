# README.md for MP3 Concatenation Tool

## Introduction
This Python script provides a utility to concatenate multiple MP3 files based on their filenames. It is designed to handle large sets of MP3 files, organizing them into combined files of specified maximum sizes. The script utilizes a configuration file for settings and employs robust logging for monitoring its operations.

## Use Cases
- Take audiobook files by chapter and consolidate them down to a few files.
- Take an entire album and turn it into one or two files.

## Features
- **Configurable**: Utilizes a `config.ini` file for easy configuration of paths, logging, and operational parameters.
- **Logging**: Detailed logging of operations, errors, and informational messages.
- **Dynamic File Handling**: Concatenates MP3 files by sorting them based on numeric values extracted from filenames.
- **Output Size Management**: Allows specification of the maximum size for the output MP3 files.

## Requirements
- Python 3.x
- `pydub` library (for handling MP3 files).  Included in requirements.txt file below.
- A valid `config.ini` file with appropriate settings.

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install required libraries using pip:
   ```
   pip install -r requirements.txt
   ```
3. Clone or download this repository to your local machine.

## Configuration
Create a `config.ini` file in the same directory as the script with the following sections and settings:

```
[Logging]
LogLevel = INFO
LogFilePath = path/to/logfile.log
LogFileMode = a
LogFormat = %(asctime)s - %(levelname)s - %(message)s
DateFormat = %Y-%m-%d %H:%M:%S

[Paths]
InputDirectory = path/to/input/directory
OutputDirectory = path/to/output/directory

[Settings]
OutputSizeMB = 50
```

- `LogLevel`: Set the logging level (e.g., `INFO`, `ERROR`).
- `LogFilePath`: Path to the log file.
- `LogFileMode`: File mode for the log file (e.g., `a` for append).
- `LogFormat` & `DateFormat`: Format for logging messages and timestamps.
- `InputDirectory` & `OutputDirectory`: Directories for input MP3 files and output.
- `OutputSizeMB`: Maximum size in MB for each concatenated output file.

## Usage
Run the script using Python:
```
python mp3_concatenation_tool.py
```

The script will read the MP3 files from the input directory, concatenate them, and save them in the output directory as specified in the `config.ini` file.

## Contributing
Contributions to this project are welcome. Please ensure that any pull requests adhere to the existing coding style and include appropriate tests.

## License
GNU General Public License 

---

*Note: This README provides basic instructions. It assumes a certain level of familiarity with Python and command-line operations.*