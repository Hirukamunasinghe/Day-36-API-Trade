import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY ="PAA0J4IS4HGOY4KH"
NEWS_API_KEY ="6c87a5ccb12e4f8682f961595ef32679"
TWILIO_SID ="AC9feb75250fc87b0b51477f05649a9bcd"
TWILIO_AUTH_TOKEN ="4e3b328ab72dede8939c2741af66b1d2"

#Getting the yesterdays closing price
stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT,params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list =[value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#Getting the day before yesterdays closing price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#Get the difference
difference = (float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference>0:
    up_down="🔺"
else:
    up_down ="🔻"

print(difference)

#Perecentage difference
diff_perc = round((float(difference)/float(yesterday_closing_price)) * 100)
print(diff_perc)

#Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if abs(diff_perc)>3:
    news_params ={
        "apiKey":NEWS_API_KEY,
        "q":COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()["articles"]
    print(articles)

#Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]
    print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

# Create a new list of the first 3 article's headline and description using list comprehension.

    formatted_article = [f"{STOCK_NAME}: {up_down}{diff_perc}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in three_articles]

#Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_article:
        message = client.messages \
            .create(
            body=article,
            from_='+15625241336',
            to='+94762193001'
        )


