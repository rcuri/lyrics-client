import asyncio
import json
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from openai import OpenAI
from dotenv import load_dotenv

import re

load_dotenv()

class LyricsClient:
    def __init__(self, model: str = None):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai = OpenAI()
        self.model = model or "gpt-4o"

    async def connect_to_server(self, server_script_path: str):
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()
        print("Connected to lyrics MCP server.")

    async def get_song_url(self, query: str) -> str:
        # If it's a Genius URL, return it
        if re.match(r"^https://genius\.com/.*", query.strip()):
            return query.strip()
        # Otherwise, search
        search_result = await self.session.call_tool("search_genius", {"query": query})
        # Extract text from TextContent object and parse as JSON
        raw_content = search_result.content
        # Search result is a list of TextContent objects, get the first three's text
        results = []
        for content in raw_content:
            results.append(json.loads(content.text))
        if not results:
            print("No results found.")
            return ""
        # Keep only the first three results if there are more than three
        if len(results) > 3:
            results = results[:3]
        print("\nTop 3 Genius results:")
        for idx, res in enumerate(results):
            print(f"{idx+1}. {res['title']} by {res['artist_names']} - {res['url']}")
        while True:
            choice = input("Select a song (1-3) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return ""
            if choice in ['1', '2', '3'] and int(choice) <= len(results):
                return results[int(choice)-1]['url']
            print("Invalid choice.")
    
    async def get_lyrics_and_annotations(self, url: str):
        result = await self.session.call_tool("parse_lyrics", {"url": url})
        # result.content is a list of TextContent objects, get the first one's text
        raw_content = result.content[0].text
        # Parse the JSON string
        data = json.loads(raw_content)
        if "error" in data:
            print(data["error"])
            return None, None
        return data["lyrics"], data["annotations"]

    def ask_chatgpt_for_meaning(self, lyrics: str, annotations: list):
        # Compose a prompt for ChatGPT
        annotation_text = "\n".join(
            f"- {a['lyric']}: {a['annotation_text']}" for a in annotations if a['annotation_text']
        )
        prompt = (
            "Given the following song lyrics and their annotations, explain the meaning of the song in detail.\n\n"
            f"Lyrics:\n{lyrics}\n\n"
            f"Annotations:\n{annotation_text if annotation_text else 'None'}"
        )
        response = self.openai.chat.completions.create(
            model=self.model,
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    async def chat_loop(self):
        print("\nLyrics Meaning Client Started!")
        print("Type a Genius URL, song name, or 'song name by artist'. Type 'quit' to exit.")
        while True:
            query = input("\nSong or URL: ").strip()
            if query.lower() == "quit":
                break
            url = await self.get_song_url(query)
            if not url:
                continue
            lyrics, annotations = await self.get_lyrics_and_annotations(url)
            if not lyrics:
                print("Could not retrieve lyrics.")
                continue
            print("\nCalling ChatGPT for song meaning...")
            meaning = self.ask_chatgpt_for_meaning(lyrics, annotations or [])
            print("\nSong Meaning:\n", meaning)

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    import argparse
    parser = argparse.ArgumentParser(description='Lyrics Meaning Client')
    parser.add_argument('server_script', help='Path to the lyrics MCP server script')
    parser.add_argument('--model', help='OpenAI model to use (default: gpt-4o)')
    args = parser.parse_args()
    client = LyricsClient(model=args.model)
    try:
        await client.connect_to_server(args.server_script)
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())