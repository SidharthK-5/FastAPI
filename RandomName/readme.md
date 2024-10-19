# RandomName

(This project has been moved to a different repository)

## Overview  

RandomName is a robust web application designed to facilitate selecting members for specific events within teams, avoiding confusion of team manager to choose from the long-list. The app features four distinct cards: _DEV_, _QA_, _Whole Team_, and _Co-Host_ (specifically designed for Team Leads).
  
Each card has an associated button that, when clicked, generates a random name from the corresponding team. This feature is especially useful for randomly assigning tasks, picking meeting participants, or simply adding a bit of fun to your team interactions.  

- The **DEV** and **QA** cards generate names from their respective teams.  
- The **Whole Team** card selects from all team members, excluding team leads.  
- The **Co-Host** card specifically selects team leads.  

In the **View All Members** page, you'll find a comprehensive list of your team members. Co-hosts are highlighted in blue, while members marked in gray are exempted from name selection.  

## Installation Guide  

Follow these steps to set-up RandomName in your system:  

1. Create a virtual environment named 'randomenv'  
  
    ```bash  
    python -m venv randomenv  
    ```  

2. Activate the virtual environment  
  
    ```bash  
    source randomenv/bin/activate # On Mac/Linux  
    .\randomenv\Scripts\activate # On Windows  
    ```  

3. Install the required libraries  
  
    ```bash  
    pip install -r requirements.txt  
    ```  

4. Add your project logo with the file name **project_name.png** inside the static/images folder.  

5. Launch the application:  
  
    ```bash  
    uvicorn main:app --reload  
    ```  

## Usage Guide  

Once you've set up RandomName, you can begin adding team members and categorizing them:  

1. Add new team members via the **Add Members** window.  
2. Categorize each member as either _DEV_, _QA_, or _Satellite_ (for contributors who aren't part of the DEV/QA team).  
3. Indicate each member's _Hosting Status_. Set this to 'Yes' if they've been selected before, 'No' otherwise.  
4. Set the _Exemption Status_ for each member. 'Tentative' is for potential co-host selection (team leads).  

You're all set! Enjoy using RandomName to enhance your team's organization and communication.  
