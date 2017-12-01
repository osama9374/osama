from tika import parser,detector
import time
from dicttoxml import dicttoxml
import sys
from xml.dom.minidom import parseString
import glob
import os
import pysolr

solr = pysolr.Solr('http://localhost:8983/solr/', timeout=10)

reload(sys)
#so that we don't get unicode encode error
sys.setdefaultencoding('utf-8')
path = "C:\\Users\\HP\\Desktop\\test_folder\\"
directory = os.listdir(path)
start = time.time()
print(directory)
count = 0;
for fpath in directory:
#parsing through file to extract metadata and content
	file_path = path + fpath
	parsed = parser.from_file(file_path)

#detecting file type
	file_type = detector.from_file(file_path)
	print(file_type)
	parsed['id'] = str(count)

#converting output from python dict to xml
	xml = dicttoxml(parsed)
	
	solr.add([{"id":str(count),"content":parsed['content']}])

#formatting xml using xml.dom.minidom
	dom = parseString(xml)
	pretty_output = dom.toprettyxml()
	count = count + 1

#creating, writing(xml), closing file
	f = open(str(count)+ 'webpages','w+')
	f.write(pretty_output)
	f.close()

#time elapsed
#avg time between 0.5 and 0.7 seconds
#specs: 3.8 GB RAM, i5-4200U, 1.6GHZ x 4
end = time.time()
#print(parsed['metadata'].keys())
t_time  = end - start
print(t_time)
result = solr.search("Oracle Ebs")
for r in result:
        print r

