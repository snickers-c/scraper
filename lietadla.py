from bs4 import BeautifulSoup
import requests
import re
import csv
def get_product_names(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        product_h2_tags = soup.find_all('h2')
        product_urls = [h2.find('a')['href'] for h2 in product_h2_tags if h2.find('a')]
        # print(product_urls)
        return product_urls
    except requests.exceptions.RequestException as e:
        print("Error fetching page:", e)
        return None
    
def search_product_by_name(product_name, arr ):
    base_url = 'https://www.modelsnavigator.com'
    product_url = base_url + '-'.join(product_name.lower().split())
    try:
        response = requests.get(product_url)
        response.raise_for_status()
        if response.status_code == 200:
            # print("Product Found:", product_name)
            # print("Product URL:", product_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            product_code_element = soup.find('td', string=re.compile(r'Objednávací kód:'))
            if product_code_element:
                product_code = product_code_element.find_next_sibling('td').text.strip()
                tag= soup.find('a' ,id= "add_to_cart_button")               
                href_value = tag['href']
                buxus_id = href_value.split('product_id=')[1].split('&')[0]
                arr += product_code + "~" + "https://www.modelsnavigator.com/buxus/system/page_details.php?page_id="+buxus_id + "#id9`"
                # print("Product Code:", product_code)
                return arr    
            else:
                print("Product code not found.")
                return ""
        else:
            print("Product not found:", product_name)
    except requests.exceptions.RequestException as e:
        print("Error searching for product:", e)

def search_product_by_code(product_code):
    url = 'https://www.aviationmegastore.com/en/quicksearch/{}'.format(product_code)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text 
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    
def extract_product_count(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    displayed_div = soup.find('div', class_='displayed')
    if displayed_div:
        product_count_text = displayed_div.text.strip()
        product_count = product_count_text.split()[0] 
        return product_count
    else:
        return None
        
if __name__ == "__main__":
    data = [['objednavaci kod;', 'link na buxus']]
    filename = "vystup5.csv"
    stringy = ""
    stringus = ""
    pocet = 0
    # dkaowdawddawddawddd
    
    spodnahranica = input("Zadajte spodnu hranicu rozsahu ktoru chcete pozriet:")
    hornahranica = input("Zadajte hornu hranicu rozsahu ktoru chcete pozriet:")
    url = 'https://www.modelsnavigator.com/sk/modely-lietadiel?stav_skladu=1179&page='+spodnahranica+'-'+hornahranica+''
    product_names = get_product_names(url)
    if product_names:
        print("Product Names:")
        for product_name in product_names:
            print("- ", product_name)
            stringus += search_product_by_name(product_name, stringy)
            print("new line stringus",stringus)
    else:
        print("No product names found.")
    # print("vypis pola: " + stringus)
    
    for row in stringus.split("`"):
        if row != "":
            ares = row.split("~")
            product_code = ares[0]
            if len(ares) > 1:
                bxs = ares[1]
            else:
                print("ares does not have a second element")

            # bxs = ares[1]
            result = search_product_by_code(product_code)
            if result:
                product_count = extract_product_count(result)
                print("\nSearch result for product code", product_code + " " + bxs + ":")
                # data.append([product_code+";", bxs])
                if product_count:
                    print("Number of products displayed:", product_count)
                    
                    if product_count == '0':
                        data.append([product_code+";",bxs])
                        pocet = pocet+1
                        with open(filename, 'w', newline='') as csvfile:
                            csvwriter = csv.writer(csvfile)
                            csvwriter.writerows(data)
                            
                else:
                    print("No product count found.")
            else:
                print("No result found for product code", product_code)
    print('Do suboru bolo danich ' , pocet)
    input("Press any key to exit...")