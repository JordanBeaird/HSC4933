import datetime
from decimal import Decimal

# Profiles provided in the assignment
profiles = [
    {'job': 'Agricultural engineer', 'company': 'Phillips-Johnson',
     'ssn': '055-51-3629', 'residence': '1107 Brian Coves\nSouth Jessica, UT 66862',
     'current_location': (Decimal('-81.6575675'), Decimal('111.794874')),
     'blood_group': 'B+', 'website': ['https://hurley.com/', 'http://www.baker.info/',
                                      'http://silva-jones.com/', 'https://www.mathews.com/'],
     'username': 'nnelson', 'name': 'Oscar Newman', 'sex': 'M',
     'address': '2574 Scott Manors\nPort Aprilfort, MI 13337',
     'mail': 'wgraham@hotmail.com', 'birthdate': datetime.date(1927, 1, 19)},

    {'job': 'Engineer, civil (consulting)', 'company': 'Guzman Inc',
     'ssn': '457-09-3674', 'residence': '8014 Lambert Ways Apt. 285\nSouth Briannaside, KS 13217',
     'current_location': (Decimal('61.686331'), Decimal('-42.036583')),
     'blood_group': 'A-', 'website': ['http://gregory-martin.org/',
                                      'http://tanner.org/', 'https://www.carr.org/'],
     'username': 'lking', 'name': 'Jeremy Wilson', 'sex': 'M',
     'address': '9375 Thomas Alley Suite 536\nNorth Darren, AZ 22956',
     'mail': 'hdeleon@hotmail.com', 'birthdate': datetime.date(1996, 10, 12)},

    {'job': 'Information officer', 'company': 'Green Inc',
     'ssn': '230-42-2169', 'residence': 'Unit 6625 Box 0858\nDPO AE 52466',
     'current_location': (Decimal('-78.802646'), Decimal('-47.996111')),
     'blood_group': 'A-', 'website': ['https://www.watkins.com/',
                                      'http://johnson.org/'],
     'username': 'timothycastro', 'name': 'Kenneth Rhodes', 'sex': 'M',
     'address': '7994 Pearson Square\nHannahmouth, FM 16699',
     'mail': 'sonya72@hotmail.com', 'birthdate': datetime.date(2003, 6, 15)},

    {'job': 'Contracting civil engineer', 'company': 'Smith-Williamson',
     'ssn': '796-76-1297', 'residence': '0041 Brittany Mountains\nNorth Harryshire, MN 69202',
     'current_location': (Decimal('66.422320'), Decimal('107.124001')),
     'blood_group': 'AB+', 'website': ['http://www.nolan.com/'],
     'username': 'debraphillips', 'name': 'Nicole Richardson', 'sex': 'F',
     'address': '303 Wong Trafficway Suite 883\nLake Kiara, MN 78039',
     'mail': 'andrew33@gmail.com', 'birthdate': datetime.date(2003, 9, 7)},

    {'job': 'Engineer, technical sales', 'company': 'Moody-Meza',
     'ssn': '574-63-6422', 'residence': '74438 Moore Fall\nSouth Andrew, GA 64257',
     'current_location': (Decimal('38.089195'), Decimal('35.459581')),
     'blood_group': 'A+', 'website': ['https://brooks-moore.com/'],
     'username': 'xlewis', 'name': 'Gary Gamble', 'sex': 'M',
     'address': '9929 Henderson Branch Suite 961\nLake Mary, AL 36478',
     'mail': 'ambercordova@yahoo.com', 'birthdate': datetime.date(1968, 8, 19)}
]


class AnonyMate:
    pass
def encrypt_profiles(profiles):

    encrypted_profiles = AnonyMate(profiles)
    return encrypted_profiles

def query_profiles(profiles):
    print("\nWhat information would you like to view?")
    print("1. Name")
    print("2. DoB")
    print("3. Sex")
    print("4. Blood Type")

    choice = input("Enter your choice: ")

    if choice == "1":
        field = "name"
    elif choice == "2":
        field = "birthdate"
    elif choice == "3":
        field = "sex"
    elif choice == "4":
        field = "blood_group"
    else:
        print("Invalid choice.")
        return

    print("\nResults:")

    for profile in profiles:
        print(profile[field])

while True:

    print("\n--- Profile System ---")
    print("1. Query profile information")
    print("2. Encrypt profile data")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        query_profiles(profiles)

    elif choice == "2":
        encrypted_profiles = encrypt_profiles(profiles)
        print("\nProfile data has been encrypted using AnonyMate.")
        print(encrypted_profiles)

    elif choice == "3":
        print("End.")
        break

    else:
        print("Invalid choice. Please try again.")


