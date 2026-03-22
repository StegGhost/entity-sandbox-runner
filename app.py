import asyncio
import json
import websockets
from dataclasses import dataclass
from datetime import datetime

# ===== CONFIG =====
PAIR = "ETH-USD"
TRADE_SIZE_USD = 200
FEE_RATE = 0.004  # 0.4% worst-case Coinbase retail
PROFIT_TARGET = 1.00
SLIPPAGE_BUFFER = 0.25
MAX_HOLD_SECONDS = 3600

# ===== STATE =====
best_bid = None
best_ask = None

@dataclass
class Position:
    entry_price: float
    size: float
    entry_fee: float
    timestamp: datetime

position = None


# ===== MARKET DATA =====
async def market_data():
    global best_bid, best_ask

    uri = "wss://advanced-trade-ws.coinbase.com"
    async with websockets.connect(uri) as ws:
        sub = {
            "type": "subscribe",
            "channel": "ticker",
            "product_ids": [PAIR]
        }
        await ws.send(json.dumps(sub))

        while True:
            msg = json.loads(await ws.recv())

            if "events" in msg:
                for event in msg["events"]:
                    if "tickers" in event:
                        for t in event["tickers"]:
                            best_bid = float(t["best_bid"])
                            best_ask = float(t["best_ask"])


# ===== STRATEGY =====
def calculate_size(price):
    return TRADE_SIZE_USD / price


def can_enter():
    global best_bid, best_ask, position
    if position is not None:
        return False
    if best_bid is None or best_ask is None:
        return False

    spread = best_ask - best_bid
    return spread < 2.0  # avoid wide spread


def enter_position():
    global position

    price = best_bid  # simulate maker fill
    size = calculate_size(price)
    fee = price * size * FEE_RATE

    position = Position(price, size, fee, datetime.utcnow())

    print(f"\n🟢 ENTER @ {price:.2f} size={size:.6f}")


def calculate_net_profit(exit_price):
    global position

    gross = (exit_price - position.entry_price) * position.size
    exit_fee = exit_price * position.size * FEE_RATE

    net = gross - position.entry_fee - exit_fee - SLIPPAGE_BUFFER
    return net


def should_exit():
    global position, best_bid

    if position is None:
        return False

    net = calculate_net_profit(best_bid)

    # time stop
    held = (datetime.utcnow() - position.timestamp).total_seconds()
    if held > MAX_HOLD_SECONDS:
        print("⏱ TIME EXIT")
        return True

    return net >= PROFIT_TARGET


def exit_position():
    global position, best_bid

    exit_price = best_bid
    net = calculate_net_profit(exit_price)

    print(f"🔴 EXIT @ {exit_price:.2f} NET=${net:.2f}")

    position = None


# ===== MAIN LOOP =====
async def trader():
    while True:
        await asyncio.sleep(0.2)

        if can_enter():
            enter_position()

        if should_exit():
            exit_position()


async def main():
    await asyncio.gather(
        market_data(),
        trader()
    )


if __name__ == "__main__":
    asyncio.run(main())
