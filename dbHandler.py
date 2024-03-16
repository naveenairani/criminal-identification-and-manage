import pymysql


def insertData(data):
    rowId = 0

    db = pymysql.connect(
        host="localhost",
        user="root",
        password="@Naveen69",
        database="criminaldb"

    )

    # db = pymysql.connect("localhost", "criminaluser", "", "criminaldb")
    cursor = db.cursor()
    print("database connected")

    query = "INSERT INTO criminaldata VALUES(0, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % \
            (data["Name"], data["Father's Name"], data["Mother's Name"], data["Gender"],
             data["DOB(yyyy-mm-dd)"], data["Blood Group"], data["Identification Mark"],
             data["Nationality"], data["Religion"], data["Crimes Done"])

    try:
        cursor.execute(query)
        db.commit()
        rowId = cursor.lastrowid
        print("data stored on row %d" % rowId)
    except:
        db.rollback()
        print("Data insertion failed")

    print(rowId)
    db.close()
    print("connection closed")
    return rowId


def retrieveData(name):
    id = None
    crim_data = None

    db = pymysql.connect(
        host="localhost",
        user="root",
        password="@Naveen69",
        database="criminaldb"

    )
    cursor = db.cursor()
    print("database connected")

    query = "SELECT * FROM criminaldata WHERE name='%s'" % name

    try:
        cursor.execute(query)
        result = cursor.fetchone()

        id = result[0]
        crim_data = {
            "Name": result[1],
            "Father's Name": result[2],
            "Mother's Name": result[3],
            "Gender": result[4],
            "DOB(yyyy-mm-dd)": result[5],
            "Blood Group": result[6],
            "Identification Mark": result[7],
            "Nationality": result[8],
            "Religion": result[9],
            "Crimes Done": result[10]
        }

        print("data retrieved")
    except:
        print("Error: Unable to fetch data")
        print(id)
    db.close()
    print("connection closed")

    return (id, crim_data)

def deleteData(id):
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="@Naveen69",
        database="criminaldb"
    )

    cursor = db.cursor()
    print("Database connected")

    try:
        # Use parameterized query to prevent SQL injection
        query = "DELETE FROM criminaldata WHERE id=%s"
        cursor.execute(query, (id,))
        db.commit()
        print("Data with ID %d deleted successfully." % id)
        db.close()  # Close database connection before returning
        print("Connection closed")
        return True  # Return True indicating successful deletion
    except Exception as e:
        db.rollback()
        print("Error: Unable to delete data")
        print("Exception:", e)
        db.close()  # Close database connection before returning
        print("Connection closed")
        return False  # Return False indicating deletion failure


def updateData(id, new_data):
    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="@Naveen69",
            database="criminaldb"
        )

        cursor = db.cursor()
        print("Database connected")

        query = """
            UPDATE criminaldata
            SET name=%s, father_name=%s, mother_name=%s, gender=%s, dob=%s,
                blood_group=%s, identification_mark=%s, nationality=%s, religion=%s, crimes_done=%s
            WHERE id=%s
        """

        # Check if 'DOB' key exists in new_data dictionary
        if 'DOB' in new_data:
            # Check if dob is empty string, if so, set it to NULL
            if new_data['DOB'] == "":
                new_data['DOB'] = None

        # Check if 'Crimes Done' key exists in new_data dictionary
        if 'Crimes Done' in new_data:
            # Check if 'Crimes Done' is empty string, if so, set it to NULL
            if new_data["Crimes Done"] == "":
                new_data["Crimes Done"] = None

        cursor.execute(query, (
            new_data["Name"], new_data["Father's Name"], new_data["Mother's Name"],
            new_data["Gender"], new_data["DOB"], new_data["Blood Group"],
            new_data["Identification Mark"], new_data["Nationality"], new_data["Religion"],
            new_data["Crimes Done"], id
        ))

        db.commit()
        print("Data with ID %s updated successfully." % str(id))
    except pymysql.Error as e:
        db.rollback()
        print("Error: Unable to update data:", e)
    finally:
        if db:
            db.close()
            print("Connection closed")

import pymysql

def create_criminaldata_table():
    try:
        # Connect to MySQL
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="@Naveen69",
            database="criminaldb"
        )
        cursor = db.cursor()
        print("Database connected")

        # SQL statement to create the criminaldata table
        create_table_query = """
            CREATE TABLE IF NOT EXISTS criminaldata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                father_name VARCHAR(255),
                mother_name VARCHAR(255),
                gender VARCHAR(10),
                dob DATE,
                blood_group VARCHAR(10),
                identification_mark VARCHAR(255),
                nationality VARCHAR(50),
                religion VARCHAR(50),
                crimes_done VARCHAR(255)
            )
        """
        cursor.execute(create_table_query)
        db.commit()
        print("Table 'criminaldata' created successfully.")

    except pymysql.Error as e:
        print("Error creating table:", e)

    finally:
        if db:
            db.close()
            print("Connection closed")

# Call the function to create the criminaldata table
create_criminaldata_table()



def modifyTableSchema():
    try:
        # Connect to MySQL
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="@Naveen69",
            database="criminaldb"
        )
        cursor = db.cursor()
        print("Database connected")

        # Alter table schema to change dob to DATE and crimes_done to VARCHAR(255)
        alter_query = """
            ALTER TABLE criminaldata 
            MODIFY COLUMN dob DATE,
            MODIFY COLUMN crimes_done VARCHAR(255);
        """
        cursor.execute(alter_query)
        db.commit()
        print("Table schema modified successfully.")
    except pymysql.Error as e:
        print("Error modifying table schema:", e)
    finally:
        if db:
            db.close()
            print("Connection closed")

# Call the function to modify the table schema
modifyTableSchema()





def displayAllNames():
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="@Naveen69",
        database="criminaldb"
    )

    cursor = db.cursor()
    print("Database connected")

    try:
        query = "SELECT name FROM criminaldata"
        cursor.execute(query)
        results = cursor.fetchall()
        print("List of names:")
        for result in results:
            print(result[0])
    except:
        print("Error: Unable to fetch names")

    db.close()
    print("Connection closed")

def fetchAllData():
    """
    Retrieve all criminal records from the database.
    Returns:
        list: A list of dictionaries, each containing the data for one criminal record.
    """
    criminal_records = []

    try:
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="@Naveen69",
            database="criminaldb"
        )

        cursor = db.cursor()
        cursor.execute("SELECT * FROM criminaldata")
        rows = cursor.fetchall()

        for row in rows:
            record = {
                "id": row[0],
                "name": row[1],
                "father_name": row[2],  # Update to match the SQL column name
                "mother_name": row[3],  # Update to match the SQL column name
                "gender": row[4],
                "dob": row[5],
                "blood_group": row[6],  # Update to match the SQL column name
                "identification_mark": row[7],  # Update to match the SQL column name
                "nationality": row[8],
                "religion": row[9],
                "crimes_done": row[10]
            }
            criminal_records.append(record)

    except Exception as e:
        print("Error: Unable to retrieve data from database:", e)

    finally:
        if db:
            db.close()
            print("Connection closed")

    return criminal_records
