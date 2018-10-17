from selenium.webdriver.chrome.options import Options
from selenium import webdriver

chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.bbc.co.uk/programmes/m0000pc1') #Browser goes to google.com
artists = driver.find_elements_by_class_name('artist')
tracks = driver.find_elements_by_class_name('segment__track')

for artist in artists:
    print(artist.text)
    
for track in tracks:
    print(track.text)

