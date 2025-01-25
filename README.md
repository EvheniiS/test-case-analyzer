# Test Case Redundancy Analyzer

Python-based tool that identifies redundant test cases using K-means clustering and similarity scoring. Helps QA teams reduce test suite maintenance by automating redundancy detection in XML exports from test management systems.

## Setup

1. Clone repository
2. Place XML file in tool directory
3. Run `run_analysis.bat`

## Requirements

- Python 3.6+
- Windows OS

Dependencies auto-install on first run:
- lxml
- pandas
- scikit-learn

## Usage

1. Export test cases as XML from your test management system
2. Place XML in tool directory
3. Double-click `run_analysis.bat`
4. Enter XML filename when prompted
5. Review generated redundancy report

## Output Files

- `[filename]-parsed.csv`: Parsed test cases
- `redundancy_analysis_[filename]-parsed.csv`: Redundancy analysis with similarity scores

## How It Works

Tool uses:
- K-means clustering to group similar test cases
- Cosine similarity scoring (>75% indicates potential redundancy)
- Priority and core dependency analysis

## License

MIT