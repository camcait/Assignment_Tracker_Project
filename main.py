from bakery import assert_equal
from drafter import *
from dataclasses import dataclass



hide_debug_information()
set_website_title("Assignment Tracker")
set_website_framed(False)
set_site_information(author = "Caitlin Cammett", description = "Assignment Tracker to help students stay organized", sources = ["https://chatgpt.com/"], planning = ["Caitlin Cammett CS1 Final Project 1: Design","LLM Documentation", "Caitlin Cammett CS1 Final Project 0: Pick a Problem"], links = ["https://camcait.github.io/Assignment_Tracker_Project/"], server=None)


# Stores information about one assignment
@dataclass
class Assignment:
    name: str
    completed: bool
    subject: str


# Stores the information for the entire website
@dataclass
class State:
    assignments: list[Assignment]
    new_assignment: str
    page_title: str
    show_completed: bool
    message: str


# Navigation buttons used throughout the website
def navigation():
    '''
This function is the main organization for
all of the buttons on the homepage of the website
Inputs are the user clikcing the buttons listed below.
'''
    return [
        Button("Home", "index"),
        Button("Add Assignment", "add_assignment"),
        Button("All Assignments", "view_assignments"),
        Button("Incomplete", "view_incomplete"),
        Button("Completed", "view_complete"),
        "\n"
    ]


# Displays assignments based on the selected filter
def assignment_page(state: State, show_all: bool = False) -> Page:
    '''
This function is the basis of the assignment page. It presents the assignment
page header, along with all inputs.
Args:
state: State
show_all: a list of the assignments that start with an uncomplete status

Return:
returns the assignment page
'''
    content = [
        Header(state.page_title),
        state.message,
        "\n"
    ]

    found_assignment = False

    # Loop through every assignment in the list
    for index, assignment in enumerate(state.assignments):

        # Check whether the assignment should be displayed
        if show_all or assignment.completed == state.show_completed:

            found_assignment = True

            # Check whether the assignment is finished
            if assignment.completed:
                status = "Completed"
            else:
                status = "Incomplete"

            content.append(
                assignment.name + " | Subject: " +
                assignment.subject + " | Status: " + status + "\n"
            )

            # Only show this button for unfinished assignments
            if not assignment.completed:
                content.append(
                    Button(
                        "Mark as Finished",
                        "mark_finished",
                        [Argument("assignment_index", index)]
                    )
                )

            content.append("\n")

    if not found_assignment:
        content.append("No assignments to display yet!\n")

    content.extend(navigation())

    return Page(state, content)


# ROUTE 1: Homepage
@route
def index(state: State) -> Page:
    state.page_title = "Student Assignment Tracker"
    '''
This route defines the homepage. This is where all the buttons
are located for the user to click.
'''

    return Page(state, [
        Header(state.page_title),
        "Welcome to your assignment tracker!",
        "\n",
        "Keep track of your homework and stay organized.",
        "\n",
        Header("What would you like to do?"),
        Button("Add a New Assignment", "add_assignment"),
        Button("View All Assignments", "view_assignments"),
        Button("View Incomplete Assignments", "view_incomplete"),
        Button("View Completed Assignments", "view_complete")
    ])


# ROUTE 2: Add assignment page
@route
def add_assignment(state: State) -> Page:
    ''' This function takes in user input to create a list
of assignments.

Args:
state: State

Return:
A page


'''
    state.page_title = "Add a New Assignment"

    return Page(state, [
        Header(state.page_title),
        state.message,
        "\n",

        "Enter the name of your assignment:",
        TextBox("new_assignment", state.new_assignment),
        "\n",

        "Select the subject:",
        SelectBox(
            "subject",
            ["Math", "English", "Science", "History", "Other"]
        ),
        "\n",

        "Is this assignment already completed?",
        CheckBox("already_completed", False),
        "\n",

        Button("Save Assignment", "save_assignment"),
        *navigation()
    ])


# ROUTE 3: Save assignment
@route
def save_assignment(
    state: State,
    new_assignment: str,
    subject: str,
    already_completed: bool
) -> Page:
    '''
This function creates a way to save the new inputted information

Args:
state: State
new_assignment: a string title of an assignment
subject: the subject of the assignment
already_completed: whether the assignment is complete or not

Return:
A page
'''

    state.new_assignment = new_assignment

    # Check whether the assignment name is empty
    if new_assignment.strip() == "":
        state.message = "Error: Please enter an assignment name!"
        return add_assignment(state)

    # Create a new Assignment object
    assignment = Assignment(
        new_assignment,
        already_completed,
        subject
    )

    # Add the assignment to the list
    state.assignments.append(assignment)

    state.new_assignment = ""
    state.message = "Your assignment was successfully saved!"

    return view_assignments(state)


# ROUTE 4: View all assignments
@route
def view_assignments(state: State) -> Page:
    '''
This route allows the user to view the new list of assignments they just inputted.
'''
    state.page_title = "All Assignments"
    return assignment_page(state, True)


# ROUTE 5: Mark an assignment as finished
@route
def mark_finished(state: State, assignment_index: int) -> Page:
    '''
This route allows the user to mark an assignment as completed.
Args:
state: State
assignment_index: the index value of the assignment

Return:
A page
'''

    # Make sure the assignment index is valid
    if 0 <= assignment_index < len(state.assignments):

        # Change the completion status
        state.assignments[assignment_index].completed = True

        state.message = "Assignment marked as completed!"

    return view_assignments(state)


# ROUTE 6: View incomplete assignments
@route
def view_incomplete(state: State) -> Page:
    '''This route allows the user to view a list of incomplete
assignments only
'''
    state.page_title = "Incomplete Assignments"
    state.show_completed = False
    state.message = ""

    return assignment_page(state)


# ROUTE 7: View completed assignments
@route
def view_complete(state: State) -> Page:
    '''This route allows the user to view a list of complete
assignments only
'''
    state.page_title = "Completed Assignments"
    state.show_completed = True
    state.message = ""

    return assignment_page(state)


# Start the website
start_server(State(
    assignments=[],
    new_assignment="",
    page_title="Student Assignment Tracker",
    show_completed=False,
    message=""
))

