# SpongeBob Meme Machine

[zh-tw version](README.md) | [english version](README.en.md)

<p align="center">
   <img src="sharp-head.jpg" width="60%"></img>
</p>

* Don't know what to send when chatting with friends?
* Want a meme machine that 'understands' you better?

You've come to the right place! This is a [Telegram Bot](https://t.me/spongebob_machine_bot) that uses **NLP / LLM** to analyze user input semantics, understanding you just like Squidward does 🙌

## Usage

[Join now!](https://t.me/spongebob_machine_bot)

### Bot Commands

- `/start` - Start the bot and see welcome message
- `/random` - Get a random meme

### Interaction Modes

1. **Free Text Input**: Type keywords, and the bot will find matching memes using similarity search on aliases
2. **Random Meme**: Use `/random` command for a random meme

### Selection Mechanism

- When search results contain multiple images, the bot displays up to 3 options
- Each option shows `meme_id` and `name`
- Users can click buttons to select the desired image
- If only one image is found, it will be sent directly

## Search Mechanism

The bot performs fuzzy text matching and similarity threshold matching, returning the best matching meme based on similarity score.

## Technology Stack

- **Bot Framework**: `python-telegram-bot`
- **Database**: PostgreSQL + pgvector
- **Search**: PostgreSQL similarity search
- **Image Storage**: Cloudflare R2 (Cyber Bodhisattva)
- **Alias Generation**: OpenAI API

## Contributing

See [`CONTRIBUTING.en.md`](CONTRIBUTING.en.md) for development and build details.
