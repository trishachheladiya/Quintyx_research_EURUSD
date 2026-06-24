import MetaTrader5 as mt5

ACCOUNT = 108308441
PASSWORD = "_6LaKvUp"
SERVER = "MetaQuotes-Demo"

symbol = "EURUSD"

# Connect
if not mt5.initialize():
    print("Initialize Failed")
    quit()

if not mt5.login(ACCOUNT, PASSWORD, SERVER):
    print("Login Failed")
    print(mt5.last_error())
    quit()

tick = mt5.symbol_info_tick(symbol)

price = tick.ask

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": 0.01,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "deviation": 20,
    "magic": 123456,
    "comment": "Quintyx Test",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_FOK
}

result = mt5.order_send(request)

print(result)

mt5.shutdown()