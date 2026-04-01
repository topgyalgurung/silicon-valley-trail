from dataclasses import dataclass

@dataclass
class ActionResult:
    game: object
    event: dict | None
    status: str | None
    message: str | None
    weather_data: dict | None = None
    game_over: bool = False 