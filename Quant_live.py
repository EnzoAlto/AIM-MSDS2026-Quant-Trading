import json
from enum import Enum
from typing import Optional

class Side(Enum):
    BUY = 0
    SELL = 1

class Ticker(Enum):
    TEAM_A = 0  # Home team

def place_market_order(side: Side, ticker: Ticker, quantity: float) -> None:
    print(f"Placing MARKET order: {side.name} {quantity} {ticker.name}")

def place_limit_order(side: Side, ticker: Ticker, quantity: float, price: float, ioc: bool = False) -> int:
    print(f"Placing LIMIT order: {side.name} {quantity} {ticker.name} @ {price}")
    return 1

def cancel_order(ticker: Ticker, order_id: int) -> bool:
    print(f"Cancelling order {order_id} on {ticker.name}")
    return True

class Strategy:
    def reset_state(self) -> None:
        self.capital = 1000.0  # starting cash
        self.position = 0      # net contracts
        print("State reset: capital = 1000, position = 0")

    def __init__(self) -> None:
        self.reset_state()

    def estimate_probability(self, home_score: int, away_score: int, time_seconds: float) -> float:
        """Heuristic probability of home winning."""
        score_diff = home_score - away_score
        time_factor = max(1, time_seconds / 2880.0)  # normalize to [0,1]
        # crude heuristic: probability shifts with score difference
        prob = 0.5 + 0.1 * score_diff * time_factor
        return min(max(prob, 0.0), 1.0)

    def on_game_event_update(
        self,
        event_type: str,
        home_away: str,
        home_score: int,
        away_score: int,
        player_name: Optional[str],
        substituted_player_name: Optional[str],
        shot_type: Optional[str],
        assist_player: Optional[str],
        rebound_type: Optional[str],
        coordinate_x: Optional[float],
        coordinate_y: Optional[float],
        time_seconds: Optional[float]
    ) -> None:

        print(f"Event: {event_type}, Score {home_score}-{away_score}, Time {time_seconds}")

        if event_type == "END_GAME":
            print("Game ended. Resetting state.")
            self.reset_state()
            return

        # Trading decision
        if time_seconds is not None:
            prob = self.estimate_probability(home_score, away_score, time_seconds)
            if prob > 0.55:  # home has higher chance
                place_market_order(Side.BUY, Ticker.TEAM_A, 1)
                self.position += 1
            elif prob < 0.45:  # away more likely
                place_market_order(Side.SELL, Ticker.TEAM_A, 1)
                self.position -= 1

def run_simulation(json_file: str):
    strategy = Strategy()
    with open(json_file, "r") as f:
        events = json.load(f)
    for event in events:
        strategy.on_game_event_update(**event)

if __name__ == "__main__":
    run_simulation("example-game.json")
