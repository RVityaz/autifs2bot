#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from re import sub as re_sub, search as re_search
from lxml import html


Session = requests.Session()
COOKIE_requestVerificationToken = Session.get('https://student.amizone.net').cookies['__RequestVerificationToken']
ASPXAUTH = None
__version__ = "0.1 beta"


def login(amizone_id, password):
    global ASPXAUTH
    LoginVerificationToken = re_search(r'<form action="\/" class=" validate-form" id="loginform" method="post" name="loginform"><input name="__RequestVerificationToken".{0,20}value=".{0,110}\/>', Session.get('https://student.amizone.net').text)[0][148:-4]
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
    def parseTimeTable(day, html_text):
        days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        if day and day.capitalize() not in days_of_the_week:
            raise Exception('"day" argument should be in range of Monday-Friday')
        day = day.capitalize()
        tree = html.fromstring(html_text)
        days_to_parse = days_of_the_week if day == "" else [day]
        res = ""
        for day in days_to_parse:
            res += (day.upper() + ' time table'.title()).strip() + "\n\n"
            div = tree.xpath('//div[@id="' + day + '"]')[0]
            time_table_boxes = div.xpath('//div[contains(@class, "timetable-box")]')
            course_names = {
                "IFP103": "Basic Numeracy Skills",
                "IFP105": "ICT Skills",
                "IFP106": "Intensive English",
                "IFP107": "ARRW",
            }
            for i in range(len(time_table_boxes)):
                res += time_table_boxes[i].xpath('//p[contains(@class, "class-time")]')[i].text.replace(' ', '').replace('to', ' - ') + '\n'
                course_code = time_table_boxes[i].xpath('//p[contains(@class, "course-code")]')[i].text
                res += course_names[course_code] + ' - ' + course_code + '\n'
                res += re_sub(r'\[[^[]*\]', '', time_table_boxes[i].xpath('//p[contains(@class, "course-teacher")]')[i].text) + '\n'
                res += '_'*20 + "\n"*3
        return res


    headers = {
        "Cookie": "__RequestVerificationToken=" + COOKIE_requestVerificationToken + ';.ASPXAUTH=' + ASPXAUTH,
        "Host": "student.amizone.net",
        "Origin": "https://student.amizone.net",
        "Referer": "https://student.amizone.net/Home",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
    }
    response = Session.get('https://student.amizone.net/TimeTable/Home?X-Requested-With=XMLHttpRequest HTTP/1.1', headers=headers)
    return parseTimeTable(day, response.text)


if __name__ == "__main__":
    print("Unofficial Amizone.net Application Programming Interface")
    print("Version:", __version__)
