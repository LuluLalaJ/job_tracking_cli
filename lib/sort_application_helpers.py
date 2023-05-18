from helpers import create_user_application_table
from rich import print


def handle_application_sorting(user):
    menu = f'How would you like to sort your applications? \n' \
        + f'A. by job title \n' \
        + f'B. by company \n' \
        + f'C. by location \n' \
        + f'D. by salary \n' \
        + f'E. by remote \n' \
        + f'F. by application status \n' \
        + f'G. go back to the main menu \n' \
        + f'H. quit the program\n' \

    print(menu)
    sorting = sorting_choice()
    if sorting == "go back to the main menu":
        return
    process_sorting(sorting, user)

def sorting_choice():
    while True:
        print('Please choose a sorting method: A, B, C, D, E, F, G, or H')
        sorting_choice = input().lower()
        if sorting_choice == "h":
            quit()
        if sorting_choice == "g":
            return "go back to the main menu"
        if sorting_choice in ["a", "b", "c", "d", "e", "f"]:
            return sorting_choice
        else:
            print('--Invalid response--')
            continue

def process_sorting(sorting, user):
    table = create_user_application_table(user)
    if sorting == "a":
        print("Filtering by: job title")
        print(table.get_string(sortby="job title"))
    if sorting == "b":
        print("Filtering by: company")
        print(table.get_string(sortby="company"))
    if sorting == "c":
        print("Filtering by: location")
        print(table.get_string(sortby="location"))
    if sorting == "d":
        print("Filtering by: salary")
        print(table.get_string(sortby="salary($)"))
    if sorting == "e":
        print("Filtering by: remote")
        print(table.get_string(sortby="remote"))
    if sorting == "f":
        print("Filtering by: application status")
        print(table.get_string(sortby="application status"))
