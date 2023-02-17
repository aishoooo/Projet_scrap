#import Libraries
from bs4 import BeautifulSoup #instalation cmd: pip install beautifulSoup
from pprint import pprint
import requests #instalation cmd: pip install request
import csv


def user_url(energy, mark, kms_max, kms_min, page, price_max, price_min, years_max, years_min) :
    '''
    function to create a filter by an url

    Parameters:
        enrgie => str
        mark => str
        kms_max => str
        kms_min => str
        page => str
        price_max => str
        price_min => str
        years_max => str
        years_min => str

    Return:
        url => str
    '''

    url_lacentrale = 'https://www.lacentrale.fr/listing?energies={energy_url}&makesModelsCommercialNames={mark_url}&mileageMax={kms_max_url}&mileageMin={kms_min_url}&options=&page={page_second}&priceMax={price_max_url}&priceMin={price_min_url}&yearMax={years_max_url}&yearMin={years_min_url}'
    url = url_lacentrale.format(energy_url = energy, mark_url = mark, kms_max_url = kms_max, kms_min_url = kms_min, page_second = page, price_max_url = price_max, price_min_url = price_min, years_max_url = years_max, years_min_url = years_min) #line is for make the filter & remplace the var 
    print(url)
    return url

def scrap_listing(url) :
    '''
    function to request the url for make some research

    Parameters:
        url => str
    
    Return :
        re.text => str

    '''
    re = requests.get(url)
    print(re)
    return re.text

def scrap(html_page, csv_writer):
    '''
    function scrap & give to the csv for write
    
    Parameters:
        html_page => var
        csv_writer => var

    Return:
        the function has no return but the information is passed to the csv_sript function
    '''
    soup = BeautifulSoup(html_page, 'html.parser')
    cards = soup.find_all("div",'Vehiculecard_Vehiculecard_cardBody') #scrap card
    
    for card in cards :     #scrap for one card 
    
        name_of_car = card.find("h3","Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2")      #scrap all name of the car
        name_complete_car = name_of_car.get_text()
        name_brand_car = ""
        name_begin = 0      #var of itteration
        while name_complete_car[name_begin] != " ":     #isolation of name of the mark & scrap the name of brand
            name_brand_car += name_complete_car[name_begin]
            name_begin += 1
        print(name_brand_car)    
        
        name_model_car = ""
        for begin2 in range(name_begin+1, len(name_complete_car)):  #scrap the name of model car
            name_model_car += name_complete_car[begin2]
        print(name_model_car)
        

        
        motor = card.find("div","Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2")       #scrap motor
        motor2 = motor.get_text()
        print(motor2)

        
        characteristic_list = []
        for characteristic in card.find_all("div","Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2"):     # scrap chracteristic && get the text
            characteristic_text = characteristic.get_text()
            characteristic_list.append(characteristic_text)
            print(characteristic_text)
        car_km_new = characteristic_list[1].replace(" ", "").replace("km", '').replace('\xa0', '') #transformation de km in int by function replace
        car_km_new = int(car_km_new)
        characteristic_list[1] = car_km_new
            
            
        
        #scrap the price & get the text
        price = card.find("span","Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2")
        price2 = price.get_text()
        #transformation price in int
        price_new = price2.replace(' ','').replace('€', '')
        price2 = price_new
        print(int(price2))
        print ("-------------------------------------------------")

        csv_script([name_brand_car,name_model_car,motor2,characteristic_list[0],characteristic_list[1],characteristic_list[2],characteristic_list[3],price2],csv_writer) #transmition the var


def csv_script(data,csv_writer):
    '''
    function for write

    Parameters:
        data => list
        csv_writer => var
    
    Return:
        No return, the information is written in the csv file
    
    '''
    csv_writer.writerow([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]])
    
def error(soup):
    """
    function to manage if there is no error

    Parameters:
        soup => var

    Return:
        error_info => int

    """
    error_info = soup.find('span',"Text_Text_text Text_Text_headline2")
    error_info2 = error_info.get_text()
    error_info = error_info2.replace(' ','').replace('\xa0', '')
    error_info = int(error_info)
    return(error_info)
    
def main():
    ''' 
    function execute 
    Paramters : 
        Nothing
    Return:
        Nothing
    '''
    csv_document = open('file_test.csv', 'w')   #open the document csv
    csv_writer = csv.writer(csv_document)
    csv_writer.writerow(['Brand', 'Model', 'Motor', 'Year', 'mileage', 'Box', 'Energy', 'Price'])
    url_request = user_url('ess', 'BMW', '1000000000', '0', 1, '1000000', '10', '2023', '1950')
    html_page = scrap_listing(url_request)
    soup = BeautifulSoup(html_page, 'html.parser')
    error_info = error(soup)
    
    if error_info > 0 :
        for one_page in range (1,11):   #loop for scrap 11 pages
            url_request = user_url('ess', 'BMW', '1000000000', '0', str(one_page), '1000000', '10', '2023', '1950') #filter for people to reschearch the car 
            html_page = scrap_listing(url_request)  #request
            scrap(html_page, csv_writer)
    else:
        print("error 0 annonce")
    csv_document.close()



main()  #code execute

