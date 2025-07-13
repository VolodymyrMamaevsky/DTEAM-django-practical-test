from typing import Any

from django.template.loader import render_to_string
from weasyprint import HTML


def generate_pdf(template_name: str, context: dict[str, Any], output_path: str) -> None:
    context["pdf"] = True
    html_content = render_to_string(template_name, context)
    HTML(string=html_content).write_pdf(output_path)
