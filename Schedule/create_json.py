#!/usr/bin/env python3
import json
import sqlite3
from sqlite3 import Error

import ffmpeg
import requests


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def select_all_tasks(conn):
    cur = conn.cursor()
    cur.execute("SELECT token FROM Schedule")
    rows = cur.fetchall()
    x = 0
    for row in rows:
        token = str(row[0])
        print(token)
    quality = '720p'
    sleep(5)
    response = requests.post(
        'https://www.luxubu.review/api/source/' + token, {}).json()
    link = [k for k in response['data'] if quality in k['label']]
    if len(link) == 0:
        print("WARN : Could not get %s version of " % (quality))
        link = response['data'][-1]
    else:
        link = link[0]
    quality = link['label']
    link_url = link['file']
    page = requests.head(link_url, allow_redirects=True)
    page.headers.get(link_url)
    follow_link = page.url
    print(follow_link)
    vid = ffmpeg.probe(follow_link)
    ffmpeg_duration = vid['streams'][0]['duration']
    print(ffmpeg_duration)
    programs = {"in": 0.0, "out": float(ffmpeg_duration), "duration": float(ffmpeg_duration), "source": follow_link}
    if x == 0:
        programs = {"in": 0.0, "out": float(ffmpeg_duration), "duration": float(ffmpeg_duration), "source": follow_link}
        main_dict = {"channel": "Channel 1","date": "2022-12-22", "program": [programs]}
        x += 1
    else:
        main_dict["program"].append(programs)
json_object = json.dumps(main_dict, indent=4)
print(json_object)
with open("sample.json", "w") as outfile:
    outfile.write(json_object)


def main():
    database = r"../Cartoon_db.sqlite"
    conn = create_connection(database)
    with conn:
        select_all_tasks(conn)


if __name__ == '__main__':
    main()
