from enum import Enum
from typing import Optional

class Side(Enum):
    BUY = 0
    SELL = 1

class Ticker(Enum):
    TEAM_A = 0  # Home team

def place_market_order(side: Side, ticker: Ticker, quantity: float) -> None:
    print(f"MARKET {side.name} {quantity} {ticker.name}")

def place_limit_order(side: Side, ticker: Ticker, quantity: float, price: float, ioc: bool = False) -> int:
    print(f"LIMIT {side.name} {quantity} {ticker.name} @ {price}")
    return 1

def cancel_order(ticker: Ticker, order_id: int) -> bool:
    print(f"CANCEL {order_id} {ticker.name}")
    return True

class Strategy:
    """Basketball Market Trading Algorithm."""

    def reset_state(self) -> None:
        """Reset to starting state."""
        self.capital = 1000.0
        self.position = 0
        self.last_prob = 0.5
        print("RESET state")

    def __init__(self) -> None:
        self.reset_state()

    def estimate_probability(self, home_score: int, away_score: int, time_seconds: float) -> float:
        """Estimate probability of home win using a simple heuristic."""
        score_diff = home_score - away_score
        time_factor = max(1, time_seconds / 2880.0)  # normalized time
        prob = 0.5 + 0.1 * score_diff * time_factor
        return min(max(prob, 0.0), 1.0)

    def on_orderbook_update(self, ticker: Ticker, side: Side, quantity: float, price: float) -> None:
        print(f"ORDERBOOK {ticker.name} {side.name} {quantity}@{price}")

    def on_trade_update(self, ticker: Ticker, side: Side, quantity: float, price: float) -> None:
        print(f"TRADE {ticker.name} {side.name} {quantity}@{price}")

    def on_account_update(
        self,
        ticker: Ticker,
        side: Side,
        price: float,
        quantity: float,
        capital_remaining: float,
    ) -> None:
        print(f"ACCOUNT {ticker.name} {side.name} {quantity}@{price} REMAIN {capital_remaining}")
        self.capital = capital_remaining

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

        print(f"GAME {event_type} {home_score}-{away_score} T={time_seconds}")

        if event_type == "END_GAME":
            print("END_GAME resetting")
            self.reset_state()
            return

        if time_seconds is not None:
            prob = self.estimate_probability(home_score, away_score, time_seconds)

            if prob > 0.55 and self.last_prob <= 0.55:
                place_market_order(Side.BUY, Ticker.TEAM_A, 1)
                self.position += 1

            elif prob < 0.45 and self.last_prob >= 0.45:
                place_market_order(Side.SELL, Ticker.TEAM_A, 1)
                self.position -= 1

            self.last_prob = prob

    def on_orderbook_snapshot(self, ticker: Ticker, bids: list, asks: list) -> None:
        best_bid = bids[0][0] if bids else None
        best_ask = asks[0][0] if asks else None
        print(f"SNAPSHOT {ticker.name} BID {best_bid} ASK {best_ask}")
