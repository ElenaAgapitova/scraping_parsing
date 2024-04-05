from lxml import etree

tree = etree.parse('web_example.html')

for i in tree.getroot():
    print(i.tag)
    for k in i:
        print(k.tag)
print('--------------------------------')
print(tree.find('body/p').text)
print('--------------------------------')
lst_elem = tree.findall('body/p')
for i in lst_elem:
    print(i.text)

print('--------------------------------')
print(tree.xpath('//title')[0].text)

print('--------------------------------')
print(tree.xpath('//title/text()')[0])

print('--------------------------------')
print(tree.xpath('//p/text()')[0])

print('--------------------------------')
lst = tree.xpath('//p')
for p in lst:
    text = ' '.join(map(str.strip, p.xpath('.//text()')))
    print(text)
