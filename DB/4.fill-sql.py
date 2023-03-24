#!/usr/bin/python
import sqlite3
conn = sqlite3.connect("Cartoon_db.sqlite") #point where you want - this db was precreated over navicat
file1 = open('sorted_links.txt', 'r')
source = file1.readlines()
old_title = ""
counter = 0
main_id = 0

for lines in source:
        kim_link = lines.split("||")[0]
        main_title=lines.split("/")[4].replace('-',' ')
        episode_title_tosplit=lines.split("/")[5]
        episode_title = episode_title_tosplit.split("?")[0]
        e_id_tosplit = episode_title_tosplit.split("=")[1]
        e_id = e_id_tosplit.split("||")[0]
        actual_link = lines.split("||")[1]
        kim_url = lines.split("/")[4]
        new_title = main_title
        try:
           check_first = episode_title.split("-")[0]
           if check_first == "Season":
              season_nr = episode_title.split("-")[1]
              episode_nr = episode_title.split("-")[3]
              try:
                 episode_title = episode_title.split("-",4)[4]
              except:
                 episode_title = "{NO TITLE}"
              print("Season Nr is: " + season_nr + " - Episode Nr: " + episode_nr)
           elif check_first == "Episode":
              episode_nr = episode_title.split("-")[1]
              season_nr = "00"
              try:
                 episode_title = episode_title.split("-",2)[2]
              except:
                 episode_title = "{NO TITLE}"
              print("No Season - Episode Nr: " + episode_nr)
           else:
              episode_nr = "00"
              season_nr = "00"
        except:
           episode_nr = "00"
           season_nr = "00"
           print("NO Season Nr, NO Episode Number")

        if new_title == old_title:
           main_id = counter
        else:
           old_title = new_title
           counter = counter+1
           main_id = counter
           conn.execute("INSERT INTO Main_Cartoons (id,main_title,kim_url) VALUES (" + str(main_id) + ",'" + str(old_title) + "','https://kimcartoon.li/Cartoon/" + str(kim_url) + "')")
        #print(counter)
        bepisode_title = episode_title.replace("-"," ")
        print(e_id + " -- " + main_title + "  :  " + bepisode_title + "   -----   " + actual_link)
        conn.execute("INSERT INTO Episodes (id,main_id,season,episode,title,kim_link,vid_link) VALUES (" + e_id + "," + str(main_id) + ",'" + season_nr + "','" + episode_nr + "','" + str(bepisode_title) + "','" + str(kim_link) + "','" + str(actual_link) + "')")
        conn.commit()

print("Records created successfully")
conn.close()
