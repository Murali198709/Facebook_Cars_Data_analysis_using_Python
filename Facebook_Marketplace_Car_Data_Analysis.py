from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
from datetime import datetime, timedelta, date
import calendar
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import datetime
from datetime import datetime, timedelta, date
import calendar
import csv


import csv
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

cars_by_user = input("Enter the cars you want to search for on facebook market place seperated by comma: ")
cars_model_year = input("Enter the car model year seperated by |: ")
enter_min_max_price = input("Enter min and max price that you are looking for seperated by comma: ")
enter_max_mileage = input("Enter max mileage: ")

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1 
})

driver = webdriver.Chrome(chrome_options=option, executable_path=r"/Users/muralitulluri/Documents/Dalplex_webscraping/chromedriver")
driver.get("https://www.facebook.com/marketplace/halifax/search?minPrice=6000&maxPrice=10000&query=Honda Accord&exact=false")
time.sleep(5)
#username = driver.find_element_by_id("email")
#password = driver.find_element_by_id("pass")

#username.send_keys("email")
#password.send_keys("password")

#driver.find_element_by_link_text("Log In").click()

#button3 = driver.find_element_by_xpath("//button[@class='_42ft _4jy0 _52e0 _4jy6 _4jy1 selected _51sy']")
#button3.click()
#time.sleep(10)

#searchbox = driver.find_element_by_xpath("//input[@placeholder='Search Marketplace']")
#searchbox.send_keys("Honda Accord")

#time.sleep(5)

#searchbox.send_keys(Keys.RETURN)

#email = driver.find_element_by_xpath("//input[@placeholder='Email or phone']")
#password = driver.find_element_by_xpath("//input[@placeholder='Password']")

#email.send_keys("email")
#password.send_keys("password")

#driver.find_element_by_link_text("login").click()

#login = driver.find_element_by_xpath("//div[@aria-label='Accessible login button']")
#login.click()
time.sleep(10)

cardata=pd.DataFrame()

def facebookcars(carmodel):
    driver.execute_script("window.open('');")# Switch to the new window and open URL B
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://www.facebook.com/marketplace/halifax/search?minPrice=6000&maxPrice=10000&query="+carmodel+"&exact=true")
    
    time.sleep(10)
    
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    for i in range(100):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(10)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    
    
    content = driver.page_source
    soup = BeautifulSoup(content)
    #soup=BeautifulSoup(response.content, 'html.parser')
    #soup
    price=[]
    #name=[a.get_text() for a in soup.findAll("div", {"class":"a8nywdso e5nlhep0 rz4wbd8a linoseic"})]
    price=[a.get_text() for a in soup.findAll("div", {"class":"a8nywdso e5nlhep0 rz4wbd8a ecm0bbzt btwxx1t3 j83agx80"})]
    
    #articles=soup.find_all("img", {"class":"idiwt2bm bixrwtb6 ni8dbmo4 stjgntxs k4urcfbm"})
    #articles=soup.find_all('img',class_='idiwt2bm bixrwtb6 ni8dbmo4 stjgntxs k4urcfbm')
    articles=soup.find_all('div',class_='j83agx80 lhclo0ds ihdl84by pmk7jnqg h119xb3h iylxurvu bo2ra7bd')
    #articles
    #b
    #b.find_all("alt",{"class":"idiwt2bm bixrwtb6 ni8dbmo4 stjgntxs k4urcfbm"})
    
    Car_Desc=[]
    for article in articles:
        Car_Desc.append(article.find('div',class_='rq0escxv j83agx80 buofh1pr datstx6m ggysqto6 exrn9cbp ojkyduve abpf7j7b l9j0dhe7 k4urcfbm').img['alt'])
        #Car_Link = article.find('div',class_='rq0escxv j83agx80 buofh1pr datstx6m ggysqto6 exrn9cbp ojkyduve abpf7j7b l9j0dhe7 k4urcfbm').img['src']
        #print(Car_Desc)
    
    car_links = soup.find_all('span',class_='a8c37x1j buofh1pr')
    
    Car_Link=[]
    for car_link in car_links:
        car_link = car_link.find('div',class_='kbiprv82')#.a['href']
        if car_link!=None:
            Car_Link.append("https://www.facebook.com"+car_link.a['href'])
            #print(Car_Link)
    #len(Car_Desc)
    #len(Car_Link)
    #len(price)
    mileage = soup.find_all('div',class_='a8nywdso e5nlhep0 rz4wbd8a ecm0bbzt')
    
    Car_Miles=[]
    for car_miles in mileage:
        miles = car_miles.find('span',class_='d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn mdeji52x e9vueds3 j5wam9gi b1v8xokw m9osqain')#.a['href']
        miles1 = miles.find('span',class_='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5').get_text()
        
        if not miles1.find(",")!=-1:
            Car_Miles.append(miles1)
            
    Car_Model=[]
    Car_Location=[]
    for car in Car_Desc:
        Car_Model.append(car.split(' in ',1)[0])
        Car_Location.append(car.split(' in ',1)[1])
    
    
        
    
    #df = pd.DataFrame({'Car_Model':Car_Model,'Car_Price':price,'Car_Location':Car_Location,'Car_Link':Car_Link}) 
    #df.to_csv('/Users/muralitulluri/Documents/Marketplace_CarData/Marketplace_Cardata.csv', index=False, encoding='utf-8')
    
        
    #2015 Honda accord v6 in Prince, PE
    
    
    mileage = soup.find_all('div',class_='a8nywdso e5nlhep0 rz4wbd8a ecm0bbzt')
    
    Car_Miles=[]
    for car_miles in mileage:
        miles = car_miles.find('span',class_='d2edcug0 hpfvmrgz qv66sw1b c1et5uql oi732d6d ik7dh3pa ht8s03o8 a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn mdeji52x e9vueds3 j5wam9gi b1v8xokw m9osqain')#.a['href']
        miles1 = miles.find('span',class_='a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5').get_text()
        
        if not miles1.find(",")!=-1:
            Car_Miles.append(miles1)
            
    if len(Car_Miles) < len(Car_Model):
        Car_Miles.append(0)
        
          
    df = pd.DataFrame({'Car_Model':Car_Model,'Car_Price':price,'Car_Mileage':Car_Miles,'Car_Location':Car_Location,'Car_Link':Car_Link}) 
    #df.to_csv('/Users/muralitulluri/Documents/Marketplace_CarData/Marketplace_Cardata'+datetime.today().strftime('%Y-%m-%d')+'.csv', mode='a',index=False, encoding='utf-8')
    
    
    #laptops = pd.read_csv("/Users/muralitulluri/Documents/Best_Buy_Laptops_Black_Friday_Deals.csv")
    global cardata
    cardata=cardata.append(df, ignore_index=True).drop_duplicates().reset_index(drop=True)
    
