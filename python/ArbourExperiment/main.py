import requests
import json
import datetime as dt
from bs4 import BeautifulSoup
import re
from flask import Flask, abort, request

app = Flask(__name__)

periods = {
        "08:50": 0,
        "09:00": 1,
        "10:00": 2,
        "11:20": 3,
        "12:20": 4,
        "13:20": 5,
        "13:45": 6,
        "14:45": 7
}

def refresh_cookie():
    json_data = {"items":[{"username":"20edunn@thelangton.org.uk","password":"'+MmkLRbi?qE2L>"}]}

    auth = requests.post("https://simon-langton-grammar-school-for-boys.uk.arbor.sc/auth/login?lang=en", json=json_data)


    login_info = auth.json()
    """{'items': [{'username':  'email':, 'display_name':, 'language': ,    'session_id': , 'loginIssues': [], 'firstTimeLogin': , 'message':  'Authentication Passed', 'logged_in': True}], 'success': True,   'action_params': [], 'notifications': []}"""

    print(login_info)
    cookies = {
        'mis': login_info["items"][0]["session_id"]
    }
    
    with open("cookies.json", "w") as f:
        f.write(json.dumps(cookies))

def update_data():
    refresh_cookie()
    
    with open("cookies.json", "r") as f:
        cookies = json.load(f)
    
    now = dt.datetime.now()
    json_data = {
        'action_params': {
            'view': 'day',
            'startDate': str(now.strftime("%Y-%m-%d")),
            'endDate': str(now.strftime("%Y-%m-%d")),
            'filters': [
                {
                    'field_name': 'object',
                    'value': {
                        '_objectTypeId': 1,
                        '_objectId': 5586,
                    },
                },
            ],
        },
    }


    calendar = requests.post(
        'https://simon-langton-grammar-school-for-boys.uk.arbor.sc/calendar-entry/list-static/format/json/',
        cookies=cookies,
        json=json_data,
    )

    main_page = requests.get(
        'https://simon-langton-grammar-school-for-boys.uk.arbor.sc/students/home-ui/dashboard',
        cookies=cookies
    )


    week: list = calendar.json()["items"][0]["fields"]["response"]["value"] ["pages"]
    day_json = next((item for item in week if item["start"] == str(now.strftime ("%Y-%m-%d"))), None)
    if day_json is None:
        exit()

    day_html = BeautifulSoup(day_json["html"], 'html.parser')
    lessons = day_html.find_all('b',  class_="title")
    lessons = [lesson.string for lesson in lessons]
    print(lessons)

    location_and_times = day_html.find_all('span',  string=re.compile   ("Location"))
    location_and_times = [location.string for location in location_and_times]
    print(location_and_times)

    
    name_url = {}
    courses = main_page.json()["content"][1]["content"][2]["content"]
    for course in courses:
        name = BeautifulSoup(course["props"]["value"], 'html.parser')
        name_url[name.string] = course["props"]["url"]
    print(name_url)
    
    lessons_json = {
    }
    pattern = re.compile(r"(\d\d:\d\d) - (\d\d:\d\d) \| Location: (.+)")
    for i in range(len(location_and_times)):
        x: re.Match = re.fullmatch(pattern, location_and_times[i])
        start_time, end_time, room = x.groups()
        
        
        lessons_json[periods[start_time]] = { 
            "name": lessons[i],
            "start_time": start_time,
            "end_time": end_time,
            "room": room,
            "url": name_url[lessons[i]]
        }



    print(lessons_json)
    with open("todays_lessons.json", "w") as f:
        f.write(json.dumps(lessons_json))

def get_next_lesson(period:int | str | None=None):
    try:
        with open("todays_lessons.json", "r") as f:
            lessons: dict[int, dict[str,str]] = json.load(f)
    except FileNotFoundError:
        update_data()
        with open("todays_lessons.json", "r") as f:
            lessons: dict[int, dict[str,str]] = json.load(f)
    
    if period is None:
        
        #now = dt.datetime.now().time()
        now = dt.time(hour=13)
        for lesson, data in lessons.items():
            start_time = data["start_time"].split(":")
            start_time = dt.time(hour=int(start_time[0]), minute=int(start_time[1]))

            end_time = data["end_time"].split(":")
            end_time = dt.time(hour=int(end_time[0]), minute=int(end_time[1]))
            
            if start_time <= now and now <= end_time:
                print(start_time, now, end_time)
                period = str(lesson)
                name = data["name"]
                break
    else:
        period = str(period)
        name = lessons[period]["name"]
           
    
    
    
    url = "https://simon-langton-grammar-school-for-boys.uk.arbor.sc" + lessons[period]["url"]
    
    with open("cookies.json", "r") as f:
        cookies = json.load(f)
        
    try:
        course_page = requests.get(
                url,
                cookies=cookies
        )
    except:
        refresh_cookie()
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
        course_page = requests.get(
                        url,
                        cookies=cookies
                )

    course_page = course_page.json()
    lesson_raw = course_page["content"][1]["content"][0]["content"][1]["content"]

    
    
    lesson_html = BeautifulSoup(lesson_raw, 'html.parser')
    date = str(lesson_html.contents[1].string)# pyright: ignore[reportAttributeAccessIssue]

    day = dt.datetime.strptime(date, "%a, %d %b %Y")

    x: re.Match = re.fullmatch(r"(\d\d:\d\d) - (\d\d:\d\d)", lesson_html.contents[0].string) # pyright: ignore[reportAttributeAccessIssue]
    start_time, end_time= x.groups()
    
 
    room = lesson_html.contents[2].string.split(":")[1].strip()# pyright: ignore[reportAttributeAccessIssue]
    lesson = {
        "name": name,
        "start_time": start_time,
        "end_time": end_time,
        "room": room,
        "teacher": lesson_html.contents[3].string # pyright: ignore[reportAttributeAccessIssue]
    }
    return lesson

get_next_lesson(7)
@app.route("/refresh",  methods=["POST"])
def refresh():
    try:
        update_data()
        return "Success"
    except Exception as e:
        return str(e), 500

@app.route("/next_lesson", methods=["POST"])
def next_lesson():
    try:
        if request.get_json() and "period" in request.get_json():
            return get_next_lesson(request.get_json()["period"])
        return get_next_lesson()
    except Exception as e:
            return str(e), 500
  
    
        