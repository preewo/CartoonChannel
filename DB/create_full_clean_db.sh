#!/bin/bash
python3 1.main.py
echo "  -  Done !"
python3 2.get_original_links.py
echo "  -  Done !"
python3 3.get_original_links+actual_links.py
echo "  -  Done !"
sort original_urls+actual_urls.txt | uniq > sorted_links.txt
python3 4.fill-sql.py
echo "  -  Done !"
python3 5.update_details.py
echo "  -  Done !"
python3 6.get_video_lenght.py
echo "Everything is done, ready to use the database!"
