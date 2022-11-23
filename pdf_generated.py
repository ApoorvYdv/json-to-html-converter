import jinja2
import pdfkit

import json

option = {
    "page-size": "A4",
    "margin-top": "0.75in",
    "margin-right": "1in",
    "margin-bottom": "0.75in",
    "margin-left": "1in",
}


def mapping():
    f = open("data.json", "r")
    data = json.loads(f.read())
    JSONtoPDF(data)


def JSONtoPDF(context):
    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)

    html_template = "template.html"
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    config = pdfkit.configuration(
        wkhtmltopdf="C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe"
    )
    output_pdf = "pdf_generated.pdf"
    pdfkit.from_string(
        output_text, output_pdf, configuration=config, css="style.css", options=option
    )


mapping()