# In[286]:

for i in cars_by_user.split(','):
    facebookcars(i)


cars_by_user = input("Enter the cars you want to search for on facebook market place seperated by comma: ")
cars_model_year = input("Enter the car model year seperated by |: ")
enter_min_max_price = input("Enter min and max price that you are looking for seperated by comma: ")
enter_max_mileage = input("Enter max mileage: ")

cardata=cardata.sort_values('Car_Model').drop_duplicates(subset=['Car_Price', 'Car_Mileage'], keep='last')

Honda_Accord=cardata[cardata['Car_Model'].str.contains("Accord|accord|camry|Camry|Mazda6|mazda6|sonata|Sonata|Altima|altima")]
Honda_Accord_gt_2014 = Honda_Accord[Honda_Accord['Car_Model'].str.contains("2009|2010|2012|2013|2011|2014|2015")]

Honda_Accord_gt_2014.Car_Price = Honda_Accord_gt_2014['Car_Price'].str[2:8]
Honda_Accord_gt_2014.Car_Price = Honda_Accord_gt_2014['Car_Price'].str.replace(",","")
Honda_Accord_gt_2014.Car_Price = Honda_Accord_gt_2014['Car_Price'].str.replace("C","")
Honda_Accord_gt_2014.Car_Mileage = Honda_Accord_gt_2014['Car_Mileage'].str.replace(" ","")

Honda_Accord_gt_2014.Car_Mileage = Honda_Accord_gt_2014['Car_Mileage'].str.replace("K","000")

Honda_Accord_gt_2014.Car_Mileage = Honda_Accord_gt_2014['Car_Mileage'].str.replace("km","")
Honda_Accord_gt_2014.Car_Mileage = Honda_Accord_gt_2014['Car_Mileage'].str.replace("miles","")

Honda_Accord_Final = Honda_Accord_gt_2014[pd.to_numeric(Honda_Accord_gt_2014.Car_Price)<=10000]
Honda_Accord_Final = Honda_Accord_Final[pd.to_numeric(Honda_Accord_Final.Car_Mileage)<=200000]

Honda_Accord_Final

Distance=[]
for location in Honda_Accord_Final.Car_Location:
    
    driver_google = webdriver.Chrome(chrome_options=option, executable_path=r"/Users/muralitulluri/Documents/Dalplex_webscraping/chromedriver")
    driver_google.get("https://www.google.com/maps/dir/1333+South+Park+St,+Halifax,+NS+B3J+2K9/"+location.split(', ',1)[0]+"+"+location.split(', ',1)[1])
    time.sleep(10)
    #print(driver_google)
    driver_google = driver_google.execute_script("return document.body.innerHTML;")
    soup_maps = BeautifulSoup(driver_google)
    if(soup_maps.find('div',class_='Fk3sm fontHeadlineSmall delay-light')!=None):
        Distance.append(soup_maps.find('div',class_='Fk3sm fontHeadlineSmall delay-light').get_text())
    elif(soup_maps.find('div',class_='Fk3sm fontHeadlineSmall delay-medium')!=None):
        Distance.append(soup_maps.find('div',class_='Fk3sm fontHeadlineSmall delay-medium').get_text())
    else:
        Distance.append(soup_maps.find('div',class_='Fk3sm fontHeadlineSmall delay-heavy').get_text())


Honda_Accord_Final['Travel_time_from_PV'] = Distance
Honda_Accord_Final['KBB_Link'] = 'https://www.kbb.ca/'+Honda_Accord_Final['Car_Model'].str.split(pat=" ",n=2).str[1]+'/'+Honda_Accord_Final['Car_Model'].str.split(pat=" ",n=2).str[2]+'/'+Honda_Accord_Final['Car_Model'].str.split(pat=" ",n=2).str[0]+'/'
final_car_list=Honda_Accord_Final[['Car_Model','Car_Price','Car_Mileage','Car_Location','Travel_time_from_PV','KBB_Link','Car_Link']]

from prettytable import PrettyTable

table = PrettyTable(['Car_Model', 'Car_Price', 'Car_Mileage','Car_Location','Travel_time_from_PV','KBB_Link','Car_Link'])

table.add_row([final_car_list['Car_Model'],final_car_list['Car_Price'],final_car_list['Car_Mileage'],final_car_list['Car_Location'],final_car_list['Travel_time_from_PV'],final_car_list['KBB_Link'],final_car_list['Car_Link']])

print(table)  
    
