from flask import Flask, request
import pandas as pd 
import sqlite3

app = Flask(__name__)

#--mendapatkan keseluruhan data employees
@app.route('/employee', methods=['GET'])
def get_emp():
    db_conn = sqlite3.connect("data_input/chinook.db")
    dt_emp = pd.read_sql_query(
        '''
        SELECT  
            (FirstName||' '||LastName) AS FullName,
            Title, 
            ReportsTo, 
            BirthDate,  
            HireDate, 
            Address, 
            City, 
            State, 
            Phone, 
             Email 
        FROM 
            employees
        ''', db_conn)
    return(dt_emp.to_json())

#--mendapatkan total sales atas suatu type media di beberapa negara
@app.route('/media/<md_id>', methods=['GET'])
def get_track(md_id):
    db_conn = sqlite3.connect("data_input/chinook.db")
    dt_md_sales = pd.read_sql_query(
                    '''
                    SELECT 
                        invs.BillingCountry AS Country, 
                        genr.Name AS Genre,     
                        med_typ.Name, 
                        SUM(invs.Total) AS Total 
                    FROM 
                        invoices AS invs, 
                        invoice_items AS invs_itm, 
                        tracks AS trks, 
                        genres AS genr, 
                        media_types AS med_typ 
                    WHERE   invs.InvoiceId = invs_itm.InvoiceId 
                        AND invs_itm.TrackId = trks.TrackId 
                        AND trks.GenreId = genr.GenreId 
                        AND trks.MediaTypeId = med_typ.MediaTypeId 
                        AND med_typ.MediaTypeId = %d 
                    GROUP BY Genre 
                    ORDER BY Total
                    '''
                    %int(md_id), db_conn)
    dt_md_sales['Genre'] = dt_md_sales['Genre'].astype('category', errors='raise')                                 
    return(dt_md_sales.to_json())

#--mendapatkan total sales dari suatu negara
@app.route('/country/<country_nm>', methods=['GET'])
def get_genre(country_nm):
    db_conn = sqlite3.connect("data_input/chinook.db")
    dt_country_sales = pd.read_sql_query(
                    '''
                     SELECT invs.BillingCountry AS Country, 
                            genr.Name AS Genre, 
                            med_typ.Name AS Media_Nm, 
                            sum(invs.Total) AS Total
                     FROM   invoices AS invs, 
                            invoice_items AS invs_itm, 
                            tracks AS trks, 
                            genres AS genr, 
                            media_types AS med_typ 
                    WHERE   invs.InvoiceId = invs_itm.InvoiceId 
                        AND invs_itm.TrackId = trks.TrackId 
                        AND trks.GenreId = genr.GenreId 
                        AND trks.MediaTypeId = med_typ.MediaTypeId 
                        AND invs.BillingCountry = ?
                    GROUP BY Genre 
                    ORDER BY Total DESC
                    '''
                    , db_conn, params=(country_nm,))

    dt_country_sales['Media_Nm'] = dt_country_sales['Media_Nm'].astype('category', errors='raise')
    return(dt_country_sales.to_json())   

#--mendapatkan total penjualan album
@app.route('/albums', methods=['GET'])
def get_album():
    db_conn = sqlite3.connect("data_input/chinook.db")
    dt_album = pd.read_sql_query(
                    '''
                        SELECT 
                            albm.Title AS Album, 
                            art.Name AS Artist, 
                            sum(invs.Total) AS TotalSales
                        FROM invoices AS invs, 
                            invoice_items AS inv_itm, 
                            tracks AS trk, 
                            albums AS albm, 
                            artists AS art 
                        WHERE    invs.InvoiceId = inv_itm.InvoiceId 
                            AND inv_itm.TrackId = trk.TrackId 
                            AND trk.AlbumId = albm.AlbumId 
                            AND albm.ArtistId = art.ArtistId 
                        GROUP BY albm.Title
                        ORDER BY TotalSales DESC
                   '''
                   , db_conn)
    return(dt_album.to_json())

#--mendapatkan total sales per-employee
@app.route('/sales', methods=['GET'])
def get_sale():
    db_conn = sqlite3.connect("data_input/chinook.db")
    emp_sales = pd.read_sql_query(
                '''
                    SELECT 
                        (empl.FirstName||' '||empl.LastName) AS FullName, 
                        sum(invs.Total) AS TotalSales,
                        invs.InvoiceDate AS Period 
                    FROM employees AS empl, 
                         customers AS cust, 
                         invoices AS invs 
                    WHERE 
                            empl.EmployeeId = cust.SupportRepId 
                        AND cust.CustomerId = invs.CustomerId 
                        AND empl.Title = 'Sales Support Agent' 
                    GROUP BY FullName, invs.InvoiceDate
                    '''
                    , db_conn, parse_dates='Period')

    emp_sales['Period'] = pd.to_datetime(emp_sales['Period']).dt.to_period('M')
    dt_sales = pd.crosstab(index=emp_sales['Period'],
                           columns=emp_sales['FullName'],
                           values=emp_sales['TotalSales'],
                           aggfunc = 'sum').fillna(0)
    return(dt_sales.to_json())

#--mendapatkan total sales per-employee untuk setiap negara
@app.route('/empsales', methods=['GET'])
def get_empsales():
    db_conn = sqlite3.connect("data_input/chinook.db")
    emp_sales_count = pd.read_sql_query(
        '''
         SELECT 
            (empl.FirstName||' '||empl.LastName) AS FullName, 
            sum(invs.Total) AS TotalSales, 
            invs.BillingCountry AS Country 
        FROM 
            employees AS empl, 
            customers AS cust, 
            invoices AS invs 
        WHERE 
                empl.EmployeeId = +cust.SupportRepId 
            AND cust.CustomerId = +invs.CustomerId 
            AND empl.Title = 'Sales Support Agent' 
        GROUP BY BillingCountry 
        ORDER BY FullName, TotalSales
        '''
        , db_conn)

    dt_sales_count = emp_sales_count.fillna(0).stack()                               
    return(dt_sales_count.to_json())

if __name__ == '__main__':
     app.run(debug=True, port=5000)


