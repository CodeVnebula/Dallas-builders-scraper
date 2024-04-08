from bs4 import BeautifulSoup
import requests
import csv
import random
import time

"""
    Note:
        Please don't move AUTOMOTIVE category link index from current 
        index 1 as it may cause errors due to the different built of 
        its content. Script logic is Meant to work well with current 
        state, Please also note that adding new links may not be working 
        as excepted because website has different attributes in html 
        content, which may not be implemented in Script logic at the 
        moment.
"""

urls = [
    "https://web.dallasbuilders.com/AUDIOVIDEO",                                    # 0 AUDIOVIDEO
    "https://web.dallasbuilders.com/AUTOMOTIVE/Huffines-Commercial-Sales-102",      # 1 AUTOMOTIVE !!! Please don't move this link to another index
    "https://web.dallasbuilders.com/BATH",                                          # 2 BATH
    "https://web.dallasbuilders.com/BUILDERS-LAND-DEVELOPER",                       # 3 BUILDERS-LAND-DEVELOPER
    "https://web.dallasbuilders.com/BUILDERS-MULTIFAMILY",                          # 4 BUILDERS-MULTIFAMILY
    "https://web.dallasbuilders.com/BUILDERS-REMODELER",                            # 5 BUILDERS-REMODELER
    "https://web.dallasbuilders.com/BUILDERS-RESIDENTIAL",                          # 6 BUILDERS-RESIDENTIAL
    "https://web.dallasbuilders.com/CLEANINGRESTORATIONMAINTENANCE",                # 7 CLEANINGRESTORATIONMAINTENANCE
    "https://web.dallasbuilders.com/CONCRETE",                                      # 8 CONCRETE
    "https://web.dallasbuilders.com/DESIGNARCHITECTURAL-SERVICES",                  # 9 DESIGNARCHITECTURAL-SERVICES
    "https://web.dallasbuilders.com/DOORS",                                         # 10 DOORS
    "https://web.dallasbuilders.com/HVAC",                                          # 11 HVAC
    "https://web.dallasbuilders.com/INSULATION"                                     # 12 INSULATION
]
print("Estimated time to scrape all data: (+-)2 minutes")
count = 0
with open('DallasBuilders.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Business Name', 'Business Address', 'Contact Name', 'Contact Phone', 'Website URL']       # Determining headers of fields in the csv file
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    i = 1
    for index, url in enumerate(urls):
        if index == 1:
            builder_category = url.split('/')
            builder_category = builder_category[-2]
        else:
            builder_category = url.split('/')
            builder_category = builder_category[-1]
        print()
        
        print(f"Waiting for {builder_category} page response...")
        response = requests.get(url)
        time.sleep(random.randrange(1, 4))
        
        content = response.text
        soup = BeautifulSoup(content, 'lxml')

        """
            Below is the case of AUTOMOTIVE url page which is a bit different 
            from others and it needed little bit different logic of scraping 
            needed data. If you change index of AUTOMOTIVE url please change 
            index == 1 to respective index in the if statement down below.
        """
        if index == 1:
            tabber_div = soup.find('div', class_ = "tabber")        
            listing = tabber_div.find('div', class_ = "ListingDetails_Level1_HEADERBOXBOX")
            
            business_name = listing.h2.text
            
            street_address = listing.find('span', itemprop = "street-address")
            locality = listing.find('span', itemprop = "locality")
            region = listing.find('span', itemprop = "region")
            post_code = listing.find('span', itemprop = "postal-code")
            business_address = street_address.text + ', ' + locality.text + ' ' + region.text + ', ' + post_code.text

            contact_name = listing.find('span',  class_ = "ListingDetails_Level1_MAINCONTACT")
            contact_name = contact_name.a.text
            
            contact_phone = listing.find('span',  class_ = "ListingDetails_Level1_MAINCONTACT")
            contact_phone = contact_phone.text.replace('Mike Stubbs', '')
            contact_phone = contact_phone.split('x')
            contact_phone = contact_phone[0]
            contact_phone = contact_phone.strip()

            link = listing.find('span', class_ = "ListingDetails_Level1_VISITSITE")
            business_link = link.a['href']
            count += 1
            writer.writerow({                        
                'Business Name': business_name,         
                'Business Address': business_address,               
                'Contact Name': contact_name,             
                'Contact Phone': contact_phone,
                'Website URL' : business_link
            })
            print(f"Company N{i} scraped")
            i += 1

        else:
            """
            Below is the other cases of the urls which are mostly the same 
            in their html content
            """

            tabber_div = soup.find(id="tabber1")        # Outer div, listed companies are placed in this one
            listings = tabber_div.find_all('div', class_ = "ListingResults_All_CONTAINER")  # this gets each listed company info
            

            for listing in listings:
                business_name_span = listing.find('span', itemprop = "name")
                business_name = business_name_span.a.text       # Got business name which is placed in span with itemprob attr "name"
                
                street_address = listing.find('span', itemprop = "street-address")
                if street_address != None:
                    locality = listing.find('span', itemprop = "locality")
                    region = listing.find('span', itemprop = "region")
                    post_code = listing.find('span', itemprop = "postal-code")

                    business_address = street_address.text + ', ' + locality.text + ' ' + region.text + ', ' + post_code.text
                else:
                    business_address = None 
                try:
                    contact_name_div = listing.find('div', class_ = "ListingResults_Level1_MAINCONTACT")
                    contact_name = contact_name_div.text
                except:
                    contact_name_div = listing.find('div', class_ = "ListingResults_Level2_MAINCONTACT")
                    if contact_name_div != None: 
                        contact_name = contact_name_div.text
                    else:
                        contact_name_div = listing.find('div', class_ = "ListingResults_Level4_MAINCONTACT")
                        if contact_name_div != None: 
                            contact_name = contact_name_div.text
                        else:
                            contact_name == None
                    
                """
                    contact_phone may be empty as few companies do not have contact phone 
                    placed on website
                """
                
                contact_phone_object = listing.find('div', class_ = "ListingResults_Level1_PHONE1")
                if contact_phone_object != None:
                    contact_phone = contact_phone_object.text
                else:
                    contact_phone_object = listing.find('div', class_ = "ListingResults_Level2_PHONE1")
                    if contact_phone_object != None:
                        contact_phone = contact_phone_object.text
                    else:
                        contact_phone_object = listing.find('div', class_ = "ListingResults_Level4_PHONE1")
                        if contact_phone_object != None:
                            contact_phone = contact_phone_object.text
                        else:
                            contact_phone = None
                
                """
                    business_link may be empty as some of the companies do not have website 
                    links placed on the page.
                """
                business_link_obj = listing.find('span', class_ = "ListingResults_Level1_VISITSITE")
                if business_link_obj != None:
                    business_link = business_link_obj.a['href']
                else:
                    business_link_obj = listing.find('span', class_ = "ListingResults_Level2_VISITSITE")
                    if business_link_obj != None:
                        business_link = business_link_obj.a["href"]
                    else:
                        business_link_obj = listing.find('span', class_ = "ListingResults_Level2_VISITSITE")    
                        if business_link_obj != None:
                            business_link = business_link_obj.a['href']
                        else:
                            business_link = None
                if business_link != None:
                    count += 1

                writer.writerow({                        
                    'Business Name': business_name,         
                    'Business Address': business_address,       
                    'Contact Name': contact_name,            
                    'Contact Phone': contact_phone,
                    'Website URL' : business_link
                }) 
                print(f"Company N{i} scraped")
                i += 1

print("Scraped data successfully moved into file - (DallasBuilders.csv)")   # Excepted amount 700+
print(f"Found {count} sites with website links!", end="\n\n")   # Excepted amount 270+
