import requests
import csv
from bs4 import BeautifulSoup

result = requests.get('https://www.liveaquaria.com/product/2936/mbuna-mixed-cichlid?pcatid=2936&c=830+831+2936&s=ts&r=')
soup = BeautifulSoup(result.text,'html.parser')

fishName = soup.find("span",class_="prodCommonName").get_text(strip=' ')
statElements = soup.findAll("div",class_="quick_stat_entry")[:9]

fishStats = {}
fishRows = [fishStats]
fieldnames = ['Care Level','Temperament','Color Form','Diet','Water Temp','Carbonate Hardness','pH','Max. Size','Origin','Family','Minimum Tank Size','Image']

for (i,stat) in enumerate(statElements):
    if i != 4:
        stat_label = stat.find('a').get_text(strip=" ")
        stat_val = stat.find('span',class_='quick_stat_value').get_text(strip=' ').replace("\"", "in")
        fishStats[stat_label] = stat_val
    else:        
        multi_stats = stat.find('span',class_='quick_stat_value').get_text(strip=' ').split(',')
        
        for (j,newStat) in enumerate(multi_stats):
            if j == 0:
                label = 'Water Temp'
                val = newStat[:-3]
            elif j == 1:
                label = 'Carbonate Hardness'
                val = newStat[4:]
            else:
                label = 'pH'
                val = newStat[4:]
            fishStats[label] = val
# fishStats['Image'] = soup.find("div",class_="product-image")
with open('./fishData.csv',mode='a+',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(fishRows)

print(fishRows)
    

