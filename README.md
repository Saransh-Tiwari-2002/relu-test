This repository aims to scrape amazon for product info on the basis of asin and country codes. main.py is the driver file wherein main() is the driver function which gets called from 20 concurrent threads at once. We're using multithreading to speed up the process here. 
The time taken to scrape through 1000 links is around 350 seconds in general.
The number of threads can be increased or decreased depending on the hardware you're working with.
The information regarding the products post a successful scraping attempt are stored in 20 different files for these 20 threads and then compiled into a single file, new.json
After creating a master file containing the information regarding all the products, we dump the info regarding each product into the table 'products' of the sql server mydb-relu.
