import logging
from groq import Groq
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def call_llm(messages: list) -> str:
    try:
        client = Groq(api_key=settings.LLM_API_KEY)
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=messages,
            temperature=0.1,
            max_tokens=300
        )
        answer = response.choices[0].message.content.strip()
        logger.info("LLM responded successfully")
        return answer
    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        raise RuntimeError(f"LLM service error: {str(e)}")