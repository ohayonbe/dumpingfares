import pychrome
import psutil

# Récupérer le processus Chrome en cours d'exécution
chrome_process = None
for process in psutil.process_iter():
    if process.name() == "chrome.exe":
        chrome_process = process
        break

if not chrome_process:
    print("Google Chrome n'est pas en cours d'exécution.")
    exit()

# Récupérer le port de débogage distant de Chrome
debugging_port = None
for conn in chrome_process.connections():
    if conn.laddr.port != 0 and conn.status == "LISTEN":
        debugging_port = conn.laddr.port
        break

if not debugging_port:
    print("Le port de débogage distant de Chrome n'a pas été trouvé.")
    exit()

# Créer une classe de rappel pour gérer les événements de Chrome
class ChromeCallbackHandler(object):
    def __init__(self):
        self.links = []

    # Fonction appelée lorsque les événements Network.requestWillBeSent sont déclenchés
    def request_will_be_sent(self, **kwargs):
        request = kwargs.get('request')
        url = request.get('url')
        self.links.append(url)

# Créer un navigateur Chrome
browser = pychrome.Browser(url=f"http://127.0.0.1:9222")

# Créer une instance de l'onglet
tab = browser.new_tab()

# Créer un gestionnaire de rappels
callback_handler = ChromeCallbackHandler()

# Ajouter le rappel pour gérer les événements Network.requestWillBeSent
tab.Network.requestWillBeSent = callback_handler.request_will_be_sent

# Ouvrir l'onglet
tab.start()

# Parcourir tous les onglets ouverts dans Chrome
for target in browser.targets():
    if target.get('type') == 'page':
        # Activer l'onglet cible
        tab.set_target(target)

        # Attendre que l'onglet soit prêt
        tab.wait(1)

        # Exécuter le script JavaScript pour obtenir les liens
        tab.Runtime.evaluate(expression="Array.from(document.getElementsByTagName('a')).map(a => a.href)", returnByValue=True)

        # Attendre quelques secondes pour permettre à JavaScript de s'exécuter
        tab.wait(2)

# Afficher les liens récupérés
print(callback_handler.links)

# Fermer l'onglet
tab.stop()
