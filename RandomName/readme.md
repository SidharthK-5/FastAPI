# RandomName

## About

- This is a single page web application with three cards; DEV, QA and Whole team.
- Each card has a button associated with it.
- When you click the button, a random name appears in the corresponding card.
- DEV and QA cards can generate names from their respective team, and the last card will generate names from both teams.

## Set-up Instructions

1. Create a file **team_members.py** inside **RandomName**
2. Create two lists _DEV_TEAM_ and _QA_TEAM_.
3. Add an optional list _OTHER_TEAM_ for members who don't belong to DEV or QA.
4. Create a list _EXCEPTION_LIST_ for the members to be excluded from random selection
5. Set the list _WHOLE_TEAM_ as the sum of lists except _EXCEPTION_LIST_. Add _OTHER_TEAM_ only if it is set.

### Sample of team_members.py

```python
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
OTHER_TEAM = [
    "Peter",
    "Rocket",
    "Groot",
    "Gamora",
    "Drax",
]
EXCEPTION_LIST = []

try:
    WHOLE_TEAM = DEV_TEAM + QA_TEAM + OTHER_TEAM
except NameError:
    WHOLE_TEAM = DEV_TEAM + QA_TEAM
```
