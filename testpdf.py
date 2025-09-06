import pdfkit

# Point to your wkhtmltopdf executable
path_wkhtmltopdf = r"D:\wkhtmltox\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

pdfkit.from_string('<h1>Hello</h1>', 'out.pdf', configuration=config)
