import requests
from gettoken import get_token

def get_tweets():
  url = "https://cdn.syndication.twimg.com/tweet-result"
  select_token = 0
  
  search_keywords = "How much is the fish?"
  params = {
      "id":get_token()[select_token],
      "lang":"en",
      "keywords": search_keywords
  }
  
  payload = ""
  headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
      "Accept": "*/*",
      "Accept-Language": "en-US,en;q=0.5",
      "Accept-Encoding": "gzip, deflate, br",
      "Origin": "https://platform.twitter.com",
      "Connection": "keep-alive",
      "Referer": "https://platform.twitter.com/",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "cross-site",
      "Pragma": "no-cache",
      "Cache-Control": "no-cache",
      "TE": "trailers"
  }
  
  response = requests.request("GET", url, data=payload, headers=headers, params=params)
  
  print(response.text)
  return response.text
