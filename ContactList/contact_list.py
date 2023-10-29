import sqlite3
import csv
import json
from datetime import datetime
from tabulate import tabulate

class ContactManaging:
    def __init__(self, db_name, csv_name, json_name, ismetify_name):
        self.db_name = db_name
        self.csv_name = csv_name
        self.json_name = json_name
        self.ismetify_name = ismetify_name
        self.create_contact_table()
        ##################################################################################################
        ################################################################################################## Kodu calistirirken csv json ve ismetify dosyalari yoksa alttaki 3 satiri acarak dosyalari olusturuyorum ama sonrasinda alttaki 3 satiri tekrar kapatmam gerekiyor yoksa dosyalari tekrar tekrar yaratiyor icleri bos gozukuyor. Cozumunu bulamadim.
        ##################################################################################################
        ##################################################################################################
        # self.create_csv_file()      
        # self.create_json_file()     
        # self.create_ismetify_file() 
        ##################################################################################################
        ##################################################################################################

    def create_contact_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                email TEXT,
                creation_date TEXT,
                last_edit_date TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def create_csv_file(self):
        with open(self.csv_name, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["id", "first_name", "last_name", "phone", "email", "creation_date", "last_edit_date"])

    def create_json_file(self):
        with open(self.json_name, 'w') as file:
            json.dump([], file)

    def create_ismetify_file(self):
        with open(self.ismetify_name, 'w') as file:
            file.write("id|first_name|last_name|phone|email|creation_date|last_edit_date\n")

    def add_contact(self, first_name, last_name, phone, email):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Contacts (first_name, last_name, phone, email, creation_date, last_edit_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, phone, email, current_time, current_time))
        conn.commit()
        contact_id = cursor.lastrowid
        conn.close()

        self.add_contact_to_csv(contact_id, first_name, last_name, phone, email, current_time, current_time)
        self.add_contact_to_json(contact_id, first_name, last_name, phone, email, current_time, current_time)
        self.add_contact_to_ismetify(contact_id, first_name, last_name, phone, email, current_time, current_time)

    def add_contact_to_csv(self, contact_id, first_name, last_name, phone, email, creation_date, last_edit_date):
        data = [contact_id, first_name.capitalize(), last_name.capitalize(), phone, email, creation_date, last_edit_date]
        self.write_to_csv(self.csv_name, data)

    def add_contact_to_json(self, contact_id, first_name, last_name, phone, email, creation_date, last_edit_date):
        with open(self.json_name, 'r') as file:
            data = json.load(file)
        
        contact_data = {
            "id": contact_id,
            "first_name": first_name.capitalize(),
            "last_name": last_name.capitalize(),
            "phone": phone,
            "email": email,
            "creation_date": creation_date,
            "last_edit_date": last_edit_date
        }
        data.append(contact_data)
        
        with open(self.json_name, 'w') as file:
            json.dump(data, file, indent=2)

    def add_contact_to_ismetify(self, contact_id, first_name, last_name, phone, email, creation_date, last_edit_date):
        with open(self.ismetify_name, 'a') as file:
            line = f'{contact_id}|{first_name.capitalize()}|{last_name.capitalize()}|{phone}|{email}|{creation_date}|{last_edit_date}\n'
            file.write(line)

    def edit_contact(self, contact_id, first_name, last_name, phone, email):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Contacts
            SET first_name = ?, last_name = ?, phone = ?, email = ?, last_edit_date = ?
            WHERE id = ?
        ''', (first_name, last_name, phone, email, current_time, contact_id))
        self.update_csv_contact(contact_id, first_name, last_name, phone, email, current_time)
        self.update_json_contact(contact_id, first_name, last_name, phone, email, current_time)
        self.update_ismetify_contact(contact_id, first_name, last_name, phone, email, current_time)
        conn.commit()
        conn.close()

    def update_csv_contact(self, contact_id, first_name, last_name, phone, email, last_edit_date):
        with open(self.csv_name, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            data = list(reader)
            headerrow = data.pop(0)


        for i, item in enumerate(data):
            # if item[0].isdigit():
            # if int(item[0]) == contact_id:
            if item[0] == str(contact_id):
                data[i][1] = first_name
                data[i][2] = last_name
                data[i][3] = phone
                data[i][4] = email
                data[i][5] = last_edit_date

        with open(self.csv_name, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(headerrow)
            writer.writerows(data)

    def update_json_contact(self, contact_id, first_name, last_name, phone, email, last_edit_date):
        with open(self.json_name, 'r') as file:
            data = json.load(file)

        for i, contact in enumerate(data):
            # print(type(contact.get("id")))
            # print(type(contact_id))
            if contact.get("id") == int(contact_id):
                # print("deneme")
                data[i]["first_name"] = first_name
                data[i]["last_name"] = last_name
                data[i]["phone"] = phone
                data[i]["email"] = email
                data[i]["last_edit_date"] = last_edit_date

        with open(self.json_name, 'w') as file:
            json.dump(data, file, indent=2)

    def update_ismetify_contact(self, contact_id, first_name, last_name, phone, email, last_edit_date):
        with open(self.ismetify_name, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            parts = line.strip().split('|')
            # if parts[0].isdigit():
            if parts[0] == str(contact_id):
                parts[1] = first_name
                parts[2] = last_name
                parts[3] = phone
                parts[4] = email
                parts[5] = last_edit_date
                lines[i] = '|'.join(parts) + '\n'

        with open(self.ismetify_name, 'w') as file:
            file.writelines(lines)

    def delete_contact(self, contact_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Contacts WHERE id = ?', (contact_id,))
        self.delete_csv_contact(contact_id)
        self.delete_json_contact(contact_id)
        self.delete_ismetify_contact(contact_id)
        conn.commit()
        conn.close()

    def delete_csv_contact(self, contact_id):
        with open(self.csv_name, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            data = list(reader)

        # new_data = [item for item in data if item[0].isdigit() and int(item[0]) != contact_id]

        new_data = [item for item in data if item[0] != str(contact_id)]

        with open(self.csv_name, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(new_data)

    def delete_json_contact(self, contact_id):
        with open(self.json_name, 'r') as file:
            data = json.load(file)

        data = [contact for contact in data if contact.get("id") != int(contact_id)]

        with open(self.json_name, 'w') as file:
            json.dump(data, file, indent=2)

    def delete_ismetify_contact(self, contact_id):
        with open(self.ismetify_name, 'r') as file:
            lines = file.readlines()

        new_lines = [line for line in lines if line.strip().split('|')[0] != str(contact_id)]

        with open(self.ismetify_name, 'w') as file:
            file.writelines(new_lines)


    def list_contacts(self, search_term, order_by):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()


        if order_by == "First name":
            order_by_clause_sql = "ORDER BY first_name"
            order_by_clause_csv = "first_name"
            order_by_clause_json = "first_name"
            order_by_clause_ismetify = "first_name"
        elif order_by == "Last name":
            order_by_clause_sql = "ORDER BY last_name"
            order_by_clause_csv = "last_name"
            order_by_clause_json = "last_name"
            order_by_clause_ismetify = "last_name"
        elif order_by == "Creation date":
            order_by_clause_sql = "ORDER BY creation_date"
            order_by_clause_csv = "creation_date"
            order_by_clause_json = "creation_date"
            order_by_clause_ismetify = "creation_date"
        elif order_by == "Last edit date":
            order_by_clause_sql = "ORDER BY last_edit_date"
            order_by_clause_csv = "last_edit_date"
            order_by_clause_json = "last_edit_date"
            order_by_clause_ismetify = "last_edit_date"
        else:
            order_by_clause_sql = ""
            order_by_clause_csv = ""
            order_by_clause_json = ""
            order_by_clause_ismetify = ""
    
        cursor.execute('''
            SELECT * FROM Contacts
            WHERE first_name LIKE ? OR last_name LIKE ? OR creation_date LIKE ? OR last_edit_date LIKE ?
            {}
        '''.format(order_by_clause_sql), (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        results = cursor.fetchall()
        conn.close()


        print("\n","\n")
        if results:
            print("Search results (SQLite):")
            headers_sql = ["ID", "First Name", "Last Name", "Creation Date"]
            table_data_sql = []
            for row in results:
                # print(f"{row[0]} - {row[1]} {row[2]} - Creation Date: {row[5]}")
                table_data_sql.append([row[0], row[1], row[2], row[5]])
            table_sql = tabulate(table_data_sql, headers_sql, tablefmt="grid")
            print(table_sql)
            print("\n","\n")


        
        csv_results = self.search_csv_contacts(search_term, order_by_clause_csv)
        if csv_results:
            print("Search results (CSV):")
            # print(csv_results)
            headers_csv = ["ID", "First Name", "Last Name", "Creation Date"]
            table_data_csv = []

            first_result_skipped = False

            for row in csv_results:
                if not first_result_skipped and search_term == "" and order_by_clause_csv == "":
                    first_result_skipped = True
                    continue
                #print(f"{row[0]} - {row[1]} {row[2]} - Creation Date: {row[5]}")
                table_data_csv.append([row[0], row[1], row[2], row[5]])
            table_csv = tabulate(table_data_csv, headers_csv, tablefmt="pretty")
            print(table_csv)
            print("\n","\n")

        
        json_results = self.search_json_contacts(search_term,order_by_clause_json)
        if json_results:
            print("Search results (JSON):")
            headers_json = ["ID", "First Name", "Last Name", "Creation Date"]
            table_data_json = []
            for contact in json_results:
                # print(f"{contact['id']} - {contact['first_name']} {contact['last_name']} - Creation Date: {contact['creation_date']}")
                table_data_json.append([contact['id'], contact['first_name'], contact['last_name'], contact['creation_date']])
            table_json = tabulate(table_data_json, headers_json, tablefmt="simple")
            print(table_json)
            print("\n","\n")
            


        
        ismetify_results = self.search_ismetify_contacts(search_term, order_by_clause_ismetify)
        if ismetify_results:
            print("Search results (Ismetify):")
            headers_ismetify = ["ID", "First Name", "Last Name", "Creation Date"]
            table_data_ismetify = []

            first_result_skipped = False


            for line in ismetify_results:
                if not first_result_skipped and search_term == "" and order_by_clause_ismetify == "":
                    first_result_skipped = True
                    continue
                parts = line.strip().split('|')
                # print(f"{parts[0]} - {parts[1]} {parts[2]} - Creation Date: {parts[5]}")
                table_data_ismetify.append([parts[0], parts[1], parts[2], parts[5]])
            table_ismetify = tabulate(table_data_ismetify, headers_ismetify, tablefmt="pipe")

            print(table_ismetify)
            print("\n","\n")


    def search_csv_contacts(self, search_term, order_by_clause_csv):
        with open(self.csv_name, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            data = list(reader)
        
        if order_by_clause_csv == "first_name":
            data.sort(key=lambda x: x[1])
        elif order_by_clause_csv == "last_name":
            data.sort(key=lambda x: x[2])
        elif order_by_clause_csv == "creation_date":
            data.sort(key=lambda x: x[5])
        elif order_by_clause_csv == "last_edit_date":
            data.sort(key=lambda x: x[6])


        
        results = [item for item in data if search_term.capitalize() in item[1] or search_term.capitalize() in item[2] or search_term in item[5] or search_term in item[6]]
        return results

    def search_json_contacts(self, search_term, order_by_clause):
        with open(self.json_name, 'r') as file:
            data = json.load(file)

        if order_by_clause:
            data.sort(key=lambda x: x[order_by_clause])
        
        results = [contact for contact in data if search_term.capitalize() in contact["first_name"] or search_term.capitalize() in contact["last_name"] or search_term in contact["creation_date"] or search_term in contact["last_edit_date"]]
        return results

    def search_ismetify_contacts(self, search_term, order_by_clause_ismetify):
        with open(self.ismetify_name, 'r') as file:
            lines = file.readlines()

        if order_by_clause_ismetify == "first_name":
            lines.sort(key=lambda line: line.strip().split('|')[1])
        elif order_by_clause_ismetify == "last_name":
            lines.sort(key=lambda line: line.strip().split('|')[2])
        elif order_by_clause_ismetify == "creation_date":
            lines.sort(key=lambda line: line.strip().split('|')[5])
        elif order_by_clause_ismetify == "last_edit_date":
            lines.sort(key=lambda line: line.strip().split('|')[6])

        
        results = [line for line in lines if search_term.capitalize() in line]
        return results
    
    def restore_data(self):
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        
        cursor.execute('SELECT * FROM Contacts')
        contacts = cursor.fetchall()

        for contact in contacts:
            contact_id, first_name, last_name, phone, email, creation_date, last_edit_date = contact

            
            csv_contact = self.find_csv_contact(contact_id)
            if not csv_contact:
                self.add_contact_to_csv(contact_id, first_name, last_name, phone, email, creation_date, last_edit_date)
            
            json_contact = self.find_json_contact(contact_id)
            if not json_contact:
                self.add_contact_to_json(contact_id, first_name, last_name, phone, email, creation_date, last_edit_date)
            
            ismetify_contact = self.find_ismetify_contact(contact_id)
            if not ismetify_contact:
                self.add_contact_to_ismetify(contact_id, first_name, last_name, phone, email, creation_date, last_edit_date)

        conn.close()

    def find_csv_contact(self, contact_id):
        with open(self.csv_name, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if row[0].isdigit() and int(row[0]) == contact_id:
                    return row
            return None

    def find_json_contact(self, contact_id):
        with open(self.json_name, 'r') as file:
            data = json.load(file)
            for contact in data:
                if contact.get("id") == contact_id:
                    return contact
            return None

    def find_ismetify_contact(self, contact_id):
        with open(self.ismetify_name, 'r') as file:
            lines = file.readlines()
            for line in lines[1:]:
                parts = line.strip().split('|')
                if parts[0].isdigit() and int(parts[0]) == contact_id:
                    return parts
            return None

    def get_next_csv_id(self):
        with open(self.csv_name, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            data = list(reader)
            if not data:
                return 1
            elif data[-1][0].isdigit():
                return int(data[-1][0]) + 1

    def get_next_json_id(self):
        with open(self.json_name, 'r') as file:
            data = json.load(file)
            if not data:
                return 1
            return data[-1]["id"] + 1

    def get_next_ismetify_id(self):
        with open(self.ismetify_name, 'r') as file:
            lines = file.readlines()
            if not lines:
                return 1
            last_line = lines[-1].strip()
            parts = last_line.split('|')
        if parts[0].isdigit():
            return int(parts[0]) + 1
        
    def write_to_csv(self, contacts, data):
        with open(contacts, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(data)

    def write_to_json(self, contacts, data):
        with open(contacts, 'a') as file:
            json.dump(data, file, indent=2)
            file.write('\n')

    def write_to_ismetify(self, contacts, data):
        with open(contacts, 'a') as file:
            data = [str(item) if item is not None else '' for item in data]
            line = '|'.join(data)
            file.write(f'{line}\n')

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem

def add_contact_menu():
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    phone = input("Enter Phone Number: ")
    email = input("Enter Email: ")
    manager.add_contact(first_name, last_name, phone, email)
    print("Contact added successfully!")
    input("Press Enter to continue...")

def delete_contact_menu():
    contact_id = input("Enter Contact ID to Delete: ")
    manager.delete_contact(contact_id)
    print("Contact deleted successfully!")
    input("Press Enter to continue...")

def list_contacts_menu():
    search_term = input("Enter a search term (leave empty to list all contacts): ")
    order_by = input("Order by (First name, Last name, Creation date, Last edit date): ")
    manager.list_contacts(search_term, order_by)
    input("Press Enter to continue...")

def edit_contact_menu():
    contact_id = input("Enter Contact ID to Edit: ")
    first_name = input("Enter New First Name: ")
    last_name = input("Enter New Last Name: ")
    phone = input("Enter New Phone Number: ")
    email = input("Enter New Email: ")
    manager.edit_contact(contact_id, first_name, last_name, phone, email)
    print("Contact edited successfully!")
    input("Press Enter to continue...")

def restore_data_menu():
    manager.restore_data()
    print("Data restored from backups successfully!")
    input("Press Enter to continue...")

# def exit_program_menu():
#     print("Exiting the program...")
#     exit()

menu = ConsoleMenu("Main Page", "Select an option:")

menu.append_item(FunctionItem("Add Contact", add_contact_menu))
menu.append_item(FunctionItem("Delete Contact", delete_contact_menu))
menu.append_item(FunctionItem("List Contacts", list_contacts_menu))
menu.append_item(FunctionItem("Edit Contact", edit_contact_menu))
menu.append_item(FunctionItem("Restore from Backup", restore_data_menu))
# menu.append_item(FunctionItem("Exit", exit_program_menu))

if __name__ == "__main__":
    manager = ContactManaging('contact_list.db', 'contacts.csv', 'contacts.json', 'contacts.txt')
    menu.show()