# MapTheInternet
Visualizing the internet through website domains and popularity. While the list of websites is continiously updating to discover new websites and update popularity of existing ones, the visualization currently is provided using the top ~100K websites and the data (data/domains.csv) contains ~1 Million websites.

## About
Generating map of the internet by web crawling and extracting outgoing and internal links from pages. To increase efficiency while crawling, I used MySQL with multiprocessing as MySQL can handle mutiple conncetions at a time from different process. 

It is possible (and better) to use conncetion pools instead of one connection for multiple process. Scaling the program, connections pools should be used instead of opening and closing a connection.


<strong>The data is a continiously growing.</strong> Currently only ~1 Million websites have been discovered. In addition, some popular websites like reddit and Netflix are yet to be fully discovered. As such, addtional crawling and adjusting methods to extract data from more pages can increase the data size and accuracy.


## Visualization
Visualization are made on Tableau. The data, along with the .twb file is found in the 'data' folder, have fun!.

You can see my interactive versions in Table Public <a href="https://public.tableau.com/app/profile/naol.basaye/viz/Mapoftheinternet-2/TheInternet">here</a> and <a href="https://public.tableau.com/app/profile/naol.basaye/viz/Mapoftheinternet-3/SuffixDomains">here</a>

The non-interactive versions are given here 
![The Internet by Domain](data/images/The%20Internet%20By%20Domain.png)
This image shows the visualization of the top ~100K websites. The size indicates the number of incoming links (the number of times other website pages linked to this domain). The color indicates the suffix of the website (google.com has a suffix of com, wekepedia.org has org). The rank of a website is determined by the total number of links leading to that website. Look for more information in the comments and docstrings of the scripts.
&nbsp;
&nbsp;

![The Internet by #Incoming Links (Ascending)](data/images/The%20Internet%20By%20Incoming%20Links%20Ascending.png)
This image shows the visualization of the top ~100K websites. The size and color indicates the number of incoming links (the number of times other website pages linked to this domain). This is arranged for ascending incoming links for Tableau visualization.
&nbsp;
&nbsp;

![The Internet by #Incoming Links (Descending)](data/images/The%20Internet%20By%20Incoming%20Links%20Descending.png)
This image shows the visualization of the top ~100K websites. The size and color indicates the number of incoming links (the number of times other website pages linked to this domain). This is arranged in descending incoming links for Tableau visualization.
&nbsp;
&nbsp;

![The Internet by #Internal Links (Descending)](data/images/The%20Internet%20By%20Internal%20Links%20Descending.png)
This image shows the visualization of the top ~100K websites. The size and color indicates the number of internal links (the number of times a page in this domain linked to another page in the same domain). This is arranged in ascending incoming links for Tableau visualization.
&nbsp;
&nbsp;

![Suffix (Domain) Distribution by Sum #Incoming Links](data/images/Suffix%20(Top%20Level%20Domain)%20Distribution%20By%20Sum%20Incoming%20Links.png)
This images shows the visualization of suffix (top level domains) for the top ~100K websites. The size indicates the total number of incoming links (the number of times website pages linked to different domains with this suffix). This is arranged in descending order for Tableau visualization.
&nbsp;
&nbsp;


![Suffix (Domain) Distribution by Sum #Incoming Links](data/images/Suffix%20(Top%20Level%20Domian)%20Distribution%20By%20Average%20Incoming%20Link.png)
This images shows the visualization of suffix (top level domains) for the top ~100K websites. The size indicates the average number of incoming links (the number of times website pages linked to different domains with this suffix).
&nbsp;
&nbsp;

This is a personal project, me  making time for stuff that interests me and have fun on the way :). If you want to join, let me know and I'll make it so we can work on the same db and create sth cool.