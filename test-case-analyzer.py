import sys
import subprocess
import os
from typing import Optional
import time

def check_and_install_dependencies():
    """Check and install required dependencies."""
    required_packages = [
        'lxml',
        'pandas',
        'scikit-learn',
    ]
    
    print("Checking and installing required packages...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is already installed")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")

def preprocess_xml(content: str) -> str:
    """Preprocess XML content to escape unescaped '&' symbols."""
    import re
    return re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', content)

def parse_test_cases(xml_file: str) -> Optional[str]:
    """Parse XML test cases and return the path to the generated CSV file."""
    try:
        from lxml import etree
        import csv
        
        print(f"\nParsing XML file: {xml_file}")
        
        # Read and preprocess XML
        with open(xml_file, 'r', encoding='utf-8') as file:
            content = preprocess_xml(file.read())
        
        # Parse XML
        root = etree.fromstring(content.encode('utf-8'))
        
        # Generate output filename
        base_filename = os.path.splitext(os.path.basename(xml_file))[0]
        csv_file = f"{base_filename}-parsed.csv"
        
        test_cases = []
        for test_case in root.xpath('.//testCase'):
            test_cases.append({
                'priority': test_case.findtext('priority'),
                'mph': test_case.get('key'),
                'title': test_case.findtext('name'),
                'core_dependency': next(iter(test_case.xpath('customFields/customField[@name="Core Dependent"]/value/text()')), None),
                'labels': ','.join(label.text for label in test_case.xpath('.//labels/label')),
                'testing level': ', '.join(test_case.xpath('customFields/customField[@name="Testing level"]/value/text()') or ["N/A"])
            })
        
        # Export to CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['priority', 'mph', 'title', 'core_dependency', 'labels', 'testing level']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for case in test_cases:
                writer.writerow(case)
        
        print(f"✓ Successfully parsed {len(test_cases)} test cases")
        return csv_file
    
    except Exception as e:
        print(f"Error parsing XML: {str(e)}")
        return None

def analyze_redundancy(csv_file: str, num_clusters: int = 5):
    """Perform redundancy analysis on parsed test cases."""
    try:
        import pandas as pd
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import KMeans
        from sklearn.metrics.pairwise import cosine_similarity
        
        print(f"\nAnalyzing redundancy in: {csv_file}")
        
        # Load and preprocess data
        data = pd.read_csv(csv_file)
        data['title'] = data['title'].str.lower()
        data['labels'] = data['labels'].str.lower()
        
        # Vectorize titles
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(data['title'])
        
        # Cluster test cases
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        data['cluster_id'] = kmeans.fit_predict(tfidf_matrix)
        
        # Calculate similarities
        cosine_sim_matrix = cosine_similarity(tfidf_matrix)
        
        redundancy_results = []
        for cluster_id in data['cluster_id'].unique():
            cluster_cases = data[data['cluster_id'] == cluster_id]
            
            for i in range(len(cluster_cases)):
                for j in range(i + 1, len(cluster_cases)):
                    case_1 = cluster_cases.iloc[i]
                    case_2 = cluster_cases.iloc[j]
                    similarity_score = cosine_sim_matrix[case_1.name, case_2.name]
                    
                    # Apply redundancy criteria
                    if similarity_score >= 0.75 or (
                        similarity_score >= 0.80 and 
                        (case_1['priority'].startswith("1 -") or case_2['priority'].startswith("1 -"))
                    ):
                        redundancy_results.append({
                            "Cluster ID": cluster_id,
                            "Review Status": "Not Started",
                            "Test Case 1 ID (mph)": case_1['mph'],
                            "Test Case 2 ID (mph)": case_2['mph'],
                            "Test Case 1 Title": case_1['title'],
                            "Test Case 2 Title": case_2['title'],
                            "Test Case 1 Priority": case_1['priority'],
                            "Test Case 2 Priority": case_2['priority'],
                            "Test Case 1 Core Dependency": case_1['core_dependency'],
                            "Test Case 2 Core Dependency": case_2['core_dependency'],
                            "Test Case 1 Labels": case_1['labels'],
                            "Test Case 2 Labels": case_2['labels'],
                            "Test Case 1 Testing Level": case_1['testing level'],
                            "Test Case 2 Testing Level": case_2['testing level'],
                            "Similarity Score": similarity_score,
                            "Reason for Redundancy": "Functional overlap",
                            "Resolution": "Keep both",
                            "To Remove": ""
                        })
        
        # Save results
        output_file = f"redundancy_analysis_{os.path.splitext(os.path.basename(csv_file))[0]}.csv"
        pd.DataFrame(redundancy_results).to_csv(output_file, index=False)
        print(f"✓ Analysis complete! Found {len(redundancy_results)} potential redundancies")
        print(f"✓ Results saved to: {output_file}")
        return True
    
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return False

def main():
    """Main function to run the test case analysis pipeline."""
    print("Test Case Analysis Tool")
    print("======================")
    
    # Check/install dependencies
    check_and_install_dependencies()
    
    # Get input file
    while True:
        print("\nPlease place your XML file in the same folder as this script.")
        xml_file = input("Enter the name of your XML file (e.g., 'test-cases.xml'): ").strip()
        
        if os.path.exists(xml_file):
            break
        print("File not found. Please make sure the file exists and try again.")
    
    # Parse XML
    csv_file = parse_test_cases(xml_file)
    if not csv_file:
        print("Failed to parse XML file. Please check the file and try again.")
        return
    
    # Wait briefly to ensure file is written
    time.sleep(1)
    
    # Perform analysis
    success = analyze_redundancy(csv_file)
    if success:
        print("\nAnalysis completed successfully!")
    else:
        print("\nAnalysis failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
