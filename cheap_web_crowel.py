import tkinter
from tkinter import ttk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

def scrape():
    global stop_second_thread
    link = enter.get()
    tekst = ""
    driver = None

    try:
        driver = webdriver.Firefox(service=service, options=firefox_options)
        wait = WebDriverWait(driver, 10)
        driver.get(link)
        print("a1")
        #footer = wait.until(EC.presence_of_element_located((By.ID, "footer")))
        print("a2")
        footer = driver.find_element(By.TAG_NAME, "footer")
        #footer = driver.find_element(By.ID, "footer")
        tekst = loud_tekst(footer,driver)
        print("a3")
        print(tekst)
        root.after(0, update_contact, tekst)

#progeam nie działa jeśli ma pobrać dużo danych
    # jast problem na poziomie loud_tekst i pobrania danych z zmiennej footer
    except Exception as e:
        print("a4")
        print(f"Wystąpił błąd: {e}")
        tekst = "Błąd w pobieraniu danych"
        root.after(0, update_contact, tekst)

    finally:
        print("a5")
        driver.quit()
        stop_second_thread = True  # Zatrzymanie animacji ładowania

def update_contact(tekst):
    print("a4.1")
    contact.config(text=tekst)
    print("a4.2")

def loud_tekst(footer,driver):
    tekst_in=""
    sleep=5
    print("a2.1")
    while tekst_in=="":
        time.sleep(sleep)
        print("a2.",sleep)
        tekst_in = footer.text
        time.sleep(sleep)
        print(tekst_in)
        if tekst_in=="":
            sleep+=1
    return tekst_in


def update_loading_text():
    if not stop_second_thread:
        current_text = contact.cget("text")
        if current_text == "Ładowanie...":
            contact.config(text="Ładowanie.")
        else:
            contact.config(text=current_text + ".")
        root.after(500, update_loading_text)
def find_contact():
    global stop_second_thread
    stop_second_thread = False  # Resetowanie flagi
    contact.config(text="Ładowanie")



    # Uruchomienie skryptu zbierającego dane i animacji ładowania w osobnych wątkach
    threa1 = threading.Thread(target=scrape)
    threa1.start()

    update_loading_text()


a1="Ładowanie."
a2="Ładowanie.."
a3="Ładowanie..."

stop_second_thread = False

firefox_options = Options()
firefox_options.add_argument("--headless")

service = Service('geckodriver.exe')


root =tkinter.Tk()
root.title("scraper")

labal=tkinter.Label(root,text="Wpisz link do strony firmy, by dostać kontakt  ąśżźćń")
enter=tkinter.Entry(root)
enter_button=tkinter.Button(root,text="wyszukaj",command=find_contact)
contact=tkinter.Label(root,text="------------------")
proggres=ttk.Progressbar(root,orient="horizontal",length=100,mode="determinate")

labal.pack()
enter.pack()
enter_button.pack()
contact.pack()
proggres.pack()

root.mainloop()
