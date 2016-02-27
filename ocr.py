#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, urllib, urllib2, json, os, base64, imp

def check_pkg(pkg_name):
	try:
		imp.find_module(pkg_name)
		return True
	except ImportError:
		return False

pil_installed = check_pkg('PIL') 

if pil_installed :
    from PIL import Image

def convert_to_jpg(image_path):
    try:
        img = Image.open(image_path)
        img.copy().save(image_path+'.jpg')
    except IOError:
        print('Error when open image: ' + image_path)
    finally:
        if img:
            img.close()    
            
    
url = 'http://apis.baidu.com/apistore/idlocr/ocr'

data = {}
data['languagetype'] = "CHN_ENG" # 语言类型: CHN_ENG(中英文) 或 ENG(英文)
data['fromdevice'] = "pc"
data['clientip'] = "10.10.10.0"
data['detecttype'] = "LocateRecognize"
data['imagetype'] = "1"



def print_usage_info():
    print('Usage: python Ocr.py [image_path]\n Note: The size of image should less than 300k')

def main(argv):
    filename = argv[-1]
    if not (not filename.endswith('Ocr.py')) and os.path.exists(filename):
        print_usage_info()
        return
    
    cache_image = False
    if not filename.lower().endswith('.jpg'):
        if pil_installed:
            convert_to_jpg(filename)
            filename = filename + '.jpg'
            cache_image = True
        else:
            print('PIL not installed')    
            print('Only support .jpg image!')
            print('Please convert image format yourself.')
            return
             
    with open(filename, 'rb') as f:  
        data['image'] = base64.b64encode( f.read() )  
        decoded_data = urllib.urlencode(data)
        req = urllib2.Request(url, data = decoded_data)

        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        req.add_header("apikey", "c9c59d0d4da208d4097b7aa53a323332")

        resp = urllib2.urlopen(req)
        content = resp.read()
        if(content):
            j = json.loads(content)
            if len(j['retData']) == 0:
                print("None")
            for rd in j['retData'] :
                print(rd['word'])
    
    if cache_image:
        os.remove(filename)
            

if __name__ == '__main__':
    main(sys.argv)