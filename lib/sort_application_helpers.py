from helpers import create_user_application_table
from rich import print
from helpers import create_user_application_table, c


def handle_application_sorting(user):
    c.print('How would you like to sort your applications?', style="prompt")
    menu = f'A. by job title \n' \
        + f'B. by company \n' \
        + f'C. by location \n' \
        + f'D. by salary \n' \
        + f'E. by remote \n' \
        + f'F. by application status \n' \
        + f'G. go back to the main menu \n' \
        + f'H. quit the program\n' \

    c.print(menu, style="menu")
    sorting = sorting_choice()
    if sorting == "go back to the main menu":
        return
    process_sorting(sorting, user)

def sorting_choice():
    while True:
        c.print('Please choose a sorting method: A, B, C, D, E, F, G, or H', style="prompt")
        sorting_choice = input().lower()
        if sorting_choice == "h":
            quit()
        if sorting_choice == "g":
            return "go back to the main menu"
        if sorting_choice in ["a", "b", "c", "d", "e", "f"]:
            return sorting_choice
        else:
            c.print('--Invalid response--', style="error")
            continue

def process_sorting(sorting, user):
    table = create_user_application_table(user)
    if sorting == "a":
        c.print("Filtering by: job title", style="success")
        print(table.get_string(sortby="job title"))
    if sorting == "b":
        c.print("Filtering by: company", style="success")
        print(table.get_string(sortby="company"))
    if sorting == "c":
        c.print("Filtering by: location", style="success")
        print(table.get_string(sortby="location"))
    if sorting == "d":
        c.print("Filtering by: salary", style="success")
        print(table.get_string(sortby="salary($)"))
    if sorting == "e":
        c.print("Filtering by: remote", style="success")
        print(table.get_string(sortby="remote"))
    if sorting == "f":
        c.print("Filtering by: application status", style="success")
        print(table.get_string(sortby="application status"))
