# 3D Story AI — clean starter

A starter app that generates original short-form scripts and simple animated vertical video drafts.

## Important truth
- It cannot guarantee viral views.
- It uses original broad storytelling techniques (fast hook, escalating reveal, payoff), not a copy of any creator's exact style.
- The visuals are simple original vector-cartoon illustrations with slow camera movement. They are not true 3D or generated AI artwork.
- A demo script is used if no OpenAI API key is configured. Varied scripts require an API key and may incur usage charges.
- Generated content is saved as a draft. Automatic YouTube publishing is intentionally not enabled in this starter.
- Free hosting may sleep or have limited CPU/storage; scheduled daily generation may not be reliable.
- Review factual claims, rights, audio, and every video before publishing.

## Deploy
1. Upload the complete contents of this folder to the ROOT of a new GitHub repository.
2. In Render choose New → Web Service and connect the repository.
3. Choose Docker as the runtime. Leave Root Directory blank.
4. Do not enter a separate Python build command; Render builds the Dockerfile.
5. Once deployed, open `/health`.

## Environment variables
- `OPENAI_API_KEY` optional; enables varied script generation.
- `OPENAI_MODEL` optional; defaults to `gpt-4o-mini`.
- `VOICE` optional; defaults to `en-US-GuyNeural`.
- `TIMEZONE` defaults to `Africa/Lagos`.
- `ENABLE_SCHEDULER` defaults to `false`.
- `POST_TIMES` defaults to `10:00,18:00`.

## Local run
Requires Python 3.11+ and FFmpeg:
`pip install -r requirements.txt`
`uvicorn app.main:app --reload`
Then open http://127.0.0.1:8000

## Publishing
YouTube publishing is not wired on by default. Production publishing needs a secure Google OAuth web callback, protected token storage, persistent storage, quota checks, and private-upload testing. Never put OAuth secrets or tokens in GitHub or chat.
