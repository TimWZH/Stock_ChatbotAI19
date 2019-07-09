from wxpy import *
from chatbot import Chatbot

INIT = 0
MAIN = 1

def main():
    # initialise the bot
    bot = Bot(cache_path=True)
    # search the friend with name
    my_friend = bot.friends().search("旋潇")[0]
    chatbot = Chatbot()

    # sent a start message
    my_friend.send('Hello! This is the chatbot')

    # reply the message send by my_friend
    @bot.register(my_friend)
    def reply_my_friend(msg):
        state = MAIN
        pending = None

        print(chatbot.get_intent(msg.text))
        state, pending, final_response, message_intent = chatbot.send_message(state, pending, msg.text)
        msg.reply(final_response)
        # send_figure
        if message_intent == 'clear_historical_data' or message_intent == 'add_historical_data':
            msg.reply_image('result.png')

        return None

    embed()


if __name__ == '__main__':
    main()