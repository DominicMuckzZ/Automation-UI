# Automation-UI
A User Interface that allows users to create and save simple processes to repeat a task multiple times whilst working its way through a CSV file.
  
## Funcitonality  
The User Interface allows for a user to set up a repetitive task and automate it.
The processes are simple instructions for where the mouse should be, if a button should be pressed, if any data from the CSV File should be typed out.
These are controllable through the buttons on the UI, however for the mouse position there is also the hotkey Alt + x which will get the current mouse position.

### 'Run' Button
The run button will start running through the instructions that have been set up.
This will repeat through the number of rows in the CSV File and stop once complete.

### The Sheet View
The sheet view will populate the data from the CSV file when loaded.
There is the option of setting the first row of the sheet to be the Header data and will allow users to identify the rows clearly.
If a user double clicks on the sheet view it will add the column to the instruction list to be output through the keyboard method as though the user typed the word.

### Buttons Frame
The buttons frame shows multiple buttons that can add a desired output to the process.
These buttons are:
* Left Click: Which will simulate the left click on the mouse
* Right Click: Which will simulate the right click on the mouse
* Select All: Which will simulate the keys Ctrl + A being pressed
* Back: Which simulates the Backspace key being pressed
* Enter: Which simulates the Enter key being pressed

### Mouse Position Frame
This contains two fields, These allow for the user to enter a Y and X coordinate and when the 'Add Pos' button is pressed, these coordinates are added to the instruction list and will define where the mouse will go on the screen.
This is for users who know where on the screen the mouse needs to goto. Otherwise users can use the hotkey 'Alt + X' which will add the current position of the mouse to the process list.

### Sidebar
The sidebar contains the previously discussed 'Add Pos' button, but also the following:
* Remove: Which will remove the selected item from the process list
* Load File: Which will prompt the user to select a CSV file, and then proceed to display it on the sheet view
* The instruction list: Which displays a list of the steps the system will go through
* Load Auto: Will load a previously setup process ready to be used on the new file
* Save Auto: Will prompt the user to save the current automation process for later use

### Settings
The settings allow for two current options:
Whether the first row of the CSV file is to be used as Headings for the sheet view.
What the delay between steps in the instruction list should be (in seconds), the default value is 0.2

## Current Limitations
The user interface is not beautiful, it accomplishes the task of housing the backend.
The instruction listbox only displays a certain number of steps and does not currently house the ability to scroll through them.
Users are unable to add custom keyboard shortcuts.
Users can not run a process for a limited iteration without a CSV.

## New Updates
Minor Bug fix
