from openai import OpenAI

from CVProject import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def translate_text(text: str, target_lang: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate the following text to {target_lang}."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content.strip()
