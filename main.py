import requests as req
import csv
from bs4 import BeautifulSoup as soup
import pandas as pd
from datetime import datetime, timedelta
import time

def daily_scraper():
    url="https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm"
    page=soup(
        req.get(url).content.decode("utf-8"),"lxml"
    )
    print("Page Successfully Scraped")
    t_obj=page.find("table",{"summary":"Henry Hub Natural Gas Spot Price (Dollars per Million Btu)"})
    rows=t_obj.find_all("tr")
    with open("data/output.csv","w",newline="") as oFile:
        writer=csv.writer(oFile)
        header=rows[0].find_all("th")
        writer.writerow([x.text.strip() for x in header])
        for i in rows:
            items=i.find_all("td")
            writer.writerow([x.text.strip() for x in items])
        print("Raw data writter to data/ folder")

def processor():
    df=pd.read_csv("data/output.csv")
    df=df.dropna(how="all",axis=0)
    colnames=list(df.columns)
    colnames.remove("Week Of")
    df=df.set_index("Week Of",drop=True)  
    dateList=[]
    priceList=[]
    for i in df.index:
        startDate=i.split(" to ")[0]
        for j in range(len(colnames)):
            price=df.at[i,colnames[j]]
            st=datetime.strptime(startDate,"%Y %b-%d")+timedelta(days=j)
            dateList.append(st.strftime("%b %d %Y"))
            priceList.append(price)
    outdf=pd.DataFrame(data={
        "Date":dateList,
        "Price":priceList
    })
    print("Data successfully cleaned and written to /data/output.csv")

    outdf.to_csv("data/output.csv",index=False)

if __name__ == "__main__":
    daily_scraper()
    processor()
