try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from CVProject import settings


def translate_text(text: str, target_lang: str) -> str:
    if not OPENAI_AVAILABLE:
        return f"[OpenAI API not available. Translation to {target_lang} is not possible.]"

    if not settings.OPENAI_API_KEY:
        return f"[OpenAI API key not configured. Translation to {target_lang} is not possible.]"

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Translate the following text to {target_lang}."},
                {"role": "user", "content": text},
            ],
        )
        content = response.choices[0].message.content
        return content.strip() if content else f"[Empty response from OpenAI for {target_lang}]"
    except Exception as e:
        return f"[Translation error to {target_lang}: {e!s}]"
