# Pyls - Python Directory Listing Utility

## Overview
`pyls` is a Python command-line utility designed to mimic the behavior of the Unix `ls` command. It reads a JSON file that represents a directory structure and outputs the contents in various formats. This project is developed as part of a technical test for Zuru.

## Features
- **List Directory Contents**: Display the names of files and directories in the specified directory.
- **Show Hidden Files**: Include hidden files in the listing with the `-A` option.
- **Detailed Listing**: Provide detailed information including permissions, size, modification time, and name with the `-l` option.
- **Reverse Order**: Display the listing in reverse order with the `-r` option.
- **Sort by Time**: Sort the listing by modification time with the `-t` option.
- **Filter by Type**: Filter the listing to show only files or only directories using the `--filter` option.
- **Navigate Paths**: Navigate and list contents within nested directories.
- **Human-Readable Sizes**: Display sizes in a human-readable format with the `-h` option.
- **Help**: Show help information with the `--help` option.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sourabhadap/pyls.git
   cd pyls
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the package:
   ```bash
   pip install .
   ```
4. Use it directly from the command line
```bash
   python -m pyls <command> 
```

## Usage
Once installed, `pyls` can be used from the command line. Below are examples of its usage:

1. **Basic Listing**:
   ```bash
   pyls
   ```
   Output:
   ```
   LICENSE README.md ast go.mod lexer main.go parser token
   ```

2. **Show All Files Including Hidden**:
   ```bash
   pyls -A
   ```
   Output:
   ```
   .gitignore LICENSE README.md ast go.mod lexer main.go parser token
   ```

3. **Detailed Listing**:
   ```bash
   pyls -l
   ```
   Output:
   ```
   -rw-r--r-- 1071 Nov 14 11:27 LICENSE
   -rw-r--r-- 83 Nov 14 11:27 README.md
   drwxr-xr-x 4096 Nov 14 15:58 ast
   -rw-r--r-- 60 Nov 14 13:51 go.mod
   drwxr-xr-x 4096 Nov 14 15:21 lexer
   -rw-r--r-- 74 Nov 14 13:57 main.go
   drwxr-xr-x 4096 Nov 17 12:51 parser
   drwxr-xr-x 4096 Nov 14 14:57 token
   ```

4. **Reverse Order**:
   ```bash
   pyls -l -r
   ```
   Output:
   ```
   drwxr-xr-x 4096 Nov 14 14:57 token
   drwxr-xr-x 4096 Nov 17 12:51 parser
   -rw-r--r-- 74 Nov 14 13:57 main.go
   drwxr-xr-x 4096 Nov 14 15:21 lexer
   -rw-r--r-- 60 Nov 14 13:51 go.mod
   drwxr-xr-x 4096 Nov 14 15:58 ast
   -rw-r--r-- 83 Nov 14 11:27 README.md
   -rw-r--r-- 1071 Nov 14 11:27 LICENSE
   ```

5. **Sorted by Modification Time**:
   ```bash
   pyls -l -r -t
   ```
   Output:
   ```
   drwxr-xr-x 4096 Nov 17 12:51 parser
   drwxr-xr-x 4096 Nov 14 15:58 ast
   drwxr-xr-x 4096 Nov 14 15:21 lexer
   drwxr-xr-x 4096 Nov 14 14:57 token
   -rw-r--r-- 74 Nov 14 13:57 main.go
   -rw-r--r-- 60 Nov 14 13:51 go.mod
   -rw-r--r-- 1071 Nov 14 11:27 LICENSE
   -rw-r--r-- 83 Nov 14 11:27 README.md
   ```

6. **Filter by Type**:
   ```bash
   pyls -l -r -t --filter=dir
   ```
   Output:
   ```
   drwxr-xr-x 4096 Nov 17 12:51 parser
   drwxr-xr-x 4096 Nov 14 15:58 ast
   drwxr-xr-x 4096 Nov 14 15:21 lexer
   drwxr-xr-x 4096 Nov 14 14:57 token
   ```

7. **Human-Readable Sizes**:
   ```bash
   pyls -l -h parser
   ```
   Output:
   ```
   -rw-r--r-- 533 Nov 14 16:03 go.mod
   -rw-r--r-- 1.6K Nov 17 12:05 parser.go
   -rw-r--r-- 1.4K Nov 17 12:51 parser_test.go
   ```

8. **Help**:
   ```bash
   pyls --help
   ```

## Testing
To run tests, use:
```bash
python -m unittest
```


Feel free to customize this README to better match your project and personal details.