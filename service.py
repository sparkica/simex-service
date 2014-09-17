from flask import Flask
from flask.ext import restful
from flask.ext.restful import Resource, reqparse

from lxml import html
import urllib2
import json


app = Flask(__name__)
api = restful.Api(app)

parser = reqparse.RequestParser()
parser.add_argument('url', type=str, location='form')
parser.add_argument('xpath', type=str, location='form')
parser.add_argument('attribute', type=str, location='form')

class SimpleExtractor(Resource):
	def post(self, **kwargs):
		args = parser.parse_args()
		source_url = args['url']
		element_xpath = args['xpath']
		element_attribute = args['attribute']

		result = self.parse_html(source_url, element_xpath, element_attribute)
		results = {'elements': [{'value': result }]}
		return json.dumps(results)

	def get(self):
		results = {'elements': [{'value':result}]}
		return json.dumps(results)


	def parse_html(self, source_url, element_xpath="/title", element_attribute=None):
		request = urllib2.urlopen(source_url)
		page = request.read()
		tree = html.fromstring(page)

		elements = tree.xpath(element_xpath)

		if len(elements) == 0:
			return ''

		elem_value = elements[0].attrib[element_attribute] if element_attribute else elements[0].text
		return elem_value


class BaseExtractor(Resource):
	def get(self):
		return {'value':'A simple extraction service'}

api.add_resource(BaseExtractor, '/')
api.add_resource(SimpleExtractor, '/extract')

if __name__ == '__main__':
	app.run(debug=True)
