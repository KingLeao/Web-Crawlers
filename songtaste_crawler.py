#!/usr/bin/env python
# -*- coding: utf-8 -*-
#usage:
#start from a user,then all his friends'id will be stored in the "data.txt"
#---------------------------------import---------------------------------------
import urllib2
import re
import sys
import time
import socket
#------------------------------------------------------------------------------
def main():
    
    url = "http://www.songtaste.com/user/230345/frd/0"
    fixedUrlLen=30
    lastPage=''
    presentFrdId='1'
    presentUserId=''
    userList=['230345']
    showData = file('data.txt', 'w')
    showHtml = file('html.txt', 'w')
    presentPageFirstId=''    
    
    userCnt=0;
    while(userCnt<=5000):
        presentUserId=userList.pop(0)
        presentPage='1'
        stopSearching=0
        while stopSearching==0: #until all pages have been searched
            url=url[0:fixedUrlLen]       
            url+=presentUserId+'/frd/'        
            url+=presentPage
            print url
            keepRequest=1
            while keepRequest==1:
                req = urllib2.Request(url)
                try:
                    resp = urllib2.urlopen(url,timeout=1)     
                except urllib2.URLError:
                    print 'request fail' 
                except socket.timeout:
                    print 'request time out'   
                except socket.error,e:
                    print 'request time out'   
                else:
                    keepRequest=0
            html = resp.read()
            #print "respHtml=",html    
            showHtml.write(html)   
            startPos=html.find('BEGIN Frd')
            endPos=html.find('END Frd',startPos)
            print startPos,endPos
            if startPos==-1:
                break
            pos=startPos
            frdId=''
            count=0
            while pos>=startPos and pos <=endPos: #search all friends in current page
                pos=html.find('class="underline"',pos,endPos)
                if pos!=-1:
                    for i in range(15,0,-1):
                        if html[pos-i]>='0' and html[pos-i]<='9':  
                            frdId+=html[pos-i]
                    if count==0:
                        if frdId!=presentPageFirstId:
                            presentPageFirstId=frdId
                        else:
                            stopSearching=1
                            break
                    showData.write(presentUserId+' '+frdId+'\n')
                    if userCnt<=5000:
                        userList.append(frdId)
                    userCnt+=1
                    count+=1
                    frdId='' 
                    pos=pos+1      
      
            presentPage=chr(ord(presentPage)+1)
            print presentPageFirstId
            #showData.write('fuck')
            showData.flush()
            showHtml.flush()
            
    
###############################################################################
if __name__=="__main__":
    main()