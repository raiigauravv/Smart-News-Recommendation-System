# Mock PDF utils for testing
import tempfile
import os

def create_news_report(articles, filename="mock_report.pdf"):
    """Mock PDF generation function"""
    print(f"Mock: Creating PDF report with {len(articles)} articles")
    
    # Create a temporary file path
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    # Create a simple text file instead of PDF for testing
    with open(file_path, 'w') as f:
        f.write("Mock News Report\n")
        f.write("================\n\n")
        for i, article in enumerate(articles, 1):
            f.write(f"{i}. {article.get('title', 'No Title')}\n")
            f.write(f"   {article.get('abstract', 'No Abstract')}\n\n")
    
    return file_path