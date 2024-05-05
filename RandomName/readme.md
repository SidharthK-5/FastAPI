# RandomName

## About
- This is a single page web application with three cards; DEV, QA and Whole team.
- Each card has a button associated with it.
- When you click the button, a random name appears in the corresponding card.
- DEV and QA cards can generate names from their respective team, and the last card will generate names from both teams.

## Set-up Instructions

1. Create a file **team_members.py** inside **RandomName**
2. Create two lists DEV_TEAM and QA_TEAM.
3. Add a third list WHOLE_TEAM as the sum of the first two.

### Sample file
```python team_members.py
DEV_TEAM = [
    "Tony",
    "Steve",
    "Bruce",
    "Thor",
    "Natasha",
    "Clint",
]
QA_TEAM = [
    "Nick",
    "Phill",
    "Maria",
]
WHOLE_TEAM = DEV_TEAM + QA_TEAM
```