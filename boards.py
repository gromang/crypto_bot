keyboard = {
    "Start": {
        "board_view": [["Торговля", "Графики"]],
        "text": '''Бот предоставляет возможность смотреть
cуммированые графики криптовалютных пар
*нажмите кнопку Chart*
и отправлять торговые приказы
*нажмите кнопку Trade*''',
        "go_to": {
            "Торговля": "Trade",
            "Графики": "Chart_pair"
        },
        "action": None
    },
    "Trade": {
        "board_view": [
            ["Новый ордер"],
            #            ["Закрыть ордер"],
            ["Назад"]
        ],
        "text": "Выберите действие",
        "go_to": {
            "Новый ордер": "Exchange",
            #            "Закрыть ордер": "Close",
            "Назад": "Start"
        },
        "action": None
    },
    "Exchange": {
        "board_view": [
            ["BINANCE", "BITFINEX"],
            ["KRAKEN", "HITBTC"],
            ["Назад"]
        ],
        "text": "На какую биржу отправить торговый приказ?",
        "go_to": {
            "BINANCE": "Trade_pair",
            "BITFINEX": "Trade_pair",
            "KRAKEN": "Trade_pair",
            "HITBTC": "Trade_pair",
            "Назад": "Trade"
        },
        "action": "store"
    },
    "Trade_pair": {
        "board_view": [
            ["BTCUSD", "LTCUSD"],
            ["ETHUSD", "XRPUSD"],
            ["Назад"]
        ],
        "text": "Выберите торговый инструмент",
        "go_to": {
            "BTCUSD": "Lot",
            "LTCUSD": "Lot",
            "ETHUSD": "Lot",
            "XRPUSD": "Lot",
            "Назад": "Exchange"
        },
        "action": 'store'
    },
    "Lot": {
        "board_view": [
            ["Назад"],
            ["Отправить приказ"],
        ],
        "text": '''Введите размер лота
в текстовом поле ниже''',
        "go_to": {
            "Отправить приказ": "Start",
            "Назад": "Trade_pair"
        },
        "action": "send order"
    },
    "Chart_pair": {
        "board_view": [
            ["BTCUSD", "LTCUSD"],
            ["ETHUSD", "XRPUSD"],
            ["Назад"]
        ],
        "text": "Выберите валютную пару",
        "go_to": {
            "BTCUSD": "Interval",
            "LTCUSD": "Interval",
            "ETHUSD": "Interval",
            "XRPUSD": "Interval",
            "Назад": "Start"
        },
        "action": 'store'
    },
    "Interval": {
        "board_view": [
            ["1 min", "5 min", "15 min", "30 min"],
            ["1 hour", "4 hour", "12 hour", "1 day"],
            ["Назад"]
        ],
        "text": "Выберите интервал свечи",
        "go_to": {
            "1 min": "Chart",
            "5 min": "Chart",
            "15 min": "Chart",
            "30 min": "Chart",
            "1 hour": "Chart",
            "4 hour": "Chart",
            "12 hour": "Chart",
            "1 day": "Chart",
            "Назад": "Chart_pair"
        },
        "action": 'store'
    },
    "Chart": {
        "board_view": [
            ["Назад"]
        ],
        "text": "График",
        "go_to": {
            "Назад": "Interval"
        },
        "action": "get chart"
    },
}
