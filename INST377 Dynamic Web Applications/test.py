import os
import re
import pandas as pd
from bs4 import BeautifulSoup

root_directory = '/Users/happy1claire/Desktop/inst377-lab-2-submissions'

def parse_student_name(file_path):
    with open(file_path, 'r', encoding='utf-8') as md_file:
        content = md_file.read()
    pattern = r'# Name \(Please Input your name\):([\w\s]+)'
    matches = re.search(pattern, content)
    if matches:
        student_name = ' '.join(matches.group(1).strip().split()[-2:])
        return ', '.join(reversed(student_name.split()))
    return None

def extract_css_styles(soup):
    """Extract styles from <style> tags and inline attributes."""
    styles = ""
    for style in soup.find_all('style'):
        styles += style.get_text()
    return styles

def check_css_properties(css_content, property_name):
    """Check for the presence of a CSS property in the given CSS content."""
    return property_name in css_content

def check_page_requirements(html_file_path, css_file_path=None):
    score = 0
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Extract CSS from <style> tags and inline attributes
    css_content = extract_css_styles(soup)
    
    # Include external CSS file content if available
    if css_file_path:
        with open(css_file_path, 'r', encoding='utf-8') as css_file:
            css_content += css_file.read()

    # HTML Checks
    form = soup.find('form')
    if form and form.get('action') and 'page2.html' in form['action']:
        score += 3
    if form and form.find('input', {'type': 'text', 'required': True}):
        score += 2
    if form and form.find('input', {'type': 'submit'}):
        score += 1
    if form and form.find('label'):
        score += 2

    # CSS Checks
    if check_css_properties(css_content, 'background-color'):
        score += 1
    if check_css_properties(css_content, '.submit-button') and check_css_properties(css_content, 'margin'):
        score += 3
    if check_css_properties(css_content, ':hover'):
        score += 6
    if check_css_properties(css_content, 'div') and check_css_properties(css_content, 'margin'):
        score += 4

    # Page 2 Specific Checks
    if soup.find('h1', style=lambda value: 'text-align: center' in value):
        score += 2
    if any('width: 50%' in img['style'] and 'margin: auto' in img['style'] for img in soup.find_all('img', style=True)):
        score += 4

    return score

def grading(root_directory, grade_book):
    for subdir, dirs, files in os.walk(root_directory):
        html_file_path = css_file_path = student_name = None
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(subdir, file)
                student_name = parse_student_name(file_path)
            elif file.endswith('.html'):
                html_file_path = os.path.join(subdir, file)
            elif file.endswith('.css'):
                css_file_path = os.path.join(subdir, file)

        if student_name and html_file_path:
            score = check_page_requirements(html_file_path, css_file_path)
            # Update the DataFrame with scores
            grade_book.loc[grade_book['Student'].str.contains(student_name, case=False, na=False), 'lab2_score'] = score
            print(f"Updated {student_name}'s score to {score}")

    # Save the updated DataFrame to CSV
    grade_book.to_csv('/Users/happy1claire/Desktop/updated_grade_book.csv', index=False)

# Load the grade book
grade_book_path = '/Users/happy1claire/Desktop/inst377-lab-2-submissions/2024-02-18T0216_Grades-INST377.csv'
grade_book = pd.read_csv(grade_book_path)
grade_book['lab2_score'] = 0  # Initialize a column for lab scores

grading(root_directory, grade_book)
