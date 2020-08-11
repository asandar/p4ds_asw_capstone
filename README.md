# p4ds_asw_capstone
P4DS Capstone Project
This is Algoritma's Python for Data Analysis Capstone Project. This project aims to create a simple API to fetch data from 'chinook.db'.

we demand data to be accessible. And we create an API for anyone who are granted access to the data for collect them and get the information from data. In this capstone project, we create Flask Application as an API and deploy it to Heroku Web Hosting.

Dependencies :
--------------

-   Pandas (pip install pandas)

-   Flask (pip install flask)

-   Gunicorn (pip install gunicorn)

Goal
----

-   Create Flask API App

-   Implements data wrangling

-   Build API Documentation

-   Deploy to Heroku

We have deployed a simple example on : https://app-asw.herokuapp.com/ Here's the list of its endpoints:

1.  /employee, method = GET Static Endpoint, returning all data of employee.

2.  /media/, method = GET Dynamic Endpoint, returning total sales from country base on media type. input md_id with one of the MediaTypeId as below :

-   1 (MPEG audio file)

-   2 (Protected AAC audio file)

-   3 (Protected MPEG-4 video file)

-   4 (Purchased AAC audio file)

-   5 (AAC audio file)

3.  /country/, method = GET Dynamic Endpoint, returning total sales base on country. input country_nm with the country name

4.  /albums, method = GET Static Endpoint, returning total sales and mean of album.

5. /empsales, method = GET Static Endpoint, returning total sales of Sales Support in every country.

6. /sales, method = GET Static Endpoint, returning total sales of Sales Support Agent per-month period
 

If you want to try it, you can access (copy-paste the link as below) :
- https://app-asw.herokuapp.com/employee
- https://app-asw.herokuapp.com/media/1
- https://app-asw.herokuapp.com/country/USA
- https://app-asw.herokuapp.com//albums
- https://app-asw.herokuapp.com/empsales
- https://app-asw.herokuapp.com/sales
