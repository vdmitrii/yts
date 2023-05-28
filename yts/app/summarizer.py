import os

import openai
from app.models.tortoise import TextSummary
from dotenv import find_dotenv, load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv(find_dotenv())
OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY


# TODO: add corner cases -> https://www.youtube.com/embed/zUES9s-yNl8
def get_id(url):
    import re

    pattern = re.compile("v=([A-Za-z0-9]+)")
    res = pattern.findall(url)
    return res[0]


# TODO: process situations then there is no have a subtitles
def generate_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id, languages=["en"])
    # transcript = transcript_list.find_transcript(['en'])
    # translated_transcript = transcript.translate('de')
    # print(translated_transcript.fetch())
    script = ""
    for text in transcript:
        t = text["text"]
        if t != "[Music]":
            script += t + " "
    return script, len(script.split())


@retry(wait=wait_random_exponential(min=23, max=31), stop=stop_after_attempt(6))
def completion_with_backoff(text):
    messages = [
        {
            "role": "system",
            "content": """Your main role is to provide clear and informative summaries of text provided by the user. Return the results in markdown format.""",
        },
        {
            "role": "user",
            "content": f"""Please create a comprehensive bullet-point summary with a two-level structure for the following text: {text}""",
        },
    ]
    # messages = f"Please create a comprehensive bullet-point summary with a two-level structure for the following text: {text}"
    # content = "To summarize: " + "\n\n" + content # TL;DR"
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        # temperature=0.5,
    )
    result = res["choices"][0]["message"]["content"]
    return result


async def generate_summary(summary_id: int, url: str) -> None:
    yt_id = get_id(url)
    transcript, _ = generate_transcript(yt_id)
    summary = completion_with_backoff(transcript)
    await TextSummary.filter(id=summary_id).update(summary=summary)
    # return summary
