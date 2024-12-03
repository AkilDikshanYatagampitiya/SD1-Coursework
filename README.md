# SD1-Coursework
# Traffic Data Analysis Program

## Overview
This Python project analyzes traffic flow data collected from two road junctions: **Elm Avenue/Rabbit Road** and **Hanley Highway/Westway**. The program provides insights to help a local council make informed decisions for managing traffic flow. The solution includes input validation, data processing, result visualization, and a loop to analyze multiple datasets.

## Features
1. **Input Validation**:
   - Prompts users for dates in `DD MM YYYY` format and validates:
     - Correct data type (Integer required).
     - Day (1–31), Month (1–12), and Year (2000–2024) ranges.
   - Provides appropriate feedback for invalid inputs.

2. **Data Analysis**:
   - Processes CSV datasets to compute metrics such as:
     - Total vehicles, trucks, and electric vehicles.
     - Two-wheeled vehicles (bikes, motorbikes, scooters).
     - Vehicles exceeding speed limits.
     - Vehicles passing through specific junctions.

3. **Text File Output**:
   - Saves the analyzed results in `results.txt`.
   - Appends results when analyzing multiple datasets.

4. **Visualization**:
   - Displays a histogram (using `tkinter`) comparing traffic volumes across junctions.

5. **Multi-File Support**:
   - Allows users to analyze multiple datasets sequentially using a loop.

## Requirements
- Python 3.9 or later
- Libraries:
  - `os`
  - `csv`
  - `tkinter`

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/akildikshan/traffic-data-analysis.git
   cd traffic-data-analysis
2.Run the script:
  ```bash
  python 20230238.py
