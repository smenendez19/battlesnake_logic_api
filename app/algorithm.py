import math


def avoid_my_neck(my_head, my_body, possible_moves):
    my_neck = my_body[1]
    if my_neck["x"] < my_head["x"]:
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:
        possible_moves.remove("up")
    return possible_moves


def avoid_walls(board_height, board_width, my_head, possible_moves):
    if my_head["x"] == board_height - 1:
        possible_moves.remove("right")
    if my_head["x"] == 0:
        possible_moves.remove("left")
    if my_head["y"] == 0:
        possible_moves.remove("down")
    if my_head["y"] == board_width - 1:
        possible_moves.remove("up")
    return possible_moves


def priorize_food(data, my_head):
    distance_food = {"up": None, "down": None, "left": None, "right": None}
    for food_pos in data["board"]["food"]:
        if my_head["x"] < food_pos["x"] and my_head["y"] == food_pos["y"]:
            if distance_food["right"] is None or distance_food["right"] > food_pos["x"] - my_head["x"]:
                distance_food["right"] = food_pos["x"] - my_head["x"]
        elif my_head["x"] > food_pos["x"] and my_head["y"] == food_pos["y"]:
            if distance_food["left"] is None or distance_food["left"] > food_pos["x"] + my_head["x"]:
                distance_food["left"] = food_pos["x"] + my_head["x"]
        elif my_head["y"] < food_pos["y"] and my_head["x"] == food_pos["x"]:
            if distance_food["up"] is None or distance_food["up"] > food_pos["y"] - my_head["y"]:
                distance_food["up"] = food_pos["y"] - my_head["y"]
        elif my_head["y"] > food_pos["y"] and my_head["x"] == food_pos["x"]:
            if distance_food["down"] is None or distance_food["down"] > food_pos["y"] - my_head["y"]:
                distance_food["down"] = food_pos["y"] + my_head["y"]
    food_move = None
    min_dist = None
    for dir in distance_food:
        if distance_food[dir] is not None and (min_dist is None or distance_food[dir] < min_dist):
            min_dist = distance_food[dir]
            food_move = dir
    return food_move


def calculate_distance_food(data, my_head):
    distance_food = dict()
    for food_pos in data["board"]["food"]:
        x = food_pos["x"] - my_head["x"]
        y = food_pos["y"] - my_head["y"]
        distance = math.sqrt(x**2 + y**2)
        distance_food[(food_pos["x"], food_pos["y"])] = distance
    if len(distance_food):
        min_distance_food = min(distance_food, key=distance_food.get)
        best_moves = get_food_move(min_distance_food, my_head)
    else:
        best_moves = []
    return best_moves


def get_food_move(food, my_head):
    food_pos = {"x": food[0], "y": food[1]}
    food_moves = []
    # Same X
    if food_pos["x"] == my_head["x"]:
        if food_pos["y"] < my_head["y"]:
            food_moves.append("down")
        elif food_pos["y"] > my_head["y"]:
            food_moves.append("up")
    # Same Y
    elif food_pos["y"] == my_head["y"]:
        if food_pos["x"] < my_head["x"]:
            food_moves.append("left")
        elif food_pos["x"] > my_head["x"]:
            food_moves.append("right")
    # < X
    elif food_pos["x"] < my_head["x"]:
        if food_pos["y"] < my_head["y"]:
            food_moves.append("left")
            food_moves.append("down")
        elif food_pos["y"] > my_head["y"]:
            food_moves.append("left")
            food_moves.append("up")
    # > X
    elif food_pos["x"] > my_head["x"]:
        if food_pos["y"] < my_head["y"]:
            food_moves.append("right")
            food_moves.append("down")
        elif food_pos["y"] > my_head["y"]:
            food_moves.append("right")
            food_moves.append("up")
    return food_moves


def avoid_snakes(data, my_head, possible_moves):
    for snake in data["board"]["snakes"]:
        for body_parts in snake["body"]:
            # Same Y
            if body_parts["y"] == my_head["y"]:
                if body_parts["x"] == my_head["x"] - 1:
                    if "left" in possible_moves:
                        possible_moves.remove("left")
                if body_parts["x"] == my_head["x"] + 1:
                    if "right" in possible_moves:
                        possible_moves.remove("right")
            # Same X
            if body_parts["x"] == my_head["x"]:
                if body_parts["y"] == my_head["y"] + 1:
                    if "up" in possible_moves:
                        possible_moves.remove("up")
                if body_parts["y"] == my_head["y"] - 1:
                    if "down" in possible_moves:
                        possible_moves.remove("down")
    return possible_moves


def avoid_body(my_head, my_body, possible_moves):
    my_body_parts = my_body[2:]
    for body_parts in my_body_parts:
        if body_parts["y"] == my_head["y"]:
            if body_parts["x"] == my_head["x"] - 1:
                if "left" in possible_moves:
                    possible_moves.remove("left")
            if body_parts["x"] == my_head["x"] + 1:
                if "right" in possible_moves:
                    possible_moves.remove("right")
        if body_parts["x"] == my_head["x"]:
            if body_parts["y"] == my_head["y"] + 1:
                if "up" in possible_moves:
                    possible_moves.remove("up")
            if body_parts["y"] == my_head["y"] - 1:
                if "down" in possible_moves:
                    possible_moves.remove("down")
    return possible_moves


def choose_move(data: dict) -> str:
    my_head = data["you"]["head"]
    my_body = data["you"]["body"]
    possible_moves = ["up", "down", "left", "right"]
    board_height = data["board"]["height"]
    board_width = data["board"]["width"]

    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    print(f"All board data this turn: {data}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    # Avoid neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    # Avoid border
    possible_moves = avoid_walls(board_height, board_width, my_head, possible_moves)

    # Avoid crash with body
    possible_moves = avoid_body(my_head, my_body, possible_moves)

    # Avoid crash with other snakes
    possible_moves = avoid_snakes(data, my_head, possible_moves)

    # Priorize food
    food_moves = calculate_distance_food(data, my_head)
    delete_moves = []
    for food_move in food_moves:
        if food_move not in possible_moves:
            delete_moves.append(food_move)
    for move in delete_moves:
        food_moves.remove(move)

    # print("Moves: ", possible_moves)

    # Include list if not possible moves
    if len(possible_moves) == 0:
        possible_moves = ["up", "left", "right", "down"]

    if len(food_moves) > 0:
        move = food_moves[0]
    else:
        move = possible_moves[0]

    # print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")
    # print("Choosed Move: ", move)

    return move
