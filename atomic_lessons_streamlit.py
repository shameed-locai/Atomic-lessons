"""
app.py
"""
import streamlit as st
import asyncio
from openai import AsyncOpenAI
from youtube_transcript_api import YouTubeTranscriptApi

try:
  client = AsyncOpenAI(api_key="OPENAI_KEY")
except:
  client = AsyncOpenAI()

st.set_page_config(
    page_title="OpenAI Async Stream Demo",
    layout="wide",
)


st.title("Demo: Atomic Lessons")
with st.sidebar:
    vlink = st.text_input("Youtube video link")
    generate = st.button("Generate")


col1 = st.columns(1)[0]

essay_1 = col1.empty()
# essay_2 = col2.empty()

async def generate_essay(placeholder):

    stream = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are an AI Quiz generation that takes youtube subtitles JSON as input "
                                                "and divides the video into logical sections and creates quizzes with 4 questions for each section."
                                                "Provide only the quizzes in the output"},
                  {"role": "user", "content": str(txt)},],
        stream=True
    )
    streamed_text = "# "
    async for chunk in stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            streamed_text = streamed_text + chunk_content
            placeholder.info(streamed_text)

async def main():
    await asyncio.gather(
        generate_essay(essay_1),
        # generate_essay(essay_2, topic=topic_2, word_count=word_count)
    )

if generate:
    if vlink == "":
        st.warning("Please enter both topics")
    else:
      txt = YouTubeTranscriptApi.get_transcript(vlink.split("=")[1])
      asyncio.run(main())