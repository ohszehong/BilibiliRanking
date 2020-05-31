from bs4 import BeautifulSoup
import requests
from datetime import date
from tabulate import tabulate 
from requests_html import HTMLSession


url = "https://www.bilibili.com/ranking/bangumi/13/0/7"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
biliweb = requests.get(url, headers=headers)

#request response from bili bili official website

bilisoup = BeautifulSoup(biliweb.text, 'html.parser')

#using BeautifulSoup to parse html response

rankingnumlist = [] #create a list to store ranking numbers only

rankingnamelist = [] #create a list to store ranking name only

rankingpointlist = [] #create a list to store ranking point only 


for rankingnum in bilisoup.find_all("div",class_="num",limit=10):

    rankingnumlist.append(rankingnum.text)

  
#using for loop to store top 10 ranking numbers into rankingnumlist[]
    
for rankingname in bilisoup.find_all('a',class_='title',limit=10):

    if len(rankingname.text) <=10:
        name = rankingname.text
    else:
        name = rankingname.text[:10] + "..."

    rankingnamelist.append(name)

#using for loop to store top 10 ranking name into rankingnamelist[]

for rankingpoint in bilisoup.find_all('div',class_='pts',limit=10): 

    rankingpointtxt = rankingpoint.text

    rankingpointonly = rankingpointtxt.split('综')

    rankingpointlist.append(rankingpointonly[0])

#using for loop to store top 10 rankingpoint into rankingpointlist[]


tableheaders = ["排名","动漫","综合得分"] #headers for table, there are 3 columns

datalist = [] #create a datalist to store tuples later on

i = 0 #create i to be used in for loop


while i<=9:

    individualnum = rankingnumlist[i]

    individualname = rankingnamelist[i]

    individualpoint = rankingpointlist[i]

    datarow = (individualnum,individualname,individualpoint)

    datalist.append(datarow)

    i += 1

#create for loop to seperate items in 3 lists and place them accordingly with tuples and store into datalist[]

stringnumlist = [] #create stringnumlist to store number of charaters in this list 

for string in rankingnamelist:

    stringnum = len(string)
    stringnumlist.append(stringnum)

maxchar = max(stringnumlist) #get the maximum characters in the list 

width = maxchar


print(tableheaders[0].ljust(3) + tableheaders[1].ljust(width+20) + tableheaders[2], end='')

print()

for item in datalist: 
    print (item[0].ljust(5) + item[1].ljust(width+20) + item[2])


#print(tabulate(datalist,headers=tableheaders,tablefmt="grid"))

#print headers and datalist[] using tabulate def














