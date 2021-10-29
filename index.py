import requests
import csv
from bs4 import BeautifulSoup

list_of_urls = [
    'https://www.liveaquaria.com/product/2936/mbuna-mixed-cichlid?pcatid=2936&c=830+831+2936&s=ts&r=',
    'https://www.liveaquaria.com/product/6744/similis-corydoras-catfish?pcatid=6744&c=830+1535+6744&s=ts&r=',
    'https://www.liveaquaria.com/product/1889/guentheri-killifish?pcatid=1889&c=830+1535+1889&s=ts&r=',
    'https://www.liveaquaria.com/product/6581/mixed-color-dumbo-ear-super-delta-betta-male?pcatid=6581&c=830+1535+6581&s=ts&r=',
    'https://www.liveaquaria.com/product/6751/blue-phantom-l-128-plecostomus?pcatid=6751&c=830+837+6751&s=ts&r=',
    'https://www.liveaquaria.com/product/6752/green-phantom-l-200-plecostomus?pcatid=6752&c=830+837+6752&s=ts&r=',
    'https://www.liveaquaria.com/product/2823/scarlet-gem-badis?pcatid=2823&c=830+836+2823&s=ts&r=',
    'https://www.liveaquaria.com/product/6664/zebra-obliquidens?pcatid=6664&c=830+1535+6664&s=ts&r=',
    'https://www.liveaquaria.com/product/991/powder-blue-dwarf-gourami?pcatid=991&c=830+882+991&s=ts&r=',
    'https://www.liveaquaria.com/product/1889/guentheri-killifish?pcatid=1889&c=830+1745+1889&s=ts&r=',
    'https://www.liveaquaria.com/product/873/clown-loach?pcatid=873&c=830+885+873&s=ts&r=',
    'https://www.liveaquaria.com/product/3012/humphead-glassfish?pcatid=3012&c=830+836+3012&s=ts&r=',
    'https://www.liveaquaria.com/product/1889/guentheri-killifish?pcatid=1889&c=830+1535+1889&s=ts&r=',
    'https://www.liveaquaria.com/product/1074/badis?pcatid=1074&c=830+836+1074&s=ts&r=',
    'https://www.liveaquaria.com/product/974/dwarf-gourami?pcatid=974&c=830+882+974&s=ts&r=',
    'https://www.liveaquaria.com/product/1892/rachovi-killifish?pcatid=1892&c=830+1745+1892&s=ts&r=',
    'https://www.liveaquaria.com/product/863/gold-nugget-plecostomus?pcatid=863&c=830+837+863&s=ts&r=',
    'https://www.liveaquaria.com/product/983/marble-veil-angel?pcatid=983&c=830+879+983&s=ts&r=',
    'https://www.liveaquaria.com/product/7647/bushy-nose-l-144-plecostomus-albino-gold?pcatid=7647&c=830+837+7647&s=ts&r=',
    'https://www.liveaquaria.com/product/2942/gold-dust-molly?pcatid=2942&c=830+1101+2942&s=ts&r=',
    'https://www.liveaquaria.com/product/2089/black-molly?pcatid=2089&c=830+1101+2089&s=ts&r=',
    'https://www.liveaquaria.com/product/6581/mixed-color-dumbo-ear-super-delta-betta-male?pcatid=6581&c=830+1535+6581&s=ts&r='
]

fieldnames = ['Name','Care Level','Temperament','Color Form','Diet','Water Temp','Carbonate Hardness','pH','Max. Size','Origin','Family','Minimum Tank Size','Image']

with open('./fishData.csv',mode='a+',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
     
    for url in list_of_urls:
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        fishName = soup.find("span", class_="prodCommonName")
        fishName = fishName.get_text(strip=' ') if fishName is not None else print('WTF')
        statElements = soup.findAll("div", class_="quick_stat_entry")[:9]
        
        fishStats = {}
        fishRows = [fishStats]

        fishStats['Name'] = fishName

        for (i, stat) in enumerate(statElements):
            
            if i != 4:
                stat_label = stat.find('a').get_text(strip=" ")
                stat_val = stat.find('span', class_='quick_stat_value').get_text(strip=' ').replace("\"", "in")
                fishStats[stat_label] = stat_val
            else:
                multi_stats = stat.find('span', class_='quick_stat_value').get_text(strip=' ').split(',')
                
                for (j,newStat) in enumerate(multi_stats):
                    label = ''
                    val = ''

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
        
        imgDiv = soup.find("div", class_="product-image").find('img')

        fishStats['Image'] = "https://www.liveaquaria.com" +  imgDiv['src'] if imgDiv['src'] != "" else "not found at: " + url

        writer.writerow(fishStats) 

print("Done")

 
    

