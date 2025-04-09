#!/usr/bin/env python3

import os
import markdown
import traceback
import sys
import argparse

def convert_book_to_html(book_dir, output_dir=None, version="v1.0"):
    """
    Convert a book directory containing Markdown files to a single HTML file.
    
    Parameters:
    - book_dir: Directory containing the Markdown files of the book
    - output_dir: Directory to save the output HTML file (defaults to "output" in the parent directory)
    - version: Version string to include in the HTML title
    
    Returns:
    - Path to the generated HTML file
    """
    try:
        # Extract book title from directory name
        book_name = os.path.basename(book_dir)
        book_title = book_name.replace('_', ' ').title()
        
        # Set default output directory if not provided
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(os.path.abspath(book_dir)), "output")
        
        # Create output filename from book directory name
        output_file = os.path.join(output_dir, f"{book_name}_{version.replace('.', '_')}.html")
        
        print(f"Starting conversion of '{book_title}' to HTML...", file=sys.stderr)
        print(f"Book directory: {book_dir}", file=sys.stderr)
        print(f"Output file: {output_file}", file=sys.stderr)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        all_content = []
        
        # Process README first
        readme_path = os.path.join(book_dir, "README.md")
        if os.path.exists(readme_path):
            print(f"Reading README.md...", file=sys.stderr)
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Process mermaid diagrams
            readme_content = process_mermaid(readme_content)
            
            # Convert markdown to HTML
            readme_html = markdown.markdown(
                readme_content,
                extensions=['extra', 'tables', 'fenced_code']
            )
            all_content.append(readme_html)
            print("✓ Processed README.md", file=sys.stderr)
        
        # Find all numbered chapter files
        chapter_files = []
        for filename in os.listdir(book_dir):
            if filename.endswith('.md') and filename != "README.md" and (filename[0].isdigit() or (filename.startswith('chapter') and len(filename) > 7 and filename[7].isdigit())):
                chapter_files.append(filename)
        
        chapter_files.sort()  # Sort by filename
        print(f"Found {len(chapter_files)} chapter files: {chapter_files}", file=sys.stderr)
        
        # Simple table of contents
        toc_html = "<h2>Table of Contents</h2><ol>"
        for filename in chapter_files:
            chapter_name = filename.replace('.md', '').replace('_', ' ').title()
            # Clean up chapter names by removing numeric prefixes
            parts = chapter_name.split(' ')
            if parts[0].replace('.', '').isdigit():
                chapter_name = ' '.join(parts[1:])
            toc_html += f'<li><a href="#{filename}">{chapter_name}</a></li>'
        toc_html += "</ol>"
        all_content.append(toc_html)
        
        # Process each chapter
        for filename in chapter_files:
            file_path = os.path.join(book_dir, filename)
            print(f"Processing {filename}...", file=sys.stderr)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                chapter_content = f.read()
            
            # Process mermaid diagrams
            chapter_content = process_mermaid(chapter_content)
            
            # Convert markdown to HTML
            chapter_html = f'<div id="{filename}" class="chapter">'
            chapter_html += markdown.markdown(
                chapter_content,
                extensions=['extra', 'tables', 'fenced_code']
            )
            chapter_html += '</div>'
            all_content.append(chapter_html)
            print(f"✓ Processed {filename}", file=sys.stderr)
        
        # Combine all content
        full_content = "\n".join(all_content)
        
        # Create final HTML
        final_html = HTML_TEMPLATE.format(
            title=book_title,
            version=version,
            content=full_content
        )
        
        # Write to file
        print(f"Writing HTML output to {output_file}...", file=sys.stderr)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"\nSUCCESS! HTML book generated at: {output_file}", file=sys.stderr)
        return output_file
        
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return None

def process_mermaid(content):
    """Process Mermaid code blocks in markdown content"""
    lines = content.split('\n')
    processed_lines = []
    in_mermaid = False
    
    for line in lines:
        if line.strip() == '```mermaid':
            in_mermaid = True
            processed_lines.append('<div class="mermaid">')
            continue
        elif in_mermaid and line.strip() == '```':
            in_mermaid = False
            processed_lines.append('</div>')
            continue
        else:
            processed_lines.append(line)
    
    return '\n'.join(processed_lines)

# HTML template with enhanced styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {version}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            color: #2c3e50;
        }}
        .mermaid {{
            background-color: white;
            padding: 1em;
            margin: 2em 0;
            text-align: center;
            border: 1px solid #eee;
            border-radius: 5px;
        }}
        pre {{
            background-color: #f6f8fa;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.9em;
            background-color: rgba(27, 31, 35, 0.05);
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 2em 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f6f8fa;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }}
        h1 {{
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3rem;
        }}
        .chapter {{
            margin-top: 3rem;
            border-top: 1px solid #eee;
            padding-top: 2rem;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        blockquote {{
            border-left: 4px solid #dfe2e5;
            padding: 0 1em;
            color: #6a737d;
            margin: 0 0 16px;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
</head>
<body>
    <h1>{title} - {version}</h1>
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                securityLevel: 'loose'
            }});
        }});
    </script>
    {content}
</body>
</html>
"""

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Convert a book directory of Markdown files to a single HTML file.')
    parser.add_argument('book_dir', help='Directory containing the Markdown files of the book')
    parser.add_argument('-o', '--output-dir', help='Directory to save the output HTML file (defaults to "output" in the parent directory)')
    parser.add_argument('-v', '--version', default='v1.0', help='Version string to include in the HTML title (default: v1.0)')
    
    args = parser.parse_args()
    
    # Convert the book
    output_file = convert_book_to_html(args.book_dir, args.output_dir, args.version)
    
    if output_file:
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
