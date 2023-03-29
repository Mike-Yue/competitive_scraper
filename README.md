# wingman-data-scraper
A python program to convert an HTML file of CS:GO Wingman match history to a CSV file.

To use this program:

1. Download your wingman/comp html file from [here](https://steamcommunity.com/my/gcpd/730?tab=matchhistorywingman). I reccomend using [this](https://www.reddit.com/r/GlobalOffensive/comments/8lyzb6/so_the_steam_client_has_been_keeping_track_of/dzkasyk/) JavaScript to scroll to the bottom for you. When all data is loaded, use [this](https://chrome.google.com/webstore/detail/save-page-we/dhhpefjklgkmgeafimnjhojgjamoafof) chrome extension to download the page.

2. Place the html file in the same directory as this program.

3. Run the command $python wingman.py "{steam_username}" "{html_file_name}". Note: quotes are neccesary.

4. A file 'wingman.csv' will be created in your current directory.
