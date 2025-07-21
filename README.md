# Lyrics Meaning Client (MCP)

An MCP (Model Context Protocol) client that interprets song meanings by fetching lyrics and annotations from Genius.com and analyzing them with ChatGPT.

## Overview

This client connects to a corresponding [Lyrics MCP Server](https://github.com/rcuri/lyrics-server) to:
1. Search for songs on Genius.com or accept direct Genius URLs
2. Fetch song lyrics and annotations via the MCP server
3. Use OpenAI's ChatGPT to provide detailed interpretations of the song's meaning

Built following the [MCP Client Quickstart Guide](https://modelcontextprotocol.io/quickstart/client).

## Demo

![Lyrics Client Demo](static/lyrics-demo.gif)

*The demo shows the complete workflow: searching for a song, selecting from results, and getting an AI-powered interpretation of the song's meaning.*

## Features

- **Flexible Song Input**: Accept either song names/artist combinations or direct Genius.com URLs
- **Interactive Search**: When searching by name, displays top 3 results for user selection
- **Rich Analysis**: Combines lyrics with Genius annotations for comprehensive meaning interpretation
- **Configurable AI Model**: Choose your preferred OpenAI model (defaults to GPT-4o)
- **Clean CLI Interface**: Simple command-line interaction for easy use

## Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- Access to the [Lyrics MCP Server](https://github.com/rcuri/lyrics-server)
- Lyrics MCP Server must be configured with a Genius API token

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rcuri/lyrics-client.git
   cd lyrics-client
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the client by providing the path to your lyrics MCP server script:

```bash
uv run python client.py /path/to/your/lyrics-server/server.py
```

### Optional Parameters

- `--model`: Specify the OpenAI model to use (default: `gpt-4o`)
  ```bash
  uv run python client.py /path/to/server.py --model gpt-3.5-turbo
  ```

### Interactive Usage

Once started, you can:

1. **Enter a song name or "song by artist":**
   ```
   Song or URL: Bohemian Rhapsody by Queen
   ```

2. **Paste a direct Genius.com URL:**
   ```
   Song or URL: https://genius.com/Queen-bohemian-rhapsody-lyrics
   ```

3. **Select from search results** (when searching by name):
   ```
   Top 3 Genius results:
   1. Bohemian Rhapsody by Queen - https://genius.com/Queen-bohemian-rhapsody-lyrics
   2. Bohemian Rhapsody by Panic! At The Disco - https://genius.com/Panic-at-the-disco-bohemian-rhapsody-lyrics
   3. Bohemian Rhapsody by Pentatonix - https://genius.com/Pentatonix-bohemian-rhapsody-lyrics
   Select a song (1-3) or 'q' to quit: 1
   ```

4. **Type `quit` to exit**

## How It Works

1. **Connection**: Establishes MCP connection to the lyrics server via stdio
2. **Song Resolution**: 
   - If input is a Genius URL, uses it directly
   - If input is a search query, calls the server's `search_genius` tool
3. **Data Retrieval**: Uses the server's `parse_lyrics` tool to fetch lyrics and annotations
4. **AI Analysis**: Sends lyrics and annotations to ChatGPT for meaning interpretation
5. **Display**: Shows the AI-generated song meaning to the user

## MCP Tools Used

This client interacts with the following MCP tools provided by the server:

- `search_genius`: Searches Genius.com for songs using the official Genius API
- `parse_lyrics`: Extracts lyrics and annotations from a Genius.com URL using HTML parsing and Selenium automation

## Dependencies

- **mcp**: Model Context Protocol implementation
- **openai**: OpenAI API client for ChatGPT integration
- **python-dotenv**: Environment variable management
- **beautifulsoup4**: HTML parsing (inherited from server requirements)
- **selenium**: Web scraping (inherited from server requirements)

## Related Projects

- **[Lyrics MCP Server](https://github.com/rcuri/lyrics-server)**: The companion server that handles Genius.com data fetching

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key for ChatGPT | Yes |

### Model Selection

The client defaults to using `gpt-4o` but supports any OpenAI chat model:
- `gpt-4o`
- `gpt-4`
- `gpt-3.5-turbo`
- Other compatible models

## Error Handling

The client handles common scenarios gracefully:
- Invalid song searches (no results found)
- Network connectivity issues with the MCP server
- OpenAI API errors
- Malformed Genius URLs

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built using the [Model Context Protocol](https://modelcontextprotocol.io/)
- Inspired by the [MCP Client Quickstart Guide](https://modelcontextprotocol.io/quickstart/client)
- Lyrics and annotations powered by [Genius.com](https://genius.com)
- AI interpretation powered by [OpenAI](https://openai.com)
