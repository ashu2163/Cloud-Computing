import pyodbc
import os


server = 'ashuapp.database.windows.net'
database = 'ashudb'
username = 'Ashu2163'
password = 'Abcd1234'
driver= '{ODBC Driver 17 for SQL Server}'
dbConnect = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)