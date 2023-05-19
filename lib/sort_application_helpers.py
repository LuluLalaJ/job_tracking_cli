from helpers import create_user_application_table, main_menu, c
from rich import print

def handle_application_sorting(user, session):
    while True:
        c.print('How would you like to view your applications?', style="prompt")
        menu = f'A. by job title \n' \
            + f'B. by company \n' \
            + f'C. by location \n' \
            + f'D. by salary \n' \
            + f'E. by remote \n' \
            + f'F. by application status \n' \
            + f'G. go back to the main menu \n' \
            + f'H. quit the program'
        c.print(menu, style="menu")
        process_sorting(user, session)

def process_sorting(user, session):
    table = create_user_application_table(user)
    c.print('Please choose a sorting method: A, B, C, D, E, F, G, or H', style="prompt")
    sorting = input().lower()
    if sorting == "a":
        c.print("Filtering by: job title", style="success")
        print(table.get_string(sortby="job title"))
    elif sorting == "b":
        c.print("Filtering by: company", style="success")
        print(table.get_string(sortby="company"))
    elif sorting == "c":
        c.print("Filtering by: location", style="success")
        print(table.get_string(sortby="location"))
    elif sorting == "d":
        c.print("Filtering by: salary", style="success")
        print(table.get_string(sortby="salary($)"))
    elif sorting == "e":
        c.print("Filtering by: remote", style="success")
        print(table.get_string(sortby="remote"))
    elif sorting == "f":
        c.print("Filtering by: application status", style="success")
        print(table.get_string(sortby="application status"))
    elif sorting == "g":
        main_menu(session, user)
    elif sorting == "h":
        quit()
    else:
        c.print('Invalid input. Please enter a valid letter.', style="error")
