# Test Case Redundancy Analysis Tool - User Guide

## Prerequisites
- Windows computer
- Python installed (version 3.6 or higher)
- Internet connection (for first-time dependency installation)

## One-Time Setup
1. Create a folder for the tool (e.g., "TestCaseAnalysis")
2. Download these files to the folder:
   - `test_case_analyzer.py`
   - `run_analysis.bat`

## Running the Analysis

### Step 1: Export Test Cases
1. In your test case management system:
   - Filter test cases for your team
   - Export them as XML format
   - Save the XML file

### Step 2: Prepare Files
1. Move your exported XML file to the tool folder
2. Make sure the filename ends with `.xml` (e.g., `team-test-cases.xml`)

### Step 3: Run Analysis
1. Double-click `run_analysis.bat`
2. When prompted, type the XML filename and press Enter
3. Wait for the process to complete

### Step 4: Review Results
The tool creates two files:
- `[your-filename]-parsed.csv`: Parsed test cases
- `redundancy_analysis_[your-filename]-parsed.csv`: Redundancy analysis results

## Understanding Results
The redundancy analysis CSV shows:
- Test cases grouped by similarity (Cluster ID)
- Similarity scores (>75% indicates potential redundancy)
- Core dependency status
- Testing levels
- Recommended actions

## Troubleshooting
- If dependencies fail to install: Run as administrator
- If XML parsing fails: Check file encoding (should be UTF-8)
- If file not found: Verify filename matches exactly, including case

## Support
For technical issues:
1. Check if XML file is in the correct folder
2. Verify Python is installed correctly
3. Try running as administrator
4. Contact technical support if issues persist