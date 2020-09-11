import sqlite3 as sql
from sqlite3 import Error


def createConnection(db_file_path):
    """ create a database connection to a SQLite database, If file doesn`t exists then, SQLite automatically creates the new database for you.
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        return sql.connect(db_file_path);
    except Error as e:  # Catch any error and print error message
        print(e)
        return conn


def createTable(connection):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    createTableSql = "CREATE TABLE IF NOT EXISTS data (product_code text,product_name text,product_price real,product_stock integer)"

    try:
        c = connection.cursor()
        c.execute(createTableSql)
        connection.commit()
    except Error as e:  # Catch any error and print error message
        print(e)
        return


def validateIDinDB(connection, id):
    """
    :param connection:
    :type connection:
    :param id:
    :type id:
    :return:
    :rtype:
    """
    # validating Product Id from Database

    checkIDSQL = "SELECT * FROM data WHERE product_code='" + id + "'"

    c = connection.cursor()
    try:
        c.execute(checkIDSQL)
    except Error as e:  # Catch any error and print error message
        print(e);
    rows = c.fetchone();
    if rows != None:
        return True
    else:
        return False


def validateID(id):
    """

    :rtype: object
    """
    # Validates whether Id is between given range
    try:
        if int(id) > 9999999999 or int(id) < 0:
            return False
        else:
            return True
    except:
        print("INVALID INPUT")
        return

def validateName(name):
    """

    :param name:
    :type name:
    :return:
    :rtype:
    """
    # Validates lenght of Product Name
    try:
        
        if len(name) <= 20:
            if name.replace(' ','').isalpha(): #name.isascii() & 
                return True
        return False
    except:
        print("NAME ERROR")

def validatePrice(price):
    """

    :param price:
    :type price:
    :return:
    :rtype:
    """
    # Validates Product Price
    try:
        if float(price) >= 0:
            return True
        else:
            return False
    except:
        return False


def validateStock(stock):
    """

    :param stock:
    :type stock:
    :return:
    :rtype:
    """
    # Vadiates Product Stock value
    try:
        if int(stock) >= 0:
            return True
        else:
            return False
    except:
        return False


def insertData(connection):
    """

    :param connection:
    :type connection:
    :return:
    :rtype:
    """
    # Inputting ID From User and Validating
    id = input("ENTER ITEM ID: ")
    if not (validateID(id)):
        print("Invalid ID")
        return
    id = id.rjust(10, '0')

    # Validate ID in Databsse
    if validateIDinDB(connection, id):
        print("ID ALREADY EXISTS...")
        return
    # Inputting Name from User and validating
    name = input("ENTER ITEM NAME: ")
    if not validateName(name):
        print("Invalid Name")
        return

    # Inputting Item Price and Validating
    price = input("ENTER ITEM PRICE: ")
    if not validatePrice(price):
        print("Invalid Price")
        return

    # Inputting Item Stock and Validating
    stock = input("ENTER ITEM STOCK: ")
    if not validateStock(stock):
        print("Invalid Stock")
        return

    # Inserting Data into Database
    try:
        insertSQL = "INSERT INTO data(product_code,product_name,product_price,product_stock) VALUES('" + id + "',?,?,?)"
        args = ([name, price, stock])
        c = connection.cursor()
        c.execute(insertSQL, args)
        connection.commit()
    except Error as e:  # Catch any error and print error message
        print(e)
        return


# def dis(data,cols,wide):
#     '''Prints formatted data on columns of given width.'''
#     n, r = divmod(len(data), cols)
#     pat = '{{:{}}}'.format(wide)
#     line = '\n'.join(pat * cols for _ in range(n))
#     last_line = pat * r
#     print(line.format(*data))
#     print(last_line.format(*data[n*cols:]))
def displaySpecificData(connection, id):
    """

    :param connection:
    :type connection:
    :param id:
    :type id:
    """
    # display Data
    selectSQL = "SELECT * FROM data WHERE product_code='" + id + "'"
    c = connection.cursor()
    c.execute(selectSQL)
    rows = c.fetchone()

    print('{:*^100}'.format(" * "))
    print('{:^100}'.format("  DATA IN DATAMANAGER "))
    print('{:*^100}'.format(" * "))
    print('{:-^100}'.format(" - "))
    printRow(["PRODUCT CODE", "PRODUCT NAME", "PRODUCT PRICE", "PRODUCT STOCK"])
    print('{:-^100}'.format(" - "))

    printRow(rows)
    print('{:*^100}'.format(" * "))
    print('{:*^100}'.format(" * "))


def printRow(rows):
    """

    :param rows:
    :type rows:
    """
    # pretty print the data in terminal
    line = 1
    for row in rows:
        if line == 4:
            print('{0:{width}{base}}'.format(str(row), base=1, width=2), end=' ')
            line = 1
            print()
        else:
            print('{0:{width}{base}}'.format(str(row), base=2, width=2), end=' ')
            line += 1


def displayAllData(connection):
    """

    :param connection:
    :type connection:
    """
    selectSQL = "SELECT * FROM data"
    c = connection.cursor()
    c.execute(selectSQL)
    rows = c.fetchall()
    print('{:*^100}'.format(" * "))
    print('{:^100}'.format(" ALL DATA IN DATAMANAGER "))
    print('{:*^100}'.format(" * "))
    print('{:-^100}'.format(" - "))
    printRow(["PRODUCT CODE", "PRODUCT NAME", "PRODUCT PRICE", "PRODUCT STOCK"])
    print('{:-^100}'.format(" - "))

    for row in rows:
        printRow(row)
    print('{:*^100}'.format(" * "))
    print('{:*^100}'.format(" * "))


def deleteData(connection, id):
    """

    :param connection:
    :type connection:
    :param id:
    :type id:
    """
    deleteSQL = "DELETE FROM data WHERE product_code='" + id + "'"

    c = connection.cursor()
    c.execute(deleteSQL)
    connection.commit()

    print()
    print("ID:" + str(id) + " DELETED SUCCESSFULLY...")


# def updateData(connection,id,name,price,stock):
#     updateSQL="UPDATE data SET product_name=?,product_price=?,product_stock=? WHERE product_code='"+id+"'"
#     args(str(name),str(price),str(stock),str(id))
#     c=connection.cursor()
#     c.execute(updateSQL,args)
#     connection.commit()

def help():
    """
    Print Help
    """
    print(
        "WELCOME TO DATAMANAGER: \n 1. INSERT ITEM: TO ADD ITEM IN DATAMANAGER \n 2. UPDATE ITEM: TO UPDATE EXISTING ITEMS \n 3. DELETE ITEM: DELETE ANY EXISTING ITEM \n 4. VIEW ALL: TO VIEW ALL PRODUCTS INFOMATION  \n 5. DISPLAY SINGLE: TO DISPLAY PRODUCT BASED ON ID \n 6. SEARCH BY PRODUCT NAME: SEARCH PRODUCT BY ITS MATCHING NAME \n 7. SEARCH BY ID: SEARCH PRODUCT BASED ON MATCHING ID \n 8. HELP: TO GET ASSISTANCE \n 9. EXIT: TO HAPPILY EXIT :)")


def updateName(connection, id, name):
    """

    :param connection:
    :type connection:
    :param id:
    :type id:
    :param name:
    :type name:
    :return:
    :rtype:
    """
    updateNameSQL = "UPDATE data SET product_name=? WHERE product_code='" + id + "'"
    args = ([name])
    try:
        c = connection.cursor()
        c.execute(updateNameSQL, args)
        connection.commit()
    except Error as e:  # Catch any error and print error message
        print(e)
        print("ERROR WHILE UPDATING... TRY AGAIN")
        return


def updatePrice(connection, id, price):
    """

    :param connection:
    :type connection:
    :param id:
    :type id:
    :param price:
    :type price:
    :return:
    :rtype:
    """
    updateNameSQL = "UPDATE data SET product_price=? WHERE product_code='" + id + "'"
    args = ([str(float(price))])
    try:
        c = connection.cursor()
        c.execute(updateNameSQL, args)
        connection.commit()
    except Error as e:  # Catch any error and print error message
        print(e)
        print("ERROR WHILE UPDATING... TRY AGAIN")
        return


def updateStock(connection, id, stock):
    """

    :param connection:
    :type connection:
    :param id:
    :type id:
    :param stock:
    :type stock:
    :return:
    :rtype:
    """
    updateNameSQL = "UPDATE data SET product_stock=? WHERE product_code='" + id + "'"
    args = ([str(int(stock))])
    try:
        c = connection.cursor()
        c.execute(updateNameSQL, args)
        connection.commit()
    except Error as e:  # Catch any error and print error message
        print(e)
        print("ERROR WHILE UPDATING... TRY AGAIN")
        return


def updateMenu(connection):
    """

    :param connection:
    :type connection:
    :return:
    :rtype:
    """
    # Update Menu
    choice = ["1. UPDATE PRODUCT NAME", "2. UPDATE PRODUCT PRICE", "3. UPDATE STOCK", "4. RETURN TO MAIN MENU"]
    print('{:*^100}'.format(" * "))
    print('{:*^100}'.format(" UPDATE STOCK OPTIONS "))
    print('{:*^100}'.format(" * "))
    printRow(choice)
    print('{:*^100}'.format(" * "))
    try:
        # Take user Input
        choice = int(input())

        # Show Menu to user
        if choice == 1:
            id = input("ENTER PRODUCT CODE: ")
            id = id.rjust(10, '0')

            if not validateID(id):
                print("INVALID ID")
                return
            if validateIDinDB(connection, id):
                name = input("ENTER UPDATED NAME: ")
                if not validateName(name):
                    print("INVALID NAME: ")
                    return
                updateName(connection, id, name)
                print('{:*^100}'.format(" UPDATED SUCCESSFULLY "))
            else:
                print('ID DOES NOT EXISTS')
                return
        elif choice == 2:
            id = input("ENTER PRODUCT CODE: ")
            id = id.rjust(10, '0')

            if not validateID(id):
                print("INVALID ID")
                return
            if validateIDinDB(connection, id):
                price = input("ENTER UPDATED PRICE: ")
                if not validatePrice(price):
                    print("INVALID PRICE")
                updatePrice(connection, id, price)
                print('{:*^100}'.format(" UPDATED SUCCESSFULLY "))
            else:
                print('ID DOES NOT EXISTS')
                return

        elif choice == 3:
            id = input("ENTER PRODUCT CODE: ")
            id = id.rjust(10, '0')

            if not validateID(id):
                print("INVALID ID")
                return
            if validateIDinDB(connection, id):
                stock = input("ENTER UPDATED STOCK: ")
                if not validateStock(stock):
                    print("INVALID STOCK")
                    return
                updateStock(connection, id, stock)
                print('{:*^100}'.format(" UPDATED SUCCESSFULLY "))
            else:
                print('ID DOES NOT EXISTS')
                return

        elif choice == 4:
            mainMenu()

    except:
        print('{:^100}'.format(" INVALID INPUT "))
        print("")
        updateMenu()


def searchByProductName(connection, name):
    """

    :param connection:
    :type connection:
    :param name:
    :type name:
    """
    searchByProductNameSQL = "SELECT * FROM data WHERE product_name LIKE '%" + name + "%'"
    c = connection.cursor()
    c.execute(searchByProductNameSQL)
    rows = c.fetchall()
    if rows == None:
        print('{:*^100}'.format(" NO DATA FOUND "))
    else:
        print('{:*^100}'.format(" * "))
        print('{:^100}'.format(" ALL DATA IN DATAMANAGER "))
        print('{:*^100}'.format(" * "))
        print('{:-^100}'.format(" - "))
        roww = ["PRODUCT CODE", "PRODUCT NAME", "PRODUCT PRICE", "PRODUCT STOCK"]
        rows.insert(0, roww)
        print('{:-^100}'.format(" - "))

        for row in rows:
            printRow(row)
        print('{:*^100}'.format(" * "))
        print('{:*^100}'.format(" * "))


def searchByID(connection, id):
    """

    :param connection:
    :type connection:
    :param id:
    :type id:
    """
    tempid = str(id)
    searchByProductIDSQL = "SELECT * FROM data WHERE product_code LIKE '%" + tempid + "%'"
    c = connection.cursor()
    c.execute(searchByProductIDSQL)
    rows = c.fetchall()
    if rows == None:
        print('{:*^100}'.format(" NO DATA FOUND "))
    else:
        print('{:*^100}'.format(" * "))
        print('{:^100}'.format(" ALL DATA IN DATAMANAGER "))
        print('{:*^100}'.format(" * "))
        print('{:-^100}'.format(" - "))
        roww = ["PRODUCT CODE", "PRODUCT NAME", "PRODUCT PRICE", "PRODUCT STOCK"]
        rows.insert(0, roww)
        print('{:-^100}'.format(" - "))

        for row in rows:
            printRow(row)
        print('{:*^100}'.format(" * "))
        print('{:*^100}'.format(" * "))


def mainMenu():
    """
    Print Main Menu
    :return:
    :rtype:
    """
    # MainMenu
    # os.system('cls')
    options = ["1. INSERT ITEM", "2. UPDATE ITEM", "3. DELETE ITEM", "4. VIEW ALL", "5. DISPLAY SINGLE",
               "6. SEARCH BY PRODUCT NAME", "7. SEARCH BY ID", "8. HELP", "9. EXIT"]
    print('{:*^100}'.format(" * "))
    print('{:*^100}'.format(" WELCOME TO DATAMANAGER"))
    print('{:*^100}'.format(" * "))
    rows = 1
    for option in options:
        if rows == 3:
            print('{0:{width}{base}}'.format(option, base=1, width=2), end=' ')
            rows = 1
            print()
        else:
            print('{0:{width}{base}}'.format(option, base=2, width=2), end=' ')
            rows += 1
    print()
    print('{:*^100}'.format(" * "))
    print('{:*^100}'.format(" * "))

    try:
        # Take User Input as Choice
        choice = int(input())
    except:
        print('{:^100}'.format(" INVALID INPUT "))
        mainMenu()
    try:
        # Select and perform operation based on user selected choice
        if choice == 1:
            insertData(conn);
        elif choice == 2:
            updateMenu(conn)
        elif choice == 3:
            id = input("ENTER PRODUCT CODE: ")
            id = id.rjust(10, '0')
            if not validateID(id):
                print("INVALID ID")
                return

            if validateIDinDB(conn, id):
                deleteData(conn, id)
        elif choice == 4:
            displayAllData(conn)
        elif choice == 5:
            id = input("ENTER PRODUCT CODE: ")
            id = id.rjust(10, '0')
            if not validateID(id):
                print("INVALID ID")
                return
            if validateIDinDB(conn, id):
                displaySpecificData(conn, id)
        elif choice == 6:
            name = input("ENTER PRODUCT NAME: ")
            if not validateName(name):
                print("NOT A VALID NAME")
                return
            searchByProductName(conn, name)
        elif choice == 7:
            id = input("ENTER PRODUCT CODE: ")
            id = id.rjust(10, '0')

            if not validateID(id):
                print("INVALID ID")
                return
            if validateIDinDB(conn, id):
                searchByID(conn, id)
            else:
                print('ID DOES NOT EXISTS')
                return
        elif choice == 8:
            help()
        elif choice == 9:
            print('{:*^100}'.format(" * "))
            print('{:^100}'.format(" THANK YOU . . . VISIT AGAIN "))
            print('{:*^100}'.format(" * "))
            # return False
            # sys.exit()
            # quit()
            global continueLoop
            continueLoop = False;
        else:
            print('{:^100}'.format("INVALID OPTION SELECTED "))

    except:
        print('{:^100}'.format(" AN ERROR OCCURED, SORRY FOR INCONVIENCE "))


if __name__ == '__main__':
    # Creating Connection
    conn = createConnection(r"data.sql")
    # Checking Connection
    if conn == None:
        print("Could Not Create Connection, Exiting....")
        exit()
    # Creating Nessary Tables
    createTable(conn)

    global continueLoop
    continueLoop = True
    while continueLoop:
        mainMenu()
