# utils/pdf_generator.py
from jinja2 import Environment, FileSystemLoader
import pdfkit
import os

def generate_pdf(template_name, data, output_path):
    # Load template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    html_out = template.render(**data)

    # PDF config
    try:
        config = pdfkit.configuration()
    except:
        # Point to your install path
        config = pdfkit.configuration(wkhtmltopdf=r'D:\wkhtmltox\bin\wkhtmltopdf.exe')

    # Generate PDF
    pdfkit.from_string(html_out, output_path, configuration=config)
    return output_path