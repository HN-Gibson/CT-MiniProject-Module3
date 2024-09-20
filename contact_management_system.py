import re

#created a custom error to catch empty inputs
class UserInputEmpty(Exception):
    pass
#created a custom error to catch when user inputs a command not on the list
class CommandNotFound(Exception):
    pass
#created a custom error to catch when the input is not validated
class InvalidEntry(Exception):
    pass
#created a custom error to catch when a contact already exists
class ContactExists(Exception):
    pass
#created a custom error to catch when a contact does not exist
class NoContactFound(Exception):
    pass

def add_contact(phone,name,email,notes):
    contact_info[f'{phone}']={}
    contact_info[f'{phone}']["Name"]=name
    contact_info[f'{phone}']["Phone"]=phone
    contact_info[f'{phone}']["Email"]=email
    contact_info[f'{phone}']["Notes"]=notes
    print("Added the following:")
    contact_for_print=contact_info[phone]
    for key, value in contact_for_print.items():
        print(f"    {key}:{value}")
    return

def edit_contact(contact,info,value):
    contact_info[f'{contact}'][f'{info}']=value
    return print("Contact updated!")         

def delete_contact(contact):
    contact_info.pop(contact)
    return print(f"Information associated with {contact} was deleted!")

def search_contact(contact):
    if contact in contact_info:
        contact_for_print=contact_info[contact]
        for key, value in contact_for_print.items():
            print(f"    {key}:{value}")
    else:
        return print(f"{requested_contact} not found.")
    return

def display_all(dictionary):
    if dictionary == {}:
        print("No Contacts Listed")
    else:
        for contact, info in dictionary.items():
            print(f"Info for {contact}:")
            for key, value in info.items():
                print(f"    {key}:{value}")
    return

def export_contacts(dictionary):
    with open('my_contacts.txt', 'w') as file:
        for contact,info in dictionary.items():
            file.write(f"\n{contact}:")
            for key, value in info.items():
                file.write(f"\n   {key}:{value}")

# def import_contacts(path): #Bonus
#     with open(f'{path}','r') as file:
#         for line in file:
#             contact, info = line.strip().split(':')
#             contact_info[contact]=info

def validate_phone(phone):
    valid_phone = r'\d{3}-\d{3}-\d{4}'
    if re.match(valid_phone,phone):
        return
    else:
        raise InvalidEntry
    
def validate_email(email):
    valid_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(valid_email,email):
        return
    else:
        raise InvalidEntry

menu = ("""
Welcome to the Contact Management System! 
    Menu:
    1. Add a new contact
    2. Edit an existing contact
    3. Delete a contact
    4. Search for a contact
    5. Display all contacts
    6. Export contacts to a text file
    7. Import contacts from a text file (WIP)
    8. Quit
        """)

contact_info = {}

print(menu)

while True:
    try:
        user_request=input("Which menu option would you like to perform?\nPlease enter menu number from the list:\n")
        if user_request == "8":
            break

        elif user_request == "1":
            while True:
                try:
                    add_phone = input("What is the phone number you would like to add?\nType 'q' to return to main menu.\nEnter in XXX-XXX-XXXX format:\n")
                    if add_phone == "q":
                        break
                    elif add_phone == "":
                        raise UserInputEmpty
                    else:
                        validate_phone(add_phone)
                        if add_phone in contact_info:
                            raise ContactExists
                    
                    add_name = input("What is the name for the contact?\n")
                    if add_name == "":
                        raise UserInputEmpty
                    
                    add_email = input("What is the email address?\nMake sure to input a valid email.\n")
                    if add_email == "":
                        raise UserInputEmpty
                    else:
                        validate_email(add_email)
                    
                    add_note= input("Any extra notes for this contact?\n")
                    add_contact(add_phone,add_name,add_email,add_note)
                
                except UserInputEmpty:
                    print("Input was empty.")
                except ContactExists:
                    print("Phone number already exists!")                    
                except InvalidEntry:
                    print("Input did not match the expected format.")    
        
        elif user_request == "2":
            while True:
                try:
                    contact_to_edit=input("What is the phone number for the contact you wish to edit?\nType 'q' to return to main menu.\nEnter in XXX-XXX-XXXX format:\n")
                    if contact_to_edit == "q":
                        break
                    elif contact_to_edit == "":
                        raise UserInputEmpty
                    validate_phone(contact_to_edit)
                    if contact_to_edit not in contact_info:
                        raise NoContactFound
                    info_to_edit=input("Would you like to edit name, phone, email, or notes?\n").lower
                    if info_to_edit() == "":
                        raise UserInputEmpty
                    elif info_to_edit() == "name":
                        new_name = input("What's the new name?\n")
                        edit_contact(contact_to_edit,"Name",new_name)
                    elif info_to_edit() == "phone":
                        new_phone = input("What's the new phone number?\n")
                        validate_phone(new_phone)
                        if new_phone in contact_info:
                            raise ContactExists
                        else:
                            edit_contact(contact_to_edit,"Phone",new_phone)
                            contact_info[f'{new_phone}'] = contact_info.pop(f'{contact_to_edit}')
                    elif info_to_edit() == "email":
                        new_email = input("What's the new email?\n")
                        validate_email(new_email)
                        edit_contact(contact_to_edit,"Email",new_email)
                    elif info_to_edit() == "notes":
                        new_note = input("What's the new note?\nThis action will overwrite the old new entirely\n")
                        edit_contact(contact_to_edit,"Notes",new_note)
                except UserInputEmpty:
                    print("Input was empty.")
                except InvalidEntry:
                    print("Input did not match the expected format.")
                except NoContactFound:
                    print("No contact found.")

        elif user_request == "3":
            while True:
                try:
                    contact_to_delete = input("What is the phone number for the contact you wish to delete?\nType 'q' to return to main menu.\nEnter in XXX-XXX-XXXX format:\n")
                    if contact_to_delete == "q":
                        break
                    elif contact_to_delete == "":
                        raise UserInputEmpty
                    elif contact_to_delete not in contact_info:
                        raise NoContactFound
                    else:
                        validate_phone(contact_to_delete)
                        delete_contact(contact_to_delete)
                except UserInputEmpty:
                    print("Input was empty.")
                except InvalidEntry:
                    print("Input did not match the expected format.")
                except NoContactFound:
                    print("No contact found.")

        elif user_request == "4":
            while True:
                try:        
                    requested_contact = input("What number would you like to search for?\nType 'q' to return to main menu.\nEnter in XXX-XXX-XXXX format:\n")
                    if requested_contact == "q":
                        break
                    elif requested_contact == "":
                        raise UserInputEmpty
                    elif requested_contact not in contact_info:
                        raise NoContactFound
                    else:
                        validate_phone(requested_contact)
                        search_contact(requested_contact)
                except UserInputEmpty:
                    print("Input was empty.")
                except InvalidEntry:
                    print("Input did not match the expected format.")
                except NoContactFound:
                    print("No contact found.")
        
        elif user_request == "5":
            display_all(contact_info)

        elif user_request == "6":
            export_contacts(contact_info)

        elif user_request == "7":
            print("This feature is a work in progress.\nPlease use other features.")
        
        elif user_request == "":
            raise UserInputEmpty 
               
        else:
            raise CommandNotFound
    #implemented an exception to handle when the user enters nothing
    except UserInputEmpty:
        print("Input was empty.")
    #implemented an exception to handle when the user enters a command that doesn't match the options
    except CommandNotFound:
        print("Input doesn't match available commands.")
    
    except InvalidEntry:
        print("Input did not match the expected format.")
    
    except NoContactFound:
        print("No contact found.")
    #used else to print the menu each time the user is prompted to enter a command for the application
    else:
        print(menu)                   
    #ensured the program will always thank the user
    finally:
        if user_request != "8":
            print("Please select another option.")
print("Thank you for using my program!")