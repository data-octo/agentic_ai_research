#!/usr/bin/env python

import os
import markdown
import traceback
import sys
import argparse
import re

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

        # Initialize chapter_files list and populate it with chapter files
        chapter_files = []

        # Find all chapter files in both root and chapters/ directory if it exists
        # Check root directory for chapter files
        for filename in os.listdir(book_dir):
            filepath = os.path.join(book_dir, filename)
            if os.path.isfile(filepath) and filename.endswith('.md') and filename != "README.md" and (
                    filename[0].isdigit() or (filename.startswith('chapter') and len(filename) > 7 and filename[7].isdigit())):
                chapter_files.append((filepath, filename))

        # Check if a chapters/ directory exists and process files there too
        chapters_dir = os.path.join(book_dir, "chapters")
        if os.path.exists(chapters_dir) and os.path.isdir(chapters_dir):
            print(f"Found chapters/ directory, checking for markdown files...", file=sys.stderr)
            for filename in os.listdir(chapters_dir):
                filepath = os.path.join(chapters_dir, filename)
                if os.path.isfile(filepath) and filename.endswith('.md') and filename != "README.md" and (
                        filename[0].isdigit() or (filename.startswith('chapter') and len(filename) > 7 and filename[7].isdigit())):
                    chapter_files.append((filepath, filename))

        # Sort chapter files using a natural sort to handle numeric prefixes correctly
        def natural_sort_key(file_info):
            filepath, filename = file_info
            # Extract numeric prefix if it exists
            match = re.match(r'^(?:chapter)?(\d+)[\._]', filename)
            if match:
                return int(match.group(1)), filename
            return 999, filename  # Files without numeric prefix go at the end

        chapter_files.sort(key=natural_sort_key)
        print(f"Found {len(chapter_files)} chapter files: {[f for _, f in chapter_files]}", file=sys.stderr)

        # Process README first
        readme_path = os.path.join(book_dir, "README.md")
        if os.path.exists(readme_path):
            print(f"Reading README.md...", file=sys.stderr)
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()

            # Process mermaid diagrams
            readme_content = process_mermaid(readme_content)

            # Remove any existing TOC from README content
            readme_content = re.sub(r'(?s)^\s*#\s*Table of Contents.*?(?=\n#|\Z)', '', readme_content, flags=re.IGNORECASE)
            book_title = re.search(r'#\s*(.*?)\s*$', readme_content, re.MULTILINE).group(1).strip()
            # Convert markdown to HTML
            readme_html = markdown.markdown(
                readme_content,
                extensions=['extra', 'tables', 'fenced_code']
            )
            all_content.append(readme_html)
            print("✓ Processed README.md", file=sys.stderr)
        
        # Generate Table of Contents (TOC) with consistent numbering and links
        toc_items = []
        for idx, (filepath, filename) in enumerate(chapter_files, start=1):
            chapter_title = filename.split('.')[0].replace('_', ' ').title()
            chapter_title = re.sub(r'^\d+\s+', '', chapter_title)  # Remove leading numbers from title
            chapter_id = f'chapter-{idx}'  # Use chapter index as ID

            # Add subsections if applicable
            subsections = []
            with open(filepath, 'r', encoding='utf-8') as f:
                subsection_counter = 1
                for line in f:
                    if line.startswith('## '):
                        subsection_title = line[3:].strip()
                        subsection_number = f'{idx}.{subsection_counter}'
                        subsection_id = f'{chapter_id}-{subsection_number.replace(".", "-")}'  # Use subsection number for ID
                        # Avoid duplicate numbering in TOC
                        if not subsection_title.startswith(subsection_number):
                            subsections.append(f'<li><a href="#{subsection_id}">{subsection_number} {subsection_title}</a></li>')
                        else:
                            subsections.append(f'<li><a href="#{subsection_id}">{subsection_title}</a></li>')
                        subsection_counter += 1

            if subsections:
                subsections_html = '\n'.join(subsections)
                toc_items.append(f'<li><a href="#{chapter_id}">Chapter {idx}: {chapter_title}</a><ul>{subsections_html}</ul></li>')
            else:
                toc_items.append(f'<li><a href="#{chapter_id}">Chapter {idx}: {chapter_title}</a></li>')

        toc_content = '\n'.join(toc_items)

        # Append the TOC after the README content with a proper heading and detailed format
        if readme_path:
            detailed_toc = f'''<section id="table-of-contents">
<h1>Table of Contents</h1>
<nav>
<ul>
{toc_content}
</ul>
</nav>
</section>'''
            all_content.append(detailed_toc)

        # Ensure chapter IDs and titles are updated with proper numbering and add two-level numbering inside chapters
        for idx, (filepath, filename) in enumerate(chapter_files, start=1):
            print(f"Processing {filename}...", file=sys.stderr)

            with open(filepath, 'r', encoding='utf-8') as f:
                chapter_content = f.read()

            # Add 'Chapter' and chapter number to the title if not present, and remove duplicate numbers
            chapter_title = filename.split('.')[0].replace('_', ' ').title()
            chapter_title = re.sub(r'^\d+\s+', '', chapter_title)  # Remove leading numbers from title
            if not chapter_content.startswith(f'# Chapter {idx}'):
                chapter_content = f'# Chapter {idx}: {chapter_title}\n\n' + chapter_content

            # Process mermaid diagrams
            chapter_content = process_mermaid(chapter_content)

            # Convert markdown to HTML
            chapter_id = f'chapter-{idx}'
            chapter_html = f'<div id="{chapter_id}" class="chapter">'

            # Ensure unique numbering for subsections
            subsection_counter = 1
            lines = chapter_content.splitlines()
            for i, line in enumerate(lines):
                if line.startswith('## '):
                    subsection_title = line[3:].strip()
                    subsection_number = f'{idx}.{subsection_counter}'
                    subsection_id = f'{chapter_id}-{subsection_number.replace(".", "-")}'  # Use subsection number for ID
                    # Avoid duplicate numbering in the title
                    if not subsection_title.startswith(subsection_number):
                        lines[i] = f'## {subsection_number} {subsection_title} {{#{subsection_id}}}'
                    subsection_counter += 1

            chapter_content = '\n'.join(lines)

            chapter_html += markdown.markdown(
                chapter_content,
                extensions=['extra', 'tables', 'fenced_code']
            )

            chapter_html += '</div>'
            all_content.append(chapter_html)
            print(f"✓ Processed {filename}", file=sys.stderr)

        # Only include the main content
        full_content = "\n".join(all_content)

               # Create final HTML with TOC
        final_html = HTML_TEMPLATE.format(
            title=book_title,  # Title for the <title> tag without version info
            version=version,   # Include version info in the header
            toc=toc_content,   # Table of Contents
            content=full_content  # Main content only
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

# Load the HTML template from an external file
with open(os.path.join(os.path.dirname(__file__), 'templates', 'html_template.html'), 'r', encoding='utf-8') as template_file:
    HTML_TEMPLATE = template_file.read()

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
