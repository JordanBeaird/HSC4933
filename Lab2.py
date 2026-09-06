
heart_rate_samples = {
    "1": {"name": "J. Alvarez", "heart_rates": [72, 75, 78]},
    "2": {"name": "M. Chen", "heart_rates": [80, 82]},
    "3": {"name": "R. Okafor", "heart_rates": [65, 68, 70, 66]},
    "4": {"name": "S. Patel", "heart_rates": [90, 95, 92, 88, 91]},
    "5": {"name": "T. Nguyen", "heart_rates": [77, 79]},
    "6": {"name": "L. Kowalski", "heart_rates": [68, 70, 69]},
    "7": {"name": "D. Osei", "heart_rates": [98, 101, 95, 99]},
    "8": {"name": "A. Whitfield", "heart_rates": [74, 76, 75, 73]}
}


def get_patient_data(patient_number, *args):
    patient = heart_rate_samples[patient_number]
    heart_rates = patient["heart_rates"]

    if not args:
        return patient

    results = {}

    for stat in args:
        if stat == "average":
            results["average"] = sum(heart_rates) / len(heart_rates)

        elif stat == "minimum":
            results["minimum"] = min(heart_rates)

        elif stat == "maximum":
            results["maximum"] = max(heart_rates)

        elif stat == "readings":
            results["readings"] = len(heart_rates)

    return results


patient_number = input("Enter patient number (1-8): ")

if patient_number not in heart_rate_samples:
    print("ERROR.")

else:
    choice = input("Enter 1 for all stats or 2 for specific stats: ")

    if choice == "1":
        patient = get_patient_data(patient_number)

        print("Patient Name:", patient["name"])
        print("Heart Rate Readings:", patient["heart_rates"])

    elif choice == "2":
        print("Available stats: average, minimum, maximum, readings")

        stats_input = input("Enter stats separated by commas: ")
        stats = stats_input.split(",")

        for i in range(len(stats)):
            stats[i] = stats[i].strip().lower()

        results = get_patient_data(patient_number, *stats)

        print("Patient Name:", heart_rate_samples[patient_number]["name"])

        for stat in results:
            print(stat.title() + ":", results[stat])

    else:
        print("ERROR.")


