import MetaTrader5 as mt5

ACCOUNT = 108308441
PASSWORD = "_6LaKvUp"
SERVER = "MetaQuotes-Demo"

print("Initialize:", mt5.initialize())

print(
    "Login:",
    mt5.login(
        login=ACCOUNT,
        password=PASSWORD,
        server=SERVER
    )
)

print("Account:", mt5.account_info())
print("Terminal:", mt5.terminal_info())

mt5.shutdown()