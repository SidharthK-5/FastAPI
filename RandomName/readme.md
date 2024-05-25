# RandomName

## About

- This is a web application with four cards; _DEV_, _QA_, _Whole team_ and _Co-Host_ (for Team Leads).
- Each card has a button associated with it.
- When you click the button, a random name appears in the corresponding card.
- DEV and QA cards can generate names from their respective team, whole team card will select all members except team leads, Co-Host card will only select team leads.
- In **View All Members** page, members in blue colour are Co-hosts and in gray colour are to be excempted completely from name selection.

## Set-up RandomName in your system

1. Add project logo with name **project_name.png** inside static/images folder.
2. Run the application:

    ```bash
    uvicorn main:app --reload
    ```

3. Add new team members from **Add Members** window.
4. Categorise the members into _DEV_, _QA_ or _Satellite_ (Others contributers or Non-DEV/QA).
5. If they've already selected before, set _Hosting status_ to Yes, No otherwise.
6. Add _Excemption_ status. Tentative is for co-host selection (Team leads).
