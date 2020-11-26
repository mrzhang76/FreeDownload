import argparse
import chardet
import pdfkit 
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileMerger
import urllib3

def arg():
	parser = argparse.ArgumentParser()
	parser.add_argument('--u', type=str,  help='article url')
	parser.add_argument('--d','--dirpath', type=str,help='set dirpath')
	parser.add_argument('--ap', type=str, help='use css selectors to choose article')
	parser.add_argument('--dp', type=str, nargs='+',help='use css selectors to choose what you want to del in article')
	parser.add_argument('--c','--cookie',type=str,help='use cookie to get article from websites need to log in')
	parser.add_argument('--f','--file',type=str,help='read url from file ')
	parser.add_argument('--p','--proxy',type=str,help='set website proxy ')
	return parser

def getpdf(data,filename):
	config = pdfkit.configuration(wkhtmltopdf='*\wkhtmltopdf.exe') # set your wkhtmltopdf  
	options = {
		'page-size': 'Letter',  
		'margin-top': '0.75in',  
		'margin-right': '0.75in',  
		'margin-bottom': '0.75in',  
		'margin-left': '0.75in',  
		'encoding': "UTF-8",  
		'custom-header': [  
			('Accept-Encoding', 'gzip')  
		],  
		'cookie': [  
			('cookie-name1', 'cookie-value1'),  
			('cookie-name2', 'cookie-value2'),  
		],  
		'outline-depth': 10,  
	}
	try:
		pdfkit.from_file(data, filename, configuration=config,options=options) 
	except:
		print('Some resources on the web page cannot be downloaded and have been skipped')
		pass

def deltag(html,css_path):
	tag= html.select(css_path)[0]
	if(tag.get('class')):
		for div in html.find_all(tag.name,class_=tag['class']): 
			div.decompose()
	else:
		for div in html.find_all(tag.name,id=tag['id']): 
			div.decompose()
	return html

def loadhtml(article_title,html,charset,dirpath):
	temp_file = open(dirpath+"/"+article_title+".html","a+",encoding=charset)
	temp_file.write(str(html))
	temp_file.close()
	
def gethtml(url,cookie,proxies):
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
		'Cookie':cookie
	}
	req = requests.get(url=url,proxies=proxies,headers=headers,verify=False)
	html = req.text
	charset = req.encoding
	data = BeautifulSoup(html,'lxml')
	return data,charset

def readfile(filename):
	file = open(filename,"r",encoding="utf-8")
	data = []
	for line in file.readlines():
		data.append(line.strip('\n'))
	file.close()
	return data
	
def main(url,cookie,csspath,delcsspaths,proxies,dirpath):
	html,charset = gethtml(url,cookie,proxies)
	article_title = html.select('title')[0].string
	data = html.select(csspath)[0]
	if(delcsspaths):
		for delcsspath in delcsspaths:
			article = deltag(data,delcsspath)
	else:
		article = data
	loadhtml(article_title,article,charset,dirpath)
	getpdf(dirpath+"/"+article_title+".html",dirpath+"/"+article_title+".pdf")
	print("suceess download article from:"+url+"\n")

if __name__ == '__main__':
	urllib3.disable_warnings()
	parser = arg()
	args = parser.parse_args()
	print('freedownload.py v0.1@mrzhang76\n\n')
	url = args.u
	csspath = args.ap
	delcsspaths = args.dp
	filename = args.f

	if(filename):
		urls = readfile(filename)
		for url in urls:
			print("url:\t"+url)
	if(url):
		print("url:\t"+url)
	if(csspath):
		print("article:\t"+csspath)
	if(delcsspaths):
		for delcsspath in delcsspaths:
			print("del tag:\t"+delcsspath)
	if(args.d):
		dirpath = args.d
		print(dirpath)
	else:
		dirpath = './'
	if(args.c):
		cookie = args.c 
		print("cookie:\t"+cookie)
	else:
		cookie = ''
	
	if(args.p):
		proxies = {
			'http':args.p,
			'https':args.p
		}
		print("proxy:")
		print(proxies)
	else:
		proxies = {}
	print("\n")

	if(filename):
		for url in urls:
			main(url,cookie,csspath,delcsspaths,proxies,dirpath)
	else:
		main(url,cookie,csspath,delcsspaths,proxies,dirpath)