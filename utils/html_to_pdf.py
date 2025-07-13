import asyncio

from django.template.loader import render_to_string
from playwright.async_api import async_playwright


async def render_pdf_from_template(context: dict, template_name: str, output_path: str):
    context["pdf"] = True
    html_content = render_to_string(template_name, context)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content, wait_until="load")
        await page.pdf(path=output_path, format="A4")
        await browser.close()


def generate_pdf(template_name: str, context: dict, output_path: str):
    asyncio.run(render_pdf_from_template(context, template_name, output_path))
