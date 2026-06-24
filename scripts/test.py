info = mt5.symbol_info(symbol)

filling = info.filling_mode

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
    "type_filling": filling
}