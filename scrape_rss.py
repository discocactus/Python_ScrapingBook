
from xml.etree import ElementTree

tree = ElementTree.parse('rss2.xml')
root = tree.getroot()

for item in root.findall('channel/item'):
    title = item.find('title').text
    url = item.find('link').text
    print(url, title)