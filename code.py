import requests
import re

def fetch_google_doc_text(doc_url):
    """Fetches the text content from a publicly accessible Google Doc."""
    # Handle both direct and published document URLs
    doc_id_match = re.search(r'document/d/([a-zA-Z0-9-_]+)', doc_url)
    if not doc_id_match:
        raise ValueError("Invalid Google Docs URL. Please provide a valid Google Docs URL.")
    
    doc_id = doc_id_match.group(1)
    
    # For published documents, use the export URL
    export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"
    
    try:
        response = requests.get(export_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException("Could not access the Google Doc. Please ensure the document is publicly accessible.")

def decode_unicode_grid(input_data):
    # Parse the input data into coordinates and characters
    lines = input_data.split('\n')
    
    # Remove any empty lines and lines that don't look like data
    lines = [line.strip() for line in lines if line.strip()]
    
    # Create a dictionary to store grid characters
    grid = {}
    
    # Skip the header row
    start_idx = 1  # Skip the header row
    
    # Extract x, character, y coordinates from the table format
    for line in lines[start_idx:]:
        if not line.strip():
            continue
            
        # Split the line by | and remove whitespace
        parts = [part.strip() for part in line.split('|')]
        if len(parts) != 3:
            continue
            
        try:
            x = int(parts[0])
            char = parts[1]
            y = int(parts[2])
            
            # Store the character at its coordinates
            grid[(x, y)] = char
        except ValueError:
            continue
    
    # Find the grid boundaries
    if not grid:
        return
    
    min_x = min(x for x, _ in grid.keys())
    max_x = max(x for x, _ in grid.keys())
    min_y = min(y for _, y in grid.keys())
    max_y = max(y for _, y in grid.keys())
    
    # Create the grid, filling empty spaces with space
    output_grid = []
    for y in range(max_y, min_y - 1, -1):  # Reversed to match the expected orientation
        row = []
        for x in range(min_x, max_x + 1):
            # Get character at this coordinate, or space if not found
            row.append(grid.get((x, y), ' '))
        output_grid.append(''.join(row))
    
    # Print the grid
    for row in output_grid:
        print(row)

# Read from local file
with open('input_data.txt', 'r') as f:
    input_data = f.read()
decode_unicode_grid(input_data)