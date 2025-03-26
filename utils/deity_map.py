def get_deity_recommendation(goal: str):
    goal = goal.lower()
    for key in GOAL_DEITY_MAP:
        if key in goal:
            return GOAL_DEITY_MAP[key]
    return GOAL_DEITY_MAP["default"]
