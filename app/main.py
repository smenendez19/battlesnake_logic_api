# Imports
import os

import algorithm as algorithm
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI(
    title="battlesnake_rest_api",
    description="BattleSnake Rest API",
    version="1.0.0",
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
    snake_data = {
        "apiversion": "1",
        "author": "smenendez19",
        "color": "#810E07",
        "head": "all-seeing",
        "tail": "shiny",
    }
    print(snake_data)
    return {
        "apiversion": "1",
        "author": "smenendez19",
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
    message = f"Game started with id {data['game']['id']}"
    print(message)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": message
        },
    )


@app.post("/move")
async def handle_move(request: Request):
    """
    This function is called on every turn of a game. It's how your snake decides where to move.
    Valid moves are "up", "down", "left", or "right".
    """
    data = await request.json()
    move = algorithm.choose_move(data)
    message = f"Choosing move {move}"
    print(message)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "move": move,
        },
    )


@app.post("/end")
async def end(request: Request):
    """
    This function is called when a game your snake was in ends.
    It's purely for informational purposes, you don't have to make any decisions here.
    """
    data = await request.json()
    message = f"Game ended with id {data['game']['id']}"
    print(message)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": message
        },
    )


if __name__ == "__main__":
    print("Starting Battlesnake Server...")
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=os.path.join("config", "log_conf.yaml"))
