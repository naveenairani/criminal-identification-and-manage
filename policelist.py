import pymysql

def fetchPoliceList():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='@Naveen69',  # Replace 'your_password' with your actual password
                                 database='criminaldb',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Check if the police_list table exists
            cursor.execute("SHOW TABLES LIKE 'police_list'")
            result = cursor.fetchone()
            if not result:
                # Create the police_list table if it does not exist
                cursor.execute("""
                    CREATE TABLE police_list (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        badge_number VARCHAR(20),
                        contact_information VARCHAR(255),
                        `rank` VARCHAR(50),
                        department VARCHAR(100),
                        hire_date DATE,
                        shift VARCHAR(50),
                        salary DECIMAL(10, 2),
                        designation VARCHAR(255)
                    )
                """)
                connection.commit()  # Commit the transaction

            # Execute the SQL query to fetch the list of police
            sql = "SELECT * FROM police_list"
            cursor.execute(sql)
            # Fetch all rows of the result
            police_list = cursor.fetchall()
    finally:
        # Close the database connection
        connection.close()

    return police_list


# Test the function
if __name__ == "__main__":
    result = fetchPoliceList()
    print(result)
