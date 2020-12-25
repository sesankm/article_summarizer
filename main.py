from bs4 import BeautifulSoup as bs
import requests
from extractive_summarization import summarize
import sys

if __name__ == "__main__":
    num_sentences = int(sys.argv[1])
    watch = [i.upper() for i in sys.argv[2:]]
    summaries = {}
    for ticker in watch:
        # find exchange
        resp = requests.get("https://www.marketwatch.com/investing/stock/{}".format(ticker)).text
        soup = bs(resp, 'html.parser')
        exchange = soup.find('span', {'class': 'company__market'}).text.split(":")[1].strip()
        # find headlines
        if(exchange == "Nasdaq"):
            resp = requests.get("https://www.reuters.com/companies/{}.OQ/news".format(ticker)).text
        else:
            resp = requests.get("https://www.reuters.com/companies/{}/news".format(ticker)).text
        soup = bs(resp, 'html.parser')
        news = [i for i in soup.find_all("div", {"class" : "MarketStoryItem-container-3rpwz"})][:3]
        news = {i.find('a').text.strip():i.find('a')['href'] for i in news}
        for headline,url in news.items():
            resp2 = requests.get(url).text
            soup2 = bs(resp2, 'html.parser')
            text = "".join([i.text for i in soup2.find_all("p", {'class':"ArticleBody-para-TD_9x"})])
            summaries[headline] = summarize(text, num_sentences)

    for i,j in summaries.items():
        print(i)
        print(j, end='\n\n')