#!/usr/bin/env python3
import os
import re
import markdown
import frontmatter
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from pathlib import Path

class MermaidPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        is_mermaid = False
        mermaid_lines = []
        
        for line in lines:
            if line.strip() == '```mermaid':
                is_mermaid = True
                mermaid_lines = []
                new_lines.append('<div class="mermaid">')
                continue
            elif is_mermaid and line.strip() == '```':
                is_mermaid = False
                new_lines.append('</div>')
                continue
            elif is_mermaid:
                new_lines.append(line)
            else:
                new_lines.append(line)
                
        return new_lines

class MermaidExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(MermaidPreprocessor(md), 'mermaid', 175)

class BookConverter:
    def __init__(self, book_dir="enterprise_data_architecture"):
        self.book_dir = book_dir
        self.chapters_dir = os.path.join(book_dir, "chapters")
        self.output_dir = os.path.join(book_dir, "output")
        self.html_dir = os.path.join(self.output_dir, "html")
        self.templates_dir = os.path.join(book_dir, "templates")
        
        # Create output directories
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.html_dir, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        
        # Initialize Markdown converter with extensions
        self.md = markdown.Markdown(extensions=[
            'meta',
            'toc',
            'tables',
            'fenced_code',
            MermaidExtension(),
            'attr_list'
        ])

        # Get book title from README.md
        readme_path = os.path.join(book_dir, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, 'r') as f:
                content = f.read()
                post = frontmatter.loads(content)
                # Try to find the title in the first h1 heading if not in frontmatter
                if hasattr(post, 'title'):
                    self.book_title = post.title
                else:
                    h1_match = re.search(r'#\s+(.+)$', content, re.MULTILINE)
                    if h1_match:
                        self.book_title = h1_match.group(1).strip()
                    else:
                        self.book_title = "Enterprise Data Architecture Guide"
        else:
            self.book_title = "Enterprise Data Architecture Guide"

    def create_templates(self):
        """Create template files if they don't exist"""
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Base template with improved styling
        base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #34495e;
            --background-color: #ffffff;
            --code-background: #f6f8fa;
            --border-color: #ddd;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
            color: var(--primary-color);
            background-color: var(--background-color);
        }
        
        h1, h2, h3, h4 { 
            color: var(--primary-color);
            margin-top: 2em;
            margin-bottom: 1em;
        }
        
        h1 { font-size: 2.5em; }
        h2 { font-size: 2em; }
        h3 { font-size: 1.5em; }
        
        code { 
            background-color: var(--code-background);
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        }
        
        pre {
            background-color: var(--code-background);
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid var(--border-color);
        }
        
        .mermaid {
            background-color: white;
            padding: 1em;
            border-radius: 5px;
            margin: 2em 0;
            text-align: center;
        }
        
        img {
            max-width: 100%;
            height: auto;
            margin: 2em 0;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 2em 0;
        }
        
        th, td {
            border: 1px solid var(--border-color);
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: var(--code-background);
            font-weight: 600;
        }
        
        blockquote {
            border-left: 4px solid var(--secondary-color);
            margin: 1.5em 0;
            padding: 0.5em 1em;
            color: var(--secondary-color);
            background-color: var(--code-background);
        }
        
        @media print {
            body { max-width: none; }
            pre, code { white-space: pre-wrap; }
            .mermaid { page-break-inside: avoid; }
            h1, h2, h3 { page-break-after: avoid; }
            img, table { page-break-inside: avoid; }
        }
    </style>
</head>
<body>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: { curve: 'basis' }
        });
    </script>
    {{ content }}
</body>
</html>
"""
        base_template_path = os.path.join(self.templates_dir, "base.html")
        if not os.path.exists(base_template_path):
            with open(base_template_path, "w") as f:
                f.write(base_template)

    def convert_markdown_to_html(self, content):
        """Convert markdown content to HTML"""
        return self.md.convert(content)

    def process_single_file(self, file_path):
        """Process a single markdown file"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse frontmatter if exists
        post = frontmatter.loads(content)
        content = post.content
        
        # Convert markdown to HTML
        html_content = self.convert_markdown_to_html(content)
        
        # Render with template
        template = self.env.get_template("base.html")
        title = os.path.basename(file_path).replace('.md', '').replace('_', ' ').title()
        if title.lower() == 'readme':
            title = self.book_title
        rendered_html = template.render(title=f"{title} - {self.book_title}", content=html_content)
        
        return rendered_html

    def process_book(self):
        """Process all markdown files and generate HTML and PDF"""
        print("Starting book conversion process...")
        
        # First, create necessary templates
        self.create_templates()
        print("Created templates...")
        
        # Read README.md first
        readme_path = os.path.join(self.book_dir, "README.md")
        readme_html = ""
        if os.path.exists(readme_path):
            readme_html = self.process_single_file(readme_path)
            print("Processed README.md...")
        
        # Process all chapter files in order
        chapter_contents = []
        for i in range(1, 11):
            chapter_file = f"{i:02d}_"
            chapter_files = [f for f in os.listdir(self.chapters_dir) if f.startswith(chapter_file)]
            
            if chapter_files:
                file_path = os.path.join(self.chapters_dir, chapter_files[0])
                chapter_html = self.process_single_file(file_path)
                chapter_contents.append(chapter_html)
                print(f"Processed chapter {i}...")
        
        # Combine all HTML content
        full_html = readme_html + "\n".join(chapter_contents)
        
        # Generate filenames with book title
        safe_title = self.book_title.lower().replace(' ', '_').replace(':', '').replace('-', '_')
        html_output = os.path.join(self.html_dir, f"{safe_title}.html")
        pdf_output = os.path.join(self.output_dir, f"{safe_title}.pdf")
        
        # Save combined HTML
        with open(html_output, "w") as f:
            f.write(full_html)
        print(f"Generated HTML version: {html_output}")
        
        # Generate PDF
        HTML(string=full_html).write_pdf(pdf_output)
        print(f"Generated PDF version: {pdf_output}")
        
        print("Book conversion completed successfully!")

if __name__ == "__main__":
    converter = BookConverter()
    converter.process_book()