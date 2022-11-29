import os

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
    body_code += "</div><div class='body_para'>"
    for key in para:
        body_code += create_body_line(para[key])
    body_code += "</div><div class='body_footer'>"
    for key in footer:
        body_code += create_body_line(footer[key])
    body_code += "</div>"
    return body_code


def create_footer_line(body_footer_line):
    text = body_footer_line["text"]
    style_class = body_footer_line["_style_class_"]
    body_code = f"<p class={style_class}>{text}</p>"
    return body_code


def html_tag(html, head):
    html_code = str(html)
    html_code += str(head)
    return html_code


def body_tag(body):
    body_header = body["header"]
    body_section = body["body_section"]
    body_footer = body["body_footer"]
    body_code = "<body><div class='header'>"
    for key in body_header:
        body_code += create_header_line(body_header[key])
    body_code += "</div><div class='body_section'>"
    body_code += create_body_section_line(body_section)
    body_code += "</div><div class='footer_section'>"
    for key in body_footer:
        body_code += create_footer_line(body_footer[key])
    body_code += "</div></body>"
    return body_code


def json_to_html(data):
    html = data["html"]
    head = data["head"]["title"]
    body = data["body"]
    header_code = html_tag(html, head)
    body_code = body_tag(body)
    code = header_code + body_code + "</html>"
    # print(code)

    return code


def create_html_file(code):
    message = f"""{code}"""
    with open("template.html", "a") as filen:
        filen.write(code)
        filen.close()


def mapping_param(data):
    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)

    html_template = "template.html"
    template = template_env.get_template(html_template)
    output_text = template.render(data)
    return output_text


def JSONtoPDF(path):
    json_data = []
    with open(path) as json_file:
        json_data = json.load(json_file)
    code = ""
    for item in json_data:
        code += json_to_html(item)
    #     print(code)
    # create_html_file(code)

    # f = open("mapping.json", "r")
    # data = json.loads(f.read())
    # output_text = mapping_param(data)
    config = pdfkit.configuration(
        wkhtmltopdf="C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe"
    )
    output_pdf = "pdf_generated.pdf"
    pdfkit.from_string(
        code, output_pdf, configuration=config, css="style.css", options=option
    )


def mapping_files():
    cwd = os.getcwd()
    path = os.path.join(cwd, "templates")
    dir_list = os.listdir(path)
    for folder_name in dir_list:
        template_path = os.path.join(path, folder_name)
        for file_name in os.listdir(template_path):
            if file_name.endswith(".json"):
                path_to_json = os.path.join(template_path, file_name)
                JSONtoPDF(path_to_json)
                flag = 1
        if flag == 1:
            break


mapping_files()
