#coding = utf-8
from BeautifulSoup import BeautifulSoup
import urllib
import re
import os
import threading
import time
import pdb
import sys
import json
import csv
reload(sys) 
sys.setdefaultencoding('utf-8')

def read_web(pagenumber, artist_name, style):
	_url = 'https://www.wikiart.org/en/'+ artist_name +'/by-Style/'+ style+'?json=2&page=%s' % pagenumber
	return  urllib.urlopen(_url)

def parse_web(artist_name, style,save_path):
	print 'start getting the painting list of %s\n' % artist_name+" "+style
	count=1
	f1=open(save_path+"/%s_painting_main_list.txt" % artist_name,'w')
	f2=open(save_path+"%s_painting_download_list.txt" % artist_name,'w')
	while True:
		web=read_web(count,artist_name,style)
		dic=json.load(web)
		painting_list= dic['Paintings']
		if painting_list==None:
			break
		else:
			for i in range(len(painting_list)):
				image_download_url=painting_list[i]['image']
				image_main_url=painting_list[i]['paintingUrl']
				f2.write(image_download_url)
				f2.write('\n')
				f2.flush()
				f1.write(image_main_url)
				f1.write('\n')
				f1.flush()
			count=count+1
	print 'finished getting the painting list of %s\n' % style

			
def download_painting(artist_name,style,save_path):
	url_lists=[]
	count=0
	f=open(save_path+"%s_painting_download_list.txt" % artist_name)
	for l in f:
		l=l.strip()
		if not l:
			continue
		url_lists.append(l)
	f.close()
	dirname = save_path+"%s_paintins" % artist_name
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	while count < len(url_lists):
		url = url_lists[count]
		count += 1
		index=url.rfind('/')
		tem=list(url)
		tem[index]='_'
		urll=''.join(tem)
		filename=urll[urll.rfind('/'):]
		path = (dirname + filename)
		exists = os.path.exists(path)
		if not exists:
			print "Downloading %s" % filename[1:]
			urllib.urlretrieve(url,path)

def get_details(artist_name,style,save_path):
	print 'start getting the painting details of %s\n' % artist_name
	f=open(save_path+"%s_painting_main_list.txt" % artist_name)
	image_list=[]
	for l in f:
		l=l.strip()
		if not l:
			continue
		image_list.append('http://www.wikiart.org'+l)
	f.close()
	detail_list = []
	csvfile=file(save_path+"/detail.csv",'wb')
	writer=csv.writer(csvfile)
	writer.writerow(["Painting","Style","Genre","Tags","Date","Media","Period","artist"])
	count=0
	for i in range(len(image_list)):
		page= urllib.urlopen(image_list[i]).read().decode('utf-8','ignore')
		soup = BeautifulSoup(page)
		
		header=soup.findAll('div',{'class':'info-line painting-header'})
		temp=header[0].findAll('h1')
		title=temp[0].string
		creater=header[0].findAll('div',{'itemprop':'creator'})
		tempp=creater[0].findAll('span',{'itemprop':'name'})
		painter=tempp[0].a.string


		article=soup.findAll('div',{'class':'info-line'})
		row_list=[]
		for i in range(8):
			row_list.append("unknown")
		row_list[0]=(str(title))
		for item in article:
			#info=item.findAll('span',{'class':re.compile('.*')})
			#print info.string
			if str(item.span.string)=="Style:":
				row_list[1]=item.a.span.string
			
			if str(item.span.string)=="Genre:":
				row_list[2]=item.a.span.string
			
			if str(item.span.string)=="Tags:":
				date=item.findAll('span',{'itemprop':'keywords'})
				row_list[3]=date[0].a.string
			
			if str(item.span.string)=="Date:":
				date=item.findAll('span',{'itemprop':'dateCreated'})
				row_list[4]=date[0].string
			
			if str(item.span.string)=="Media:":
				row_list[5]=item.a.string
			
			if str(item.span.string)=="Period:":
				row_list[6]=item.a.string
		row_list[7]=painter
		writer.writerow(row_list)
		count=count+1
		print(count)
	csvfile.close()
	print 'start getting the painting details of %s\n' % style





if __name__=="__main__":
	artist_name = raw_input("Input the the artist's name you what:(eg: claude-monet)\n")
	style = raw_input("Input the the artist's style you what:(eg: surrealism)\n")
	save_path = raw_input("Input the path of the folder:(please add the / at the end)\n")
	if not os.path.exists(save_path):
		print("this path does not exsit and it is created!!!")
		os.mkdir(save_path)
	parse_web(artist_name, style,save_path)
	download_painting(artist_name, style,save_path)
	get_details(artist_name, style,save_path)
	
