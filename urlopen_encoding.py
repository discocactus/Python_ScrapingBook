
import sys
from urllib.request import urlopen

f = urlopen('http://sample.scraping-book.com/dp')
encoding = f.info().get_content_charset(failobj="utf-8")
print('encoding:', encoding, file=sys.stderr)

text = f.read().decode(encoding)
print(text)