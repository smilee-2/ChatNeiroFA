from g4f.client import AsyncClient
from g4f.providers.retry_provider import RetryProvider
from g4f.Provider import OpenaiChat, Gemini, DDG, Blackbox, GizAI, Mhystical, DarkAI
import g4f.debug
import asyncio


async def gpts(msg):
    g4f.debug.logging = True
    g4f.debug.version_check = False

    print(msg)
    client = AsyncClient(
        provider=RetryProvider([Blackbox, GizAI, DDG, Mhystical, DarkAI], shuffle=False)
    )
    response = await client.chat.completions.create(
        model="",
        messages=[
            {
                "role": "user",
                "content": f"{msg}"
            }
        ]
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

