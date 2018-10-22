from selenium.webdriver.chrome.options import Options
from selenium import webdriver

chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.bbc.co.uk/programmes/m0000pc1') #Browser goes to google.com
artists = driver.find_elements_by_class_name('artist')
tracks = driver.find_elements_by_xpath('//div[@class="segment__track"]//p')

print(len(tracks))

'''
Last few tracks on tracklist should be:
    
    Secret Agent Man (Female Version)
    Station to Station
    Friday's Child
    Heat (feat. Joanne Roberston) 
    Streetwise
    Don't Get Me Started
'''

    

