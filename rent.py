# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, time, os
import pickle
import re

from mechanize import Browser
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

from email.MIMEText import MIMEText
import smtplib



def get_mail_server():
    mailserver = smtplib.SMTP('smtp.googlemail.com')#'smtp.webfaction.com')
    
    mailserver.set_debuglevel(1)
    mailserver.ehlo()
    mailserver.starttls()    
    mailserver.login('', '')
    return mailserver
    #mailserver.close() #TODO: gc



url_58_1500_2000 = {
          '牡丹园':'http://bj.58.com/mudanyuan/zufang/0/b11i1/',          
    }


url_58_2000_3000 = {         
          '牡丹园':'http://bj.58.com/mudanyuan/zufang/0/b12i1/',
      
    }



url_58_3000_5000 = {
          '牡丹园':'http://bj.58.com/mudanyuan/zufang/0/b13i1/',          
    }


url_58_share = {
          '牡丹园':'http://bj.58.com/mudanyuan/hezu/0/',
          
          }

url_58_list = [url_58_1500_2000, url_58_2000_3000, url_58_3000_5000]#, url_58_3000_4500]

url_58_share_list = [url_58_share]


url_ganji_1500_2000 = {
          '牡丹园':'http://bj.ganji.com/fang1/mudanyuan/h1p4/',
          
          }


url_ganji_2000_2500 = {
          '牡丹园':'http://bj.ganji.com/fang1/mudanyuan/h1p5/',
          
          }

url_ganji_2500_3000 = {
          '牡丹园':'http://bj.ganji.com/fang1/mudanyuan/h1p6/',
         
          }


url_ganji_3000_5000 = {
          '牡丹园':'http://bj.ganji.com/fang1/mudanyuan/h1p7/',
          
          }


url_ganji_share = {
          '牡丹园':'http://bj.ganji.com/fang3/mudanyuan/a3/',
          
          }


url_ganji_list = [url_ganji_1500_2000, url_ganji_2000_2500, url_ganji_2500_3000, url_ganji_3000_5000]#, url_ganji_3000_5000]

url_ganji_share_list = [url_ganji_share]

individual_sites_dict = {
               '58':url_58_list, 'ganji':url_ganji_list}

individual_sites_share_dict = {
               '58':url_58_share_list, 'ganji':url_ganji_share_list}


broker_url_58_2500_3000 = {
          
          '牡丹园':'http://bj.58.com/mudanyuan/zufang/1/b5i1/',
          
    }

broker_url_58_3000_4500 = {          
          '牡丹园':'http://bj.58.com/mudanyuan/zufang/1/b6i1/',
          
    }

broker_url_58_list = [broker_url_58_2500_3000, broker_url_58_3000_4500]


broker_url_ganji_2500_3000 = {          
          '牡丹园':'http://bj.ganji.com/fang1/mudanyuan/a2h1p6/',          
          }


broker_url_ganji_3000_5000 = {          
          '牡丹园':'http://bj.ganji.com/fang1/mudanyuan/a2h1p7/',         
          }


broker_url_ganji_list = [broker_url_ganji_2500_3000, broker_url_ganji_3000_5000]


broker_sites_dict = {'ganji':broker_url_ganji_list,
               '58':broker_url_58_list}


to_addr_list = [
                u'youremail@gmail.com',
                u'someotheremail@gmail.com'
                ]

price_minimum = 1500
price_maximum = 3300


def sendEmail(mailserver, fromAddr, toAddrList, subject, content):
    print 'sending email...'
    #msg = MIMEText(content,  _charset='utf-8')
    msg = MIMEText(content)
    msg.set_charset('utf-8')
    msg['Subject'] = subject
    msg['From'] = fromAddr
    msg['To'] = toAddrList[0]
    mailserver.sendmail(fromAddr, toAddrList, msg.as_string())   
    print 'email sent!'
    
    #mailserver.close()
    


