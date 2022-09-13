from bs4 import BeautifulSoup
import urllib.request
import re
import newspaper
import sys

arg=sys.argv[1]
parser = 'html.parser'
resp = urllib.request.urlopen("https://akharinkhabar.ir/"+arg, timeout=None)
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
i=0
if(arg!="story"):
    for link in soup.find_all('a', href=True):
        if(i==5):
            break
        if(re.match(f'/{arg}/[0-9].*',link['href'])!=None):
            i+=1
            article=newspaper.build_article("https://akharinkhabar.ir"+link['href'])
            article.download()
            article.parse()
            print("-"+article.title)
else:
    for link in soup.find_all('a', href=True):
        if(i==5):
            break
        if(re.match('/.*/[0-9].*',link['href'])!=None):
            i+=1
            article=newspaper.build_article("https://akharinkhabar.ir"+link['href'])
            article.download()
            article.parse()
            print("-"+article.title)