import MetaTrader5 as mt5

if mt5.initialize():
    print("MT5 Connected Successfully")
    print(mt5.version())

    symbols = mt5.symbols_get()

    print("\nFirst 10 symbols:")

    for s in symbols[:10]:
        print(s.name)

    mt5.shutdown()

else:
    print("Connection Failed")
    print(mt5.last_error())