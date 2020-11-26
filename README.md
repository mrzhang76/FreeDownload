# Free Download V0.1 @mrzhang76  
This script is desgined to download articles cleanly from website  
You can use CSS selector to choose whether you want to download from the page or not  
## Requirements:
+ wkhtmltopdf:https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf  
After wkhtmltopdf , you need to set wkhtmltopdf bin path  
```
···
def getpdf(data,filename):
	config = pdfkit.configuration(wkhtmltopdf='*\wkhtmltopdf') # set your wkhtmltopdf  
	options = {
		'page-size': 'Letter',  
···
```
## Usage:
```
usage: freedownload.py [-h] [--u U] [--d D] [--ap AP] [--dp DP [DP ...]] [--c C] [--f F] [--p P]

optional arguments:
  -h, --help          show this help message and exit
  --u U               article url
  --d D, --dirpath D  set dirpath
  --ap AP             use css selectors to choose article
  --dp DP [DP ...]    use css selectors to choose what you want to del in article
  --c C, --cookie C   use cookie to get article from websites need to log in
  --f F, --file F     read url from file
  --p P, --proxy P    set website proxy
```
Notice:  *Use cookie to simulate login site is a experimental sexual function*  
  
---
Powered by www.mrzhang76.com
