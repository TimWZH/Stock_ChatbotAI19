from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from states_rules import *

from datetime import datetime

# iexfinance
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data



class Chatbot:

    def __init__(self):
        print('Create a new chatbot.')
        trainer = Trainer(config.load("config_spacy.yml"))
        # Load the training data
        training_data = load_data('training-data.json')
        interpreter = trainer.train(training_data)
        self.interpreter = interpreter
        self.state = INIT
        self.params={}

    def send_message(self,state, pending, message):
        print("old_state: ", state, "message: ", message, "pending: ", pending)
        new_state, response, pending_state = self.respond(state, message)
        #print("new_state: ", new_state, "response: ", response, "pending_state: ", pending_state)

        if pending is not None:
            new_state, response, pending_state = self.respond(state, message)
        if pending_state is not None:
            pending = (pending_state, self.get_intent(message))

        return new_state, pending, response, self.get_intent(message)

    def respond(self,state, message):
        entity = self.get_entity(message)

        try:
            new_state = policy_rules[(state, self.get_intent(message))][0]
            print("new_state is:"+str(new_state))
        except KeyError:
            new_state = CONFUSE
        pending_state = policy_rules[(state, self.get_intent(message))][2]

        if self.get_intent(message) == 'greet':
            response = policy_rules[(state, self.get_intent(message))][1]

        if self.get_intent(message) == 'finish':
            response = policy_rules[(state, self.get_intent(message))][1]

        if self.get_intent(message) == 'function_intro':
            response = policy_rules[(state, self.get_intent(message))][1]


        if self.get_intent(message) == 'current_price':
            response = policy_rules[(state, self.get_intent(message))][1].format(entity, self.get_current_price(entity), entity,
                                                                            self.get_news(entity))
        if self.get_intent(message) == 'clear_historical_data':
            response = policy_rules[(state, self.get_intent(message))][1]
            self.generate_figure(message)
            print('clear_historical_data:'+response)
        if self.get_intent(message) == 'vague_historical_data':
            response = policy_rules[(state, self.get_intent(message))][1]

        if self.get_intent(message) == 'add_historical_data':
            response = policy_rules[(state, self.get_intent(message))][1]
            self.generate_figure(message)
            print('add_historical_data:'+response)

        if self.get_intent(message) == 'analyze':
            response = policy_rules[(state, self.get_intent(message))][1].format(entity, self.get_ttmEPS(entity))

        return new_state, response, pending_state

    def get_intent(self,message):
        return self.interpreter.parse(message)['intent']['name']



    def get_entity(self,message):
        if self.interpreter.parse(message)['entities'] == []:
            return []

        if self.interpreter.parse(message)['entities'][0]['entity'] == 'company':
            return self.interpreter.parse(message)['entities'][0]['value']

            return [self.interpreter.parse(message)['entities'][0]['value'],
                    self.interpreter.parse(message)['entities'][1]['value']]

    #########################################
    def get_current_price(self,company):
        print("Company: ", company)
        stock = Stock(company, token="pk_093076db203147459265b42be5c55e6b")
        prices = str(stock.get_price())
        return prices

    def get_ttmEPS(self,company):
        ttmEPS = Stock(company, token="pk_093076db203147459265b42be5c55e6b").get_key_stats()['ttmEPS']
        return ttmEPS

    def get_news(self,company):
        news = Stock(company, token="pk_093076db203147459265b42be5c55e6b").get_news()
        for i in news:
            if i['summary'] != 'No summary available.':
                return i['url']

    def generate_figure(self,message,):
        comprehended_data = self.interpreter.parse(message)

        for i in range(0, 2):
            if comprehended_data['entities'][i]['entity'] == 'company':
                required_company = comprehended_data['entities'][i]['value']
            if comprehended_data['entities'][i]['entity'] == 'his_price_type':
                required_type = comprehended_data['entities'][i]['value']
            else:
                required_company = 'AAPL'
                required_type = 'close'

        if len(comprehended_data['entities']) <= 3:
            time_period = [comprehended_data['entities'][0]['value'],
                           comprehended_data['entities'][1]['value']]

            start_time_splited = time_period[0].split(' - ')
            end_time_splited = time_period[1].split(' - ')

            start_year = int(start_time_splited[0])
            start_month = int(start_time_splited[1])
            start_day = int(start_time_splited[2])

            end_year = int(end_time_splited[0])
            end_month = int(end_time_splited[1])
            end_day = int(end_time_splited[2])

            start_time = datetime(start_year, start_month, start_day)
            end_time = datetime(end_year, end_month, end_day)

            his_data = get_historical_data(required_company, start_time, end_time, output_format='pandas', token="pk_093076db203147459265b42be5c55e6b")

        else:
            time_period = [comprehended_data['entities'][2]['value'],
                           comprehended_data['entities'][3]['value']]

            start_time_splited = time_period[0].split('-')
            end_time_splited = time_period[1].split('-')

            start_year = int(start_time_splited[0])
            start_month = int(start_time_splited[1])
            start_day = int(start_time_splited[2])

            end_year = int(end_time_splited[0])
            end_month = int(end_time_splited[1])
            end_day = int(end_time_splited[2])

            start_time = datetime(start_year, start_month, start_day)
            end_time = datetime(end_year, end_month, end_day)

            his_data = get_historical_data(required_company, start_time, end_time, output_format='pandas', token="pk_093076db203147459265b42be5c55e6b")

        plot_required_type = his_data[required_type].plot()
        fig = plot_required_type.get_figure()
        fig.savefig('result.png')
