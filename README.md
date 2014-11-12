websta-crawler
==============

Crawls a geographical location for Instagram pictures using an URL pointing to websta, extracts all Instagram image URLs and saves them in a text file for downloading with wget

Example
-------

I was interested in all Instagram pictures taken at Huayu Resort And Spa Sanya Hainan because of my distrust of fancy hotel advertisement material. websta, an (unofficial) Instagram frontend, lists all Instagram pictures taken at this location under the following URL:

http://websta.me/location/7428634

Unfortunately, the results are paged and each page contains loads of ads. Last, but not least I wasn't keen on manually clicking through all pages and saving all images of this location. That's why I wrote this script.

Once you provide a websta URL of a location to my script, it fetches the base page and all subsequent pages and extracts all links to the embedded Instagram pictures. The links are stored in ``./cache/%LocationID%/urls.txt``.

The script caches all pages in case you need to adjust the script and parse the HTML pages again. You can prevent the script from using the cache by either deleting the directory cache/* or by setting the variable ``useCache`` to ``False``.

You then can go ahead and download the Instagram photos using your local wget installation:

    wget -i urls.txt