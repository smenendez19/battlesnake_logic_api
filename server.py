# Imports

import logging
import os

import uvicorn
from fastapi import FastAPI, Request

import server_logic

app = FastAPI(
    title="battlesnake_logic_python",
    description="BattleSnake API with FastAPI",
    version="0.0.1",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


@app.get("/")
def handle_info():
    """
    This function is called when you register your Battlesnake on play.battlesnake.com
    See https://docs.battlesnake.com/guides/getting-started#step-4-register-your-battlesnake

    It controls your Battlesnake appearance and author permissions.
    For customization options, see https://docs.battlesnake.com/references/personalization

    TIP: If you open your Battlesnake URL in browser you should see this data.
    """
    return {
        "apiversion": "1",
        "author": "NeoDemon",
        "color": "#810E07",
        "head": "all-seeing",
        "tail": "shiny",
    }


@app.post("/start")
async def handle_start(request: Request):
    """
    This function is called everytime your snake is entered into a game.
    request.json contains information about the game that's about to be played.
    """
    data = await request.json()
    print(f"{data['game']['id']} START")
    return "ok"


@app.post("/move")
async def handle_move(request: Request):
    """
    This function is called on every turn of a game. It's how your snake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """
    data = await request.json()
    move = server_logic.choose_move(data)
    return {"move": move}


@app.post("/end")
async def end(request: Request):
    """
    This function is called when a game your snake was in ends.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = await request.json()
    print(f"{data['game']['id']} END")
    return "ok"


if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    print("Starting Battlesnake Server...")
    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
