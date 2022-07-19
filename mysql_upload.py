import mysql.connector
from json import load
from os.path import join, dirname

class tables:               #class containing all table related functions
    def create_tables(cursor):          
        cursor.execute('CREATE TABLE Products (Serial_Number int NOT NULL, Product_Title varchar(1000) NOT NULL, Product_Image_URL varchar(1000) NULL, Product_Price varchar(45) NOT NULL, PRIMARY  KEY (Serial_Number))')
        
    def update_table1(cursor, conn):
        insert_stmt ="INSERT INTO Products (Serial_Number, Product_Title, Product_Image_URL, Product_Price) VALUES (%s, %s, %s, %s)"     # Preparing SQL query to INSERT a record into the database.
        data_1 = load(open(join(dirname(__file__), 'new.json'), "r", encoding='utf-8')) #loading the required json file into a dictionary
        
        for serial_num in data_1:
            
            try:
                cursor.execute(insert_stmt, (int(serial_num)+1, data_1.get(serial_num).get('Title'), data_1.get(serial_num).get('Image URL'), data_1.get(serial_num).get('Price')))            # Executing the SQL command            
                conn.commit()               # Commit your changes in the database
                print("Data inserted")
            except:
                conn.rollback()             # Rolling back in case of error    
                    

    
def mysql_upload():
    #establishing the connection
    
    conn=mysql.connector.connect(user='Saransh', password='sqltesting_123', host='127.0.0.1', database='mydb_relu')

    cursor = conn.cursor()          #Creating a cursor object using the cursor() method
    
    tables.create_tables(cursor)    #Creating the required table
    tables.update_table1(cursor, conn)
    conn.close()        # Closing the connection  



