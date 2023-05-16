from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pytesseract
from PIL import Image
import time
import random
import re
import pandas as pd
from copy import deepcopy

from PIL import ImageGrab

# Définir les coordonnées de la zone à capturer
left = 295   # Coordonnée X du coin supérieur gauche
top = 530    # Coordonnée Y du coin supérieur gauche
width = 180 # Largeur de la zone
height = 40 # Hauteur de la zone

# Instanciation du navigateur Firefox avec Selenium


LISTE_VOLS_url = ['https://www.skyscanner.fr/transport/d/CDG/2023-10-25/LHR/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/LHR/2023-10-25/CDG/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/FRA/2023-10-25/AMS/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/AMS/2023-10-25/FRA/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/BCN/2023-10-25/MAD/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/MAD/2023-10-25/BCN/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/FCO/2023-10-25/MUC/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/MUC/2023-10-25/FCO/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/IST/2023-10-25/ATH/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/ATH/2023-10-25/IST/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB',
                  'https://www.skyscanner.fr/transport/d/ARN/2023-10-25/CPH/LIS/2023-10-27/VCP/VCP/2023-11-04/LIS/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&infants=0&currency=EUR&market=FR&locale=en-GB']

LISTE_VOLS_url_copy = deepcopy(LISTE_VOLS_url)
PRIX = []

# URL de la page à figer
for url in LISTE_VOLS_url_copy:
    driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(10)
    delay = random.uniform(5, 9)
    time.sleep(delay)
    try:
        cookie_button = driver.find_element(By.XPATH, '//button[text()="OK"]')
        cookie_button.click()
    except:
        pass

    IMG = 'capture.png'

    screenshot = ImageGrab.grab(bbox=(left, top, left+width, top+height))
    screenshot.save(IMG)

    image_path = IMG
    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)
    number = int(re.findall(r'\d+', text)[0])

    PRIX.append(number)

    if number > 700:
        index = LISTE_VOLS_url.index(url)
        LISTE_VOLS_url.pop(index)
        PRIX.pop(index)

    driver.quit()


# Vérification si les deux listes ont la même longueur
if len(LISTE_VOLS_url) == len(PRIX):
    # Déterminer la longueur maximale de l'URL pour l'alignement
    max_url_length = max(len(url) for url in LISTE_VOLS_url)
    
    # Affichage du tableau
    print("LISTE_VOLS_url".ljust(max_url_length+5), "PRIX")
    for url, prix in zip(LISTE_VOLS_url, PRIX):
        print(url.ljust(max_url_length+5), prix)
else:
    print("Les listes ne sont pas de même longueur.")

# Création du dataframe pandas à partir des listes
df = pd.DataFrame({'LISTE_VOLS_url': LISTE_VOLS_url, 'PRIX': PRIX})

# Exportation du dataframe vers un fichier Excel
df.to_excel('notrepremiertableau.xlsx', index=False)
