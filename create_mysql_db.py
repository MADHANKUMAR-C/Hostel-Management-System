import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS hostel_management")
            print("Hostel Management database created successfully")
            
            # Close connection
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

if __name__ == "__main__":
    create_database()
