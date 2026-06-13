import MetaTrader5 as mt5
from datetime import datetime

ACCOUNT = 108308441
PASSWORD = "_6LaKvUp"
SERVER = "MetaQuotes-Demo"

mt5.initialize()
mt5.login(ACCOUNT, PASSWORD, SERVER)

symbol = "EURUSD"

print("Symbol Select:", mt5.symbol_select(symbol, True))

rates = mt5.copy_rates_from_pos(
    symbol,
    mt5.TIMEFRAME_H1,
    0,
    10
)

print("Rates:")
print(rates)

if rates is not None and len(rates) > 0:
    print("\nLatest Candle:")
    print(datetime.fromtimestamp(rates[-1]["time"]))

tick = mt5.symbol_info_tick(symbol)

print("\nTick:")
print(tick)

mt5.shutdown()