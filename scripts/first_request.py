import os
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(
    api_key=os.getenv("MINIMAX_API_KEY"),
        base_url="https://api.minimax.io/anthropic",

)
