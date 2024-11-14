import mysql.connector
import argon2
import os

with open("PEPPER.txt", 'r') as file:
    PEPPER = file.read().strip()

def hash_password(password):
    try:
        salt = os.urandom(16)
        ph = argon2.PasswordHasher()
        hashed_password = ph.hash(password + PEPPER)
        return hashed_password
    except Exception as e:
        print(f"Error hashing password: {e}")
        return None

mysql_url = "mysql://root:cldWscwfzqrsQIsVFeEFSIvOPjwhWhfd@junction.proxy.rlwy.net:20548/railway"

try:
    db_config = mysql_url.split("://")[1].split("@")
    user_pass = db_config[0].split(":")
    host_port_db = db_config[1].split("/")
    host_port = host_port_db[0].split(":")  

    mydb = mysql.connector.connect(
        host=host_port[0],
        user=user_pass[0],
        password=user_pass[1],
        port=int(host_port[1]),
        database=host_port_db[1]
    )

    print("[✔] Database connection successful!")

    cursor = mydb.cursor(dictionary=True)
    print("[✔] Database cursor created")
    print("")
    
    ####################################################### Removing table and data #######################################################
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table["Tables_in_railway"]
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f"[✔] Successfully dropped {table_name}.")
        except Exception as e:
            print(f"[✗] Error dropping {table_name}: {e}")
    print("")
    ####################################################### End of Removing table and data #######################################################

    ####################################################### Creating table and data for admin #######################################################
    create_table_query = """
    CREATE TABLE admin (
        admin_ic VARCHAR(12) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        phone_number VARCHAR(20),
        address TEXT,
        date_of_joining DATE,
        gender ENUM('Male', 'Female'),
        password VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    print("[✔] Admin table created successfully!")

    hashed_password = [hash_password('root'), hash_password('Admin')]

    if hashed_password:

        data = [
            ('000000000000', 'ROOT ADMIN', 'realblank21@gmail.com', '01159568937', 'Redacted', '2024-11-14', 'Male', hashed_password[0]),
            ('900101145678', 'ZAINAB ISMAIL', 'zainab.ismail@gmail.com', '0123456789', '45 Jalan Tanjung, George Town, Penang', '2022-11-10', 'Female', hashed_password[1])
        ]

        insert_query = """
        INSERT INTO admin (admin_ic, name, email, phone_number, address, date_of_joining, gender, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(insert_query, data)

        mydb.commit()
        print("[✔] Record inserted successfully with hashed password!")
        print("")

    ####################################################### End of Creating table and data for admin #######################################################

    ####################################################### Creating table and data for warden #######################################################
    create_table_query = """
    CREATE TABLE warden (
        warden_ic VARCHAR(12) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        phone_number VARCHAR(20),
        address TEXT,
        date_of_joining DATE,
        gender ENUM('Male', 'Female'),
        password VARCHAR(255) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    print("[✔] Warden table created successfully!")

    hashed_password = [hash_password('Warden1'), hash_password('Warden2')]

    data = [
        ('880212123456', 'ADAM RAHMAN', 'adam.rahman@gmail.com', '0198765432', '56 Jalan Bayan Lepas, Penang', '2021-04-20', 'Male', hashed_password[0]),
        ('910305089876', 'SITI MARIAM', 'siti.mariam@gmail.com', '0172345678', '21 Jalan Perak, George Town, Penang', '2022-06-15', 'Female', hashed_password[1])
    ]

    insert_query = """
    INSERT INTO warden (warden_ic, name, email, phone_number, address, date_of_joining, gender, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    cursor.executemany(insert_query, data)
    
    mydb.commit()
    print("[✔] Warden records inserted successfully with hashed passwords!")
    print("")
    ####################################################### End of Creating table and data for warden #######################################################

    ####################################################### Creating table and data for student #######################################################
    create_table_query = """
    CREATE TABLE student (
        student_ic VARCHAR(12) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        form_class VARCHAR(20),
        race VARCHAR(50),
        gender ENUM('Male', 'Female'),
        citizenship VARCHAR(40),
        family_members INT,
        address TEXT,
        home_distance INT,
        guardian_status ENUM('Father', 'Mother', 'Others'),
        guardian_contact VARCHAR(20),
        outing_ban_period DATE DEFAULT NULL
    );
    """
    cursor.execute(create_table_query)
    print("[✔] Student table created successfully!")

    data = [
        ('010101123456', 'AMIRUL ZULKIFLI', 'amirul@gmail.com', '4A', 'Malay', 'Male', 'Malaysian', 4, '123 Jalan Merdeka, Penang', '15', 'Father', '0123456789', None),
        ('020202225678', 'AISYAH BINTI ZAIN', 'aisyah@gmail.com', '3B', 'Malay', 'Female', 'Malaysian', 4, '45 Taman Impian, Bukit Mertajam, Penang', '20', 'Mother', '0138765432', '2024-11-15'),
        ('030303337890', 'DANIEL LIM', 'daniel@gmail.com', '5C', 'Chinese', 'Male', 'Malaysian', 2, '78 Jalan Sungai, George Town, Penang', '10', 'Father', '0142345678', None),
        ('040404442345', 'NURUL HIDAYAH', 'hidayah@gmail.com', '2D', 'Malay', 'Female', 'Malaysian', 3, '56 Jalan Kampung, Bukit Jambul, Penang', '18', 'Mother', '0191234567', None),
        ('050505556789', 'KAMARUL AKMAL', 'akmal@gmail.com', '6E', 'Malay', 'Male', 'Malaysian', 6, '12 Taman Sejahtera, Penang', '12', 'Father', '0169876543', None)
    ]

    insert_query = """
    INSERT INTO student (student_ic, name, email, form_class, race, gender, citizenship, family_members, address, home_distance, guardian_status, guardian_contact, outing_ban_period)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    cursor.executemany(insert_query, data)

    mydb.commit()
    print("[✔] Students records inserted successfully!")
    print("")
    ####################################################### End of Creating table and data for student #######################################################
    
    ####################################################### Creating table and data for hostel_application #######################################################
    create_table_query = """
    CREATE TABLE hostel_application (
        student_ic VARCHAR(12) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        gender ENUM('Male', 'Female'),
        form_class VARCHAR(50) NOT NULL,
        race VARCHAR(50),
        citizenship VARCHAR(50),
        family_members INT,
        address TEXT,
        home_distance DECIMAL(10, 2),
        guardian_status ENUM('Father', 'Mother', 'Others'),
        guardian_contact VARCHAR(20),
        status ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending'
    );
    """

    cursor.execute(create_table_query)
    print("[✔] Hostel Application table created successfully!")

    data = [
        ('011205135678', 'ADAM TAN', 'adamtan@gmail.com', 'Male', '4C', 'Chinese', 'Malaysian', 4, 
        '45 Jalan Bukit, Penang', 20.00, 'Father', '0123344556', 'Pending'),
        
        ('021305227890', 'NURUL FARHANA', 'farhana@gmail.com', 'Female', '3B', 'Malay', 'Malaysian', 3, 
        '67 Taman Sejahtera, Bayan Lepas, Penang', 15.00, 'Mother', '0136677889', 'Pending'),
        
        ('031406322345', 'RAJESH KUMAR', 'kumar@gmail.com', 'Male', '5A', 'Indian', 'Malaysian', 5, 
        '123 Jalan Dato, George Town, Penang', 18.00, 'Father', '0162233445', 'Pending'),
        
        ('041507432198', 'CHONG MEI LING', 'meiling@gmail.com', 'Female', '2A', 'Chinese', 'Malaysian', 2, 
        '89 Lorong Melur, Butterworth, Penang', 14.00, 'Mother', '0178899001', 'Pending'),
        
        ('051608542187', 'ALI HASSAN', 'alihassan@gmail.com', 'Male', '5B', 'Malay', 'Malaysian', 5, 
        '22 Jalan Merdeka, Sungai Petani, Kedah', 18.00, 'Father', '0181122334', 'Pending'),
        
        ('061709652376', 'SITI AISHAH', 'sitiaishah@gmail.com', 'Female', '4D', 'Malay', 'Malaysian', 4, 
        '31 Jalan Tunku Abdul Rahman, Alor Setar, Kedah', 17.00, 'Mother', '0193344556', 'Pending'),
        
        ('071810762465', 'BALAKRISHNAN', 'bala@gmail.com', 'Male', '3C', 'Indian', 'Malaysian', 3, 
        '76 Jalan Hang Tuah, Ipoh, Perak', 16.00, 'Father', '0125566778', 'Pending'),
        
        ('081911872554', 'ANGELINA TAN', 'angelina@gmail.com', 'Female', '1B', 'Chinese', 'Malaysian', 1, 
        '34 Jalan Utama, Seberang Perai, Penang', 13.00, 'Mother', '0149988776', 'Pending'),
        
        ('091012982643', 'FAIZAL HAKIM', 'faizalhakim@gmail.com', 'Male', '2D', 'Malay', 'Malaysian', 2, 
        '11 Jalan Bukit Mertajam, Bukit Mertajam, Penang', 14.00, 'Father', '0112244668', 'Pending'),
        
        ('101113093732', 'TAN YI XUAN', 'yixuan@gmail.com', 'Female', '4A', 'Chinese', 'Malaysian', 4, 
        '98 Jalan Masjid, Sungai Petani, Kedah', 17.00, 'Mother', '0136677880', 'Pending')
    ]

    insert_query = """
    INSERT INTO hostel_application (
        student_ic, name, email, gender, form_class, race, citizenship, family_members, 
        address, home_distance, guardian_status, guardian_contact, status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Execute the insert query for all records
    cursor.executemany(insert_query, data)
    mydb.commit()
    print("[✔] Hostel Application records inserted successfully!")
    print("")
    ####################################################### End of Creating table and data for hostel_application #######################################################

    ####################################################### Creating table and data for confiscated_item #######################################################
    create_table_query = """
    CREATE TABLE confiscated_items (
        confiscated_item_id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(255) NOT NULL,
        student_ic VARCHAR(20) NOT NULL,
        item_description TEXT,
        confiscation_date DATE NOT NULL,
        confiscater_warden_ic VARCHAR(20) NOT NULL,
        item_status ENUM('Confiscated', 'Returned', 'Disposed') NOT NULL DEFAULT 'Confiscated',
        confiscation_reason TEXT,
        return_date DATE,
        notes TEXT,
        FOREIGN KEY (student_ic) REFERENCES student(student_ic)
    );
    """

    cursor.execute(create_table_query)
    print("[✔] Confiscated Item table created successfully!")

    data = [
    ('Smartphone', '020202225678', 'Black iPhone 12', '2024-08-15', 
     '880212123456', 'Confiscated', 'Usage during class', '2024-10-01', 'Item is still in good condition.'),
    
    ('Headphones', '030303337890', 'Wireless Bluetooth Headphones', '2024-09-05', 
     '880212123456', 'Confiscated', 'Used during study hour', '2024-11-10', 'Has charging cable included.'),
    
    ('Power Bank', '040404442345', '10,000mAh Portable Charger', '2024-07-30', 
     '910305089876', 'Confiscated', 'Unpermitted item in hostel', '2024-09-15', 'Slight damage to casing.')
    ]

    insert_query = """
    INSERT INTO confiscated_items (
        item_name, student_ic, item_description, confiscation_date, 
        confiscater_warden_ic, item_status, confiscation_reason, return_date, notes
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    cursor.executemany(insert_query, data)

    mydb.commit()
    print("[✔] Confiscated Item records inserted successfully!")
    print("")
    ####################################################### End of Creating table and data for confiscated_item #######################################################

except mysql.connector.Error as e:
    print(f"[✗] Error connecting to the database: {e}")
finally:
    if cursor:
        cursor.close()
    if mydb:
        mydb.close()