def get_rent_links(soup, site):
    rent_links = []
    if site == 'ganji':
        links = soup.findAll('a',href=re.compile(r'^/fang1/(.*).htm'))             
        for link in links:
            try:                
                tr = link.parent.parent
                link_price = tr.find('span', attrs={'class':'price'}).find('b').text
                price = int(link_price) 
                if price < price_minimum or price > price_maximum:
                    continue
                link_date = tr.find('span', attrs={'class':'pubtime'}).text               
                if '-' in link_date:                    
                    continue
                print 'posted today!'
                link_url = 'http://bj.ganji.com'+link['href']
                link_text = link.text
                
                link_addr = tr.find('p', attrs={'class':'list-word'}).findAll('a',attrs={'class':'adds'}, limit=2)
                link_addr_area = link_addr[0].text
                link_addr_community = link_addr[1].text
                rent_link = [link_url, link_price, link_addr_area, link_addr_community, link_text, link_date]                
                rent_links.append(rent_link)
            except  Exception, e:  
                print 'An error happened when parsing the page from ', site, e
                print 'The error happened when parsing the following rent info:', tr
                continue  
    if site == '58':
        links = soup.findAll('a', href=re.compile(r'x.shtml$'))
        print 'links:', links
        for link in links:
            try:                             
                tr = link.parent.parent
                if tr.find(attrs={'class':'ico tui'}):
                    print 'It is an ad.'
                    continue
                link_price = tr.find(attrs={'class':'pri'}).text                
                price = int(link_price) 
                if price < price_minimum or price > price_maximum:
                    continue
                link_date = tr.findAll('td', attrs={'class':'tc'})[-1].text                
                if '-' in link_date:                    
                    continue
                print 'posted today!'
                link_url = link['href']                
                link_text = link.text                
                link_addr = tr.findAll(attrs={'class':'a_xq1'})                 
                link_addr_area = link_addr[0].text                
                link_addr_community = link_addr[1].text                
                rent_link = [link_url, link_price, link_addr_area, link_addr_community, link_text, link_date]                
                rent_links.append(rent_link)                
            except  Exception, e:  
                print 'An error happened when parsing the page from ', site, e
                print 'The error happened when parsing the following rent info:', tr
                continue    
                                                       
                                                       
    return rent_links



def process_sites(sites_dict, rent_src):
    br = Browser()    
    for site in sites_dict.keys(): 
        print 'Searching site ', site
        all_rent_links = []  
        for site_urls in sites_dict.get(site):             
            all_locs_rent_links = []          
            for loc in site_urls.keys(): 
                print  >> sys.stderr, 'Looking for new rent for a price range in ', site, loc
                time.sleep(3)                
                result = br.retrieve(site_urls.get(loc))                 
                temp_file_name = result[0]
                html_f = open(temp_file_name)
                soup = BeautifulSoup(html_f)                
                rent_links = get_rent_links(soup,site)                
                all_locs_rent_links.extend(rent_links) 
            all_rent_links.extend(all_locs_rent_links)    

                             
        print >> sys.stderr, len(all_rent_links), 'links found!'        
        
        #TODO: any better way to do below
        try:
            f = open(site+'_'+rent_src,'r')
        except IOError:
            f = open(site+'_'+rent_src,'w')
            pickle.dump([],f)
            f.close()
            f = open(site+'_'+rent_src,'r')
                
        old_pure_rent_links = pickle.load(f)
        f.close()
        
        print >> sys.stderr, len(old_pure_rent_links), 'old links stored in file!'
        
        #below actually IS list of string!
        #new_all_rent_links = list(set(all_rent_links) - set(old_all_rent_links))
        new_all_rent_links = [] 
        #old_pure_links = [link[0] for link in old_all_rent_links]       
        new_pure_rent_links = []
        for l in all_rent_links:
            if not l[0] in old_pure_rent_links and not l[0] in new_pure_rent_links: 
                new_all_rent_links.append(l)
                #only the link info is stored in the file to save the space
                new_pure_rent_links.append(l[0])
        
        
        print >> sys.stderr, len(new_all_rent_links), ' of new rents found!'
        
        #think of using lambda TODO:
        if new_all_rent_links:            
            info = ('\n\n'.join(['   '.join(link) for link in new_all_rent_links])).encode('utf-8')
            print 'info', info 
            last_parag = "\n\n\n 去http://91biji.com/groups/%E7%A7%9F%E6%88%BF/bookmarkbook/管理你的看房记录（如果点击上面链接后看到想继续考虑的房子，你可以用91biji.com将其加入你在的租房小组。） \n\n 91biji.com 敬上" 
            content = '从 '+site+' 新找到的租房信息:\n\n'+info+last_parag
            mailserver = get_mail_server()  
            sendEmail(mailserver, u'sys.notebook@gmail.com', to_addr_list, '('+rent_src+')'+' 从 '+site+' 新找到的'+str(len(new_all_rent_links))+'条租房信息', content) 
            mailserver.close()
        
        old_pure_rent_links.extend(new_pure_rent_links)
        f = open(site+'_'+rent_src,'w')
        pickle.dump(old_pure_rent_links,f)
        f.close()


#TODO:check on size, check on date    
if __name__ == "__main__":
    rent_source = sys.argv[1]
    if rent_source == 'indiv':
        print 'looking for renting info from individual...'
        process_sites(individual_sites_dict, '个人房源')
        process_sites(individual_sites_share_dict, '个人房源合租')
    if rent_source == 'broker':    
        print 'looking for renting info from broker...'
        process_sites(broker_sites_dict, '经纪人房源')
        

    
    
        
        
    
