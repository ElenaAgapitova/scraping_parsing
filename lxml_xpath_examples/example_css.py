from lxml import etree

tree = etree.parse('web_example.html')
html = tree.getroot()
print(html.cssselect('title')[0].text)
print('----------------------')
print(html.cssselect('p')[0].text)
