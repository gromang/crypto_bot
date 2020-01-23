boards = {
    "Start": {
        "board_view": [["Торговля", "Графики"]],
        "text": "Бот предоставляет возможность смотреть cуммированые графики криптовалютных пар и отправлять торговые приказы",
        "go_to": {"Торговля": "Trade", "Графики": "Chart_pair"},
        "action": None,
    },
    "Trade": {
        "board_view": [
            ["Новый ордер"],
            # ["Закрыть ордер"],
            ["Назад"],
        ],
        "text": "Выберите действие",
        "go_to": {
            "Новый ордер": "Exchange",
            # "Закрыть ордер": "Close_order",
            "Назад": "Start",
        },
        "action": None,
    },
    "Exchange": {
        "board_view": [["BINANCE", "BITFINEX"], ["KRAKEN", "HITBTC"], ["Назад"]],
        "text": "На какую биржу отправить торговый приказ?",
        "go_to": {
            "BINANCE": "Trade_pair",
            "BITFINEX": "Trade_pair",
            "KRAKEN": "Trade_pair",
            "HITBTC": "Trade_pair",
            "Назад": "Trade",
        },
        "action": "save",
    },
    "Trade_pair": {
        "board_view": [["BTCUSD", "LTCUSD"], ["ETHUSD", "XRPUSD"], ["Назад"]],
        "text": "Выберите торговый инструмент",
        "go_to": {
            "BTCUSD": "Buy_Sell",
            "LTCUSD": "Buy_Sell",
            "ETHUSD": "Buy_Sell",
            "XRPUSD": "Buy_Sell",
            "Назад": "Exchange",
        },
        "action": "save",
    },
    "Buy_Sell": {
        "board_view": [["Buy", "Sell"], ["Назад"]],
        "text": "Выберите направление позиции",
        "go_to": {"Buy": "Lot", "Sell": "Lot", "Назад": "Trade_pair"},
        "action": "save",
    },
    "Lot": {
        "board_view": [["Назад"], ["Сформировать приказ"],],
        "text": "Введите размер лота в текстовом поле ниже",
        "go_to": {"Сформировать приказ": "Send_order", "Назад": "Buy_Sell"},
        "action": "make_order",
    },
    "Send_order": {
        "board_view": [["Назад"], ["Отправить приказ"],],
        "text": "Приказ не отправлен",
        "go_to": {"Отправить приказ": "Start", "Назад": "Buy_Sell"},
        "action": "send_order",
    },
    "Chart_pair": {
        "board_view": [["BTCUSD", "LTCUSD"], ["ETHUSD", "XRPUSD"], ["Назад"]],
        "text": "Выберите валютную пару",
        "go_to": {
            "BTCUSD": "Interval",
            "LTCUSD": "Interval",
            "ETHUSD": "Interval",
            "XRPUSD": "Interval",
            "Назад": "Start",
        },
        "action": "save",
    },
    "Interval": {
        "board_view": [
            ["1 min", "5 min", "15 min", "30 min"],
            ["1 hour", "4 hours", "6 hours", "12 hours"],
            ["Назад"],
        ],
        "text": "Выберите интервал свечи",
        "go_to": {
            "1 min": "Chart",
            "5 min": "Chart",
            "15 min": "Chart",
            "30 min": "Chart",
            "1 hour": "Chart",
            "4 hours": "Chart",
            "6 hours": "Chart",
            "12 hours": "Chart",
            "Назад": "Chart_pair",
        },
        "action": "save",
    },
    "Chart": {
        "board_view": [["Назад"]],
        "text": "График",
        "go_to": {"Назад": "Interval"},
        "action": "get_chart",
    },
}
