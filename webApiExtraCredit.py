import pprint
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

secret = '27f1f4908a0a43d18fd550e879571600'

# Define and endpoint 
url = 'https://newsapi.org/v2/everything?'

# Specify the query and number of returns

parameters = {
    'q': 'palestine',  # query phrase
    'from': '05/10/25',  #start date 
    'to': '05/10/25',    #end date 
    'sortBy': 'relevancy', #sort by relevancy
    'pageSize': 10,      # maximum is 100
    'apiKey': secret     # your own API key
}

#making the request
response = requests.get(url, params=parameters)

#convert the response to JSON format and pretty print it
responseJASON = response.json()
pprint.pprint(responseJASON)


for i in responseJASON['articles']:
    print(i['title'])

#create and empty string 

textCombined = ''

#loop through all the headlines and add them to the textcombined 
for i in responseJASON['articles']:
    textCombined += i['title'] + ''   # add space after headlines
print(textCombined[0:300])

wordcloud = WordCloud(max_font_size=40).generate(textCombined)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()