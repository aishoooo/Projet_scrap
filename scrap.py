#import Libraries
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import csv

#function URL
def User_URL(energie, marque, kms_max, kms_min, page, prix_max, prix_min, annees_max, annees_min) :
    url_lacentrale = 'https://www.lacentrale.fr/listing?energies={energy_url}&makesModelsCommercialNames={mark_url}&mileageMax={kms_max_url}&mileageMin={kms_min_url}&options=&page={page_second}&priceMax={price_max_url}&priceMin={price_min_url}&yearMax={years_max_url}&yearMin={years_min_url}'
    url = url_lacentrale.format(energy_url = energie, mark_url = marque, kms_max_url = kms_max, kms_min_url = kms_min, page_second = page, price_max_url = prix_max, price_min_url = prix_min, years_max_url = annees_max, years_min_url = annees_min)
    print(url)
    return url

#function request
def scrap_listing(url) :
    re = requests.get(url)
    print(re)
    return re.text

#function scrap & guive to the csv
def scrap(html_page, csv_writer):
    #import the object Beautifulsoup
    soup = BeautifulSoup(html_page, 'html.parser')
    cards = soup.find_all("div",'Vehiculecard_Vehiculecard_cardBody')
    
    #pour une card 
    for card in cards :
    
        #name of brand
        name_of_car = card.find("h3","Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2")
        name_complete_car = name_of_car.get_text()
        name_brand_car = ""
        name_begin = 0 
        while name_complete_car[name_begin] != " ":
            name_brand_car += name_complete_car[name_begin]
            name_begin += 1
        print(name_brand_car)
        
        #name of model car
        name_model_car = ""
        for begin2 in range(name_begin+1, len(name_complete_car)):
            name_model_car += name_complete_car[begin2]
        print(name_model_car)

        #motor
        motor = card.find("div","Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2")
        motor2 = motor.get_text()
        print(motor2)

        #chracteristic
        characteristic_list = []
        for characteristic in card.find_all("div","Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2"):
            characteristic_text = characteristic.get_text()
            characteristic_list.append(characteristic_text)
            print(characteristic_text)
        car_km_new = characteristic_list[1].replace(" ", "").replace("km", '').replace('\xa0', '')
        car_km_new = int(car_km_new)
        characteristic_list[1] = car_km_new
            
            
        
        #price
        price = card.find("span","Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2")
        price2 = price.get_text()
        #transformation int
        price_new = price2.replace(' ','').replace('€', '')
        price2 = price_new
        
        print(int(price2))
        print ("-------------------------------------------------")

        csv_script([name_brand_car,name_model_car,motor2,characteristic_list[0],characteristic_list[1],characteristic_list[2],characteristic_list[3],price2],csv_writer)


#function write
def csv_script(data,csv_writer):
    csv_writer.writerow([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]])
    


#function execute
def main():
    csv_document = open('file_test.csv', 'w')
    csv_writer = csv.writer(csv_document)
    csv_writer.writerow(['Brand', 'Model', 'Motor', 'Year', 'Kms', 'Box', 'Energy', 'Price'])


    for one_page in range (0,10):
        URL_request = User_URL('ess', 'BMW', '1000000000', '0', str(one_page), '1000000', '10', '2023', '1950')
        html_page = scrap_listing(URL_request)
        scrap(html_page, csv_document, csv_writer)
    csv_document.close()


#code execute
main()

