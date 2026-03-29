from dataclasses import dataclass

@dataclass
class ActionResult:
    game: object
    event: dict | None
    status: str | None
    message: str | None
    game_over: bool = False 