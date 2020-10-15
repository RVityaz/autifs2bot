#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re


Session = requests.Session()
COOKIE_requestVerificationToken = Session.get('https://student.amizone.net').cookies['__RequestVerificationToken']
ASPXAUTH = None
__version__ = "0.1 beta"


def login(amizone_id, password):
	global ASPXAUTH
	LoginVerificationToken = re.search(r'<form action="\/" class=" validate-form" id="loginform" method="post" name="loginform"><input name="__RequestVerificationToken".{0,20}value=".{0,110}\/>', Session.get('https://student.amizone.net').text)[0][148:-4]
	headers = {
		"Cookie": "__RequestVerificationToken=" + COOKIE_requestVerificationToken,
		"Host": "student.amizone.net",
		"Origin": "https://student.amizone.net",
		"Referer": "https://student.amizone.net/",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
	}
	formData = {
	    "__RequestVerificationToken": LoginVerificationToken,
	    "_UserName": amizone_id,
	    "_QString": "",
	    "_Password": password,
	}
	login_response = Session.post('https://student.amizone.net', headers=headers, data=formData)
	ASPXAUTH = Session.cookies['.ASPXAUTH']
	return 200 if login_response.url == "https://student.amizone.net/Home" else 500


def getTimeTable(day=""):
	if not ASPXAUTH:
		raise Exception('Login to Amizone first')
	def parseTimeTable(html):
		return ""
	headers = {
		"Cookie": "__RequestVerificationToken=" + COOKIE_requestVerificationToken + ';.ASPXAUTH=' + ASPXAUTH,
		"Host": "student.amizone.net",
		"Origin": "https://student.amizone.net",
		"Referer": "https://student.amizone.net/Home",
		"X-Requested-With": "XMLHttpRequest",
		"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
	}
	response = Session.get('https://student.amizone.net/TimeTable/Home?X-Requested-With=XMLHttpRequest HTTP/1.1', headers=headers)
	return parseTimeTable(response.text)


if __name__ == "__main__":
	print("Unofficial Amizone.net Application Programming Interface")
	print("Version:", __version__)
