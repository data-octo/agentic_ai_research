# Airline Agentic AI Series

Welcome to the **Airline Agentic AI Series** repository. This series explores the transformative potential of Agentic AI in revolutionizing airline operations, workforce dynamics, and customer experiences.

## Author
**Tedd Yuan**  
An expert in AI-driven transformations, Tedd Yuan specializes in leveraging Agentic AI to drive innovation and efficiency in the aviation industry.

---

## List of Books

### 1. [Airline Agentic AI Transformation](1_airline_agentic_ai_transformation/)
**Summary:** This book introduces the concept of Agentic AI and its applications in transforming airline operations. It covers technological foundations, implementation strategies, and future trends.

### 2. [Airline Agentic AI Digital Workforce](2_airline_agentic_ai_digital_workforce/)
**Summary:** Focuses on building a digital workforce in aviation using Agentic AI. It discusses IT strategies, governance, and case studies.

### 3. [Airline Agentic AI Modern Data Architecture](3_airline_agentic_ai_modern_data_architecture/)
**Summary:** Explores modern data architecture for airlines, including data fabric, data mesh, and customer experience transformation with Agentic AI.

### 4. [Airline Enterprise Data Architecture Transformation](4_airline_enterprise_data_architecture_transform/)
**Summary:** Provides a comprehensive guide to transforming enterprise data architecture in airlines, with a focus on domain-driven design and implementation strategies.

### 5. [Airline Agentic AI Digital Sales Transformation](5_airline_agentic_ai_digital_sales_transformation/)
**Summary:** Examines the role of Agentic AI in transforming digital sales for airlines, including challenges, ethics, and future trends.

---

## How to Use the Python Script

The `convert_book_to_html.py` script allows you to generate HTML output for each book in the series.

### Steps to Generate HTML Output
1. Ensure you have Python installed on your system.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script for a specific book:
   ```bash
   python convert_book_to_html.py <book_folder> -o <output_folder> -v <version>
   ```
   - `<book_folder>`: Path to the book folder (e.g., `1_airline_agentic_ai_transformation`)
   - `<output_folder>`: Directory to save the generated HTML file (e.g., `docs`)
   - `<version>`: Version string to include in the HTML title (e.g., `v1.0`)

### Example
To generate HTML for the first book:
```bash
python convert_book_to_html.py 1_airline_agentic_ai_transformation -o docs -v v1.0
```

---

## Repository Structure
- **`convert_book_to_html.py`**: Python script to convert book markdown files to HTML.
- **`requirements.txt`**: List of Python dependencies.
- **`docs/`**: Directory containing generated HTML files.
- **`templates/`**: HTML templates for styling the output.
- **`<book_folders>/`**: Each folder contains markdown files for a specific book.

---

## Book Folder Structure

To maintain consistency across all books in the series, follow this folder structure when creating a new book:

```
<book_folder>/
    README.md                # Overview of the book
    chapters/                # Directory containing all chapter markdown files
        01_introduction.md   # Chapter 1: Introduction
        02_chapter_title.md  # Chapter 2: Title
        ...                  # Additional chapters
```

### Naming Conventions
- **Book Folder:** Use a numeric prefix followed by a descriptive name (e.g., `6_new_book_title`).
- **Chapter Files:** Use a numeric prefix followed by an underscore and a descriptive name (e.g., `01_introduction.md`).
- **README.md:** Provide an overview of the book, including its purpose, target audience, and key topics.

### Example
For a new book titled "Airline AI Innovations":
```
6_airline_ai_innovations/
    README.md
    chapters/
        01_introduction.md
        02_ai_in_aviation.md
        03_future_trends.md
```

This structure ensures that all books are organized consistently and can be easily processed by the Python script.

---

## License
This repository is licensed under the MIT License. See the LICENSE file for details.


