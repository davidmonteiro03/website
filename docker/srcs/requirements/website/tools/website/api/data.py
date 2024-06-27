# import Python modules
from bs4 import BeautifulSoup # HTML parser
import json

# import utils
from . import utils

# Function to parse Liga Portugal data
# :param: json_data - JSON data
# :return: Liga Portugal data
def ligaportugal(json_data):
	result = {}
	result['name'] = utils.parse_name(json_data[0]['Description'])
	result['teams'] = []
	for club in json_data[0]['Classificacoes']:
		html = BeautifulSoup(features='html.parser').new_tag('html')
		head = BeautifulSoup(features='html.parser').new_tag('head')
		meta1 = BeautifulSoup(features='html.parser').new_tag('meta')
		meta1['charset'] = 'UTF-8'
		meta2 = BeautifulSoup(features='html.parser').new_tag('meta')
		meta2['name'] = 'viewport'
		meta2['content'] = 'width=device-width, initial-scale=1.0'
		link = BeautifulSoup(features='html.parser').new_tag('link')
		link['rel'] = 'stylesheet'
		link['href'] = 'https://www.ligaportugal.pt/styles/lpfpweb2017?v=iPacDQe4u9557mk1UUqiHJiiYudNamZxAyXY-1stU-Q1'
		body = BeautifulSoup(features='html.parser').new_tag('body')
		body['style'] = 'background-color: transparent'
		body['class'] = f'badge-80 t-{club["IdClube"]}'
		head.append(meta1)
		head.append(meta2)
		head.append(link)
		html.append(head)
		html.append(body)
		result['teams'].append(str(html))
	return result
