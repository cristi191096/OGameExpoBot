import sys, getopt
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import formations

def PrintHelp():
    print('main.py -f <fleet-formation> -e <number-of-expeditions>')

def getFleetFromPlanet(browser, planetName):
    planet = browser.find_element_by_xpath(f"//span[@class='planet-name ' and contains(text(), '{planetName}')]")
    planet.click()
    fleet = browser.find_element_by_xpath("//span[contains(text(), 'Fleet')]")
    fleet.click()

class HomePage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://s175-en.ogame.gameforge.com/')

        sleep(1)

    def go_to_login_page(self):
        login_tab = self.browser.find_element_by_xpath("//span[contains(text(), 'Log in')]")
        print(login_tab)
        login_tab.click()
       # return LoginPage(self.browser)

    def login(self, username, password):
        self.go_to_login_page()
        username_input = self.browser.find_element_by_css_selector("input[name='email']")
        password_input = self.browser.find_element_by_css_selector("input[name='password']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()
        server_button = self.browser.find_element_by_xpath("//span[contains(text(), 'Last played')]")
        server_button.click()


def login(browser, username, password):
    home_page = HomePage(browser)
    home_page.login(username, password)
    browser.switch_to.window(browser.window_handles[-1])
    accept_cookies = browser.find_element_by_xpath("//button[text()='Accept Cookies']")
    accept_cookies.click()

def sendFleet(browser):
    browser.find_element_by_id("continueToFleet2").click()
    password_input = browser.find_element_by_css_selector("input[name='position']").send_keys("16")
    browser.find_element_by_id("continueToFleet3").click()
    browser.find_element_by_id("missionButton15").click()
    browser.find_element_by_id("sendFleet").click()
    sleep(2)

def insertShips(browser, formation):
    current_ship_input = browser.find_element_by_css_selector("input[name='fighterLight']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["lightFighter"])
    current_ship_input = browser.find_element_by_css_selector("input[name='fighterHeavy']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["heavyFighter"])
    current_ship_input = browser.find_element_by_css_selector("input[name='cruiser']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["cruiser"])
    current_ship_input = browser.find_element_by_css_selector("input[name='battleship']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["battleship"])
    current_ship_input = browser.find_element_by_css_selector("input[name='interceptor']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["battleCruiser"])
    current_ship_input = browser.find_element_by_css_selector("input[name='bomber']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["bomber"])
    current_ship_input = browser.find_element_by_css_selector("input[name='destroyer']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["destroyer"])
    current_ship_input = browser.find_element_by_css_selector("input[name='deathstar']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["deathStar"])
    current_ship_input = browser.find_element_by_css_selector("input[name='reaper']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["reaper"])
    current_ship_input = browser.find_element_by_css_selector("input[name='explorer']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["pathFinder"])
    current_ship_input = browser.find_element_by_css_selector("input[name='transporterSmall']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["smallCargo"])
    current_ship_input = browser.find_element_by_css_selector("input[name='transporterLarge']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["largeCargo"])
    current_ship_input = browser.find_element_by_css_selector("input[name='colonyShip']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["colonyShip"])
    current_ship_input = browser.find_element_by_css_selector("input[name='recycler']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["recycler"])
    current_ship_input = browser.find_element_by_css_selector("input[name='espionageProbe']")
    if current_ship_input.is_enabled():
        current_ship_input.send_keys(formation["probe"])

def main(argv):
    fleetName = ''
    numberExpeditions = 0
    try:
        opts, args = getopt.getopt(argv,"hf:e:",["fleet=","expeditions="])
    except getopt.GetoptError:
        PrintHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            PrintHelp()
            sys.exit()
        elif opt in ("-f", "--fleet"):
            fleetName = arg
        elif opt in ("-e", "--expeditions"):
            numberExpeditions = int(arg)
    
    formation = formations.get[fleetName]

    print("Your formation is:")
    for key, value in formation.items():
        print(key, " : ", value)

    service = Service('chromedriver')
    service.start()

    browser = webdriver.Remote(service.service_url)
    browser.implicitly_wait(5)
    browser.maximize_window()

    login(browser, "YOUR EMAIL", "YOUR PASSWORD")

    for n in range(numberExpeditions):
        getFleetFromPlanet(browser, 'Home 2')
        insertShips(browser, formation)
        sendFleet(browser)

if __name__ == "__main__":
    main(sys.argv[1:])
