import random

# Define the states
CONFUSE = -1
INIT = 0
MAIN = 1

# stock
CRT_PRICE = 2
HIS_PRICE = 3


response_group = {

    "greet": ["Hi! I am a chatbot. I can help you to check the stock price",
              "Nice to meet you. I'm a stock chatbot and I'm ready to help you.",
              ],
    "finish": ["OK. Tell me when you need more assists!",
               "Alright. I'm glad to help you!",
               ],
    "function_intro": [
        "Currently I can help you with: \n1 Get current data\n2 Get historical data \n3 Get earnings Per Share(TTM)"],

    "current_price": ["The current price of {} is {}, and there are some news about {}:\n{}",
                      "{} has a real-time price of {}, and there are some news about {}:\n{}",
                      ],
    "vague_historical_data": ["Please specify which time of data you want to query.",
                              "Which time do you want to know?"
                              ],
    "analyze": ["The Earning Per Share (TTM) of {} is currently {}."]
}


def resp_sentence(intent):
    return random.choice(response_group[intent])


policy_rules = {
    (INIT, "greet"): (MAIN, resp_sentence("greet"), None),
    (MAIN, "greet"): (MAIN, resp_sentence("greet"), None),
    (MAIN, "finish"): (MAIN, resp_sentence("finish"), None),

    (MAIN, "function_intro"): (MAIN, resp_sentence("function_intro"), None),

    (MAIN, "current_price"): (CRT_PRICE, resp_sentence("current_price"), None),
    (CRT_PRICE, "current_price"): (CRT_PRICE, resp_sentence("current_price"), None),
    (CRT_PRICE, "finish"): (MAIN, resp_sentence("finish"), None),

    (MAIN, "clear_historical_data"): (MAIN, "Here is a figure:", None),
    (MAIN, "vague_historical_data"): (MAIN, resp_sentence("vague_historical_data"), HIS_PRICE),
    (HIS_PRICE, "vague_historical_data"): (MAIN, resp_sentence("vague_historical_data"), HIS_PRICE),
    (MAIN, "add_historical_data"): (HIS_PRICE, "Here is a figure:", None),
    (HIS_PRICE, "vague_historical_data"): (HIS_PRICE, "Here is a figure:", None),
    (HIS_PRICE, "finish"): (MAIN, resp_sentence("finish"), None),

    (MAIN, "analyze"): (MAIN, resp_sentence("analyze"), None)

}