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


def create_header_line(body_header_key):
    text = body_header_key["text"]
    style_class = body_header_key["_style_class_"]
    body_code = f"<h1 class={style_class}>{text}</h1>"
    return body_code


def create_body_line(body_header_key):
    text = body_header_key["text"]
    style_class = body_header_key["_style_class_"]
    if text == "br":
        return "<br />"
    body_code = f"<p class={style_class}>{text}</p>"
    return body_code


def create_body_section_line(body_section_key):
    header = body_section_key["body_header"]
    para = body_section_key["body_para"]
    footer = body_section_key["body_footer"]
    body_code = "<div class='body_header'>"
    for key in header:
        body_code += create_body_line(header[key])
    body_code = "</div>"
    for key in para:
        body_code += create_body_line(para[key])
    body_code = "</div>"
    return body_code


def html_tag(html, head):
    html_code = str(html)
    html_code += str(head)
    return html_code


def body_tag(body):
    body_header = body["header"]
    body_section = body["body_section"]
    body_code = "<body><div class='header'>"
    for key in body_header:
        body_code += create_header_line(body_header[key])
    body_code += "</div><div class='body_section'>"
    body_code += create_body_section_line(body_section)
    body_code += "</div></body>"
    return body_code


def mapping(data):
    html = data["html"]
    head = data["head"]["title"]
    body = data["body"]
    header_code = html_tag(html, head)
    body_code = body_tag(body)

    print(body_code)
    code = header_code + body_code + "</html>"
    return code


def JSONtoPDF():
    f = open("test\data.json", "r")
    data = json.loads(f.read())
    code = mapping(data)
    config = pdfkit.configuration(
        wkhtmltopdf="C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe"
    )
    output_pdf = "test\pdf_generated.pdf"
    pdfkit.from_string(
        code, output_pdf, configuration=config, css="style.css", options=option
    )


JSONtoPDF()
