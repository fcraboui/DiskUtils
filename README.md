DiskUtils is a Python utility for managing disk operations. This tool provides various actions and options to help you manage your disk space efficiently.

## Installation
To install DiskUtils, you can clone the repository and install the required dependencies:
```sh
git clone <repository-url>
cd DiskUtils
pip install -r requirements.txt
```

## Usage
To run DiskUtils, use the following command:
``` sh
python main.py
```

## Possible Actions
DiskUtils supports various actions that can be performed on your disk. Here are some of the common actions:  

### Check Disk Usage: Check the disk usage of a specified directory.  
``` sh
python main.py check-usage /path/to/directory
```

### Clean Disk: Clean up unnecessary files in a specified directory.  
``` sh
python main.py clean /path/to/directory
```

### List Files: List all files in a specified directory.  
``` sh 
python main.py list-files /path/to/directory
```

## Possible Options
DiskUtils provides several options to customize its behavior. Here are some of the common options:  
```--verbose```: Enable verbose output.  
python main.py check-usage /path/to/directory --verbose

```--dry-run```: Perform a dry run without making any changes.  
python main.py clean /path/to/directory --dry-run

```--output```: Specify the output format (e.g., text, json).  
python main.py list-files /path/to/directory --output json

## Example Outputs
Here are some examples of the output you can expect from DiskUtils:  
### Check Disk Usage output:  
```$ python main.py check-usage /path/to/directory
Total size: 1.2 GB
```

### Clean Disk output:  
```$ python main.py clean /path/to/directory
Cleaned 500 MB of unnecessary files.
```

### List Files output:  
```$ python main.py list-files /path/to/directory
file1.txt
file2.txt
directory1/
```

## Pre-commit Hook Configuration
To ensure code quality, you can use the ruff pre-commit hook. Add the following configuration to your .pre-commit-config.yaml file:

```yaml
repos:
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.7.1 # Replace with the desired version
    hooks:
      - id: ruff    
```
