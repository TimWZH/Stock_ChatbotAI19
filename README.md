# Stock_ChatbotAI19

## Description
This is a chatbot that can answer questions on stock price. The chatbot is integrated into Wechat. Users are allowed to send text or audio message to ask questions. 
To let the chatbot understand your question, you need to specify which company you are asking and what kind of information(current price,historical price, EPS(TTM)).

&nbsp;
## Demo


&nbsp;
## Project structure

```
└── StockBot                        
    ├── StockBot.ipynb         // chatbot
    ├── training_data.json     // training data for extracting intents and entities
    ├── config_spacy.yml       // config for trainer
    ├── city_code.db           // database(all provinces in China with their codes)
    ├── Report.pdf             // report of this project
    └── Demo.mp4               // a demo showing an example dialogue
```
&nbsp;
## How to run
1. In `main.py`, set configuration with a friend's information 
```
my_friend = bot.friends().search('name' sex= , city="city")[0]
```

2. Run `main.py`


&nbsp;
## Requirements
There are few online packages need to be installed for this project
### Rasa-NLU
The recommended way to install Rasa NLU is using pip which will install the latest stable version of Rasa NLU:<br>
```
pip install rasa_nlu
```
Rasa NLU has different components for recognizing intents and entities, most of these will have some additional dependencies.<br>
When you train your model, Rasa NLU will check if all required dependencies are installed and tell you if any are missing.<br>  

***For more installation information***<br>
Go to https://rasa.com/docs/nlu/installation/<br>

### iexfinance
**From PyPI with pip (latest stable release):**<br>
```
$ pip3 install iexfinance
```
**From development repository (dev version):**<br>
If you want to use the bleeding edge version you can get it from github:<br>
```
$ git clone https://github.com/addisonlynch/iexfinance.git
$ cd iexfinance
$ python3 setup.py install
```
***For more installation information***<br>
Go to https://github.com/addisonlynch/iexfinance<br>
<br>

### wxpy
wxpy support Python 3.4-3.6, and 2.7 version<br>
To ensure the package can be installed in different Python version<br>
Replace `pip` in the commond below to `pip3` or `pip2`<br>
<br>
**From PyPI with pip:**<br>
```
pip install -U wxpy
```
**From douban IO PyPI source (Recommend for users in China mainland):**<br>
```

pip install -U wxpy -i "https://pypi.doubanio.com/simple/"
```
***For more installation information***<br>
Go to https://wxpy.readthedocs.io/zh/latest/#<br>


&nbsp;
## TECHNOLOGY USED
https://pypi.org/project/iexfinance/  

https://spacy.io/  

https://rasa.com/docs/nlu/   

https://github.com/youfou/wxpy  

