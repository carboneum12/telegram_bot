
import requests
from lxml import html
def mistakes_correction(object):
    link = f'https://www.google.ru/search?q={object}'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    req = requests.get(link, headers=headers).text
    parse = html.fromstring(req)
    google_text_without_mistakes = parse.xpath('//a[@class="gL9Hy"]/text()')
    google_text_with_mistakes = parse.xpath('//a[@id="fprsl"]//b[*]//i/text()')
    for n in google_text_with_mistakes:
        google_text_without_mistakes.append(n)
    return google_text_without_mistakes


