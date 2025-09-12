import json
import os
from Portfolio.generator import generate_portfolio

def test_portfolio_generation():
    """Test portfolio generation using sample data"""
    
    # Load sample data
    with open('data/sample-data.json', 'r', encoding='utf-8') as f:
        sample_data = json.load(f)
    
    print("Sample data loaded:")
    print(f"Name: {sample_data.get('name')}")
    print(f"Projects: {len(sample_data.get('projects', []))}")
    print(f"Skills: {len(sample_data.get('skills', []))}")
    
    # Fix the data structure to match what the generator expects
    # The generator expects 'experiences' but sample data has 'experience'
    if 'experience' in sample_data:
        sample_data['experiences'] = sample_data['experience']
    
    try:
        print("\nGenerating portfolio...")
        html_content = generate_portfolio(sample_data)
        
        print("[SUCCESS] Portfolio generated successfully!")
        print(f"HTML content length: {len(html_content)} characters")
        
        # Check if output file was created
        output_path = os.path.join("output", "portfolio.html")
        if os.path.exists(output_path):
            print(f"[SUCCESS] Portfolio saved to: {output_path}")
            
            # Get file size
            file_size = os.path.getsize(output_path)
            print(f"File size: {file_size} bytes")
        else:
            print("[ERROR] Output file not found")
            
    except Exception as e:
        print(f"[ERROR] Error generating portfolio: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_portfolio_generation()