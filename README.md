# Book Standards

## Markdown File Naming Convention
- Each chapter markdown file should follow the naming convention: `chapterX_title.md`, where `X` is the chapter number.

## Chapter Titles
- Each chapter markdown file must start with a title in the format: `# Chapter X: Title`, where `X` is the chapter number and `Title` is the chapter name.

## Table of Contents
- The Table of Contents (TOC) in the generated HTML should include two levels:
  - Chapter level (e.g., Chapter 1: Introduction)
  - Subsections within each chapter (if applicable).

## HTML Output Standards
- Each chapter in the HTML output must have:
  - A unique ID in the format `chapter-X`.
  - A title in the format `Chapter X: Title`.

## Example

### Markdown File
```markdown
# Chapter 1: Introduction

Content of the chapter...
```

### HTML Output
```html
<section id="table-of-contents">
  <h2>Table of Contents</h2>
  <nav>
    <ul>
      <li><a href="#chapter-1">Chapter 1: Introduction</a></li>
      <li><a href="#chapter-2">Chapter 2: Technological Foundations</a></li>
    </ul>
  </nav>
</section>

<div id="chapter-1" class="chapter">
  <h2>Chapter 1: Introduction</h2>
  <p>Content of the chapter...</p>
</div>
```


