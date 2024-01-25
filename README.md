# Warehouse control application

Created by [Rosvaldas Šlekys](https://github.com/RosSlek) 

This project was made to deepen my knowledge about python, SQL databases, learn new things and better understand what I already knew.

## The main goals for this project were to:
#### • Create app, which could be used for small business. Ensure traceability in warehouse and production.
#### • Create SQL database
#### • Track material quantities
#### • Have fun and improve

## Main steps:
#### •	Create UI using Tkinter.
#### •	Create SQL database for warehouse materials, materials in production and production register.
#### •  Add functionality and comfortability.

## Result:
### Created UI to represent daily routines.

![image](https://github.com/RosSlek/Sandelio_programa/assets/149397027/67a7d76b-15ba-468e-bec4-bf71b664845c)

### Created functions to add materials to the warehouse, transfer materials to production with optional comment fields and timestamps when action occured. Functions to show remaining inventory in warehouse and production, informational popup windows.

![image](https://github.com/RosSlek/Sandelio_programa/assets/149397027/6ebef651-89f8-44ca-9906-e68b6b8ed78d)

![image](https://github.com/RosSlek/Sandelio_programa/assets/149397027/150a93fb-7f73-43e3-b960-1c90c022dba6)

### Created function to registrate work orders, to write off used materials, added safety features to fill correct data.

![image](https://github.com/RosSlek/Sandelio_programa/assets/149397027/dd4843f8-6c22-4c83-8254-11fe853d8084)

### Added switches to change view of inventory in warehouse/production, light/dark mode.

![image](https://github.com/RosSlek/Sandelio_programa/assets/149397027/71deef22-6481-47a7-b53b-fe8cfdfcec9c)

### Program creates excel files (not CSV, so it would be more friendly to lithuanian language and user) with history of every action, in case of mistakes it can be easily corrected manually. Positive numbers show added materials, negative - removed or consumed.


## Conslusion
It was a really nice experience to work on this project, a bunch of new things learned, tons of bugs and puzzles to solve. I`m quite happy with the result and will continue to develop my skills. You can download this apllication and try it yourself [here](https://www.dropbox.com/scl/fi/vfekzijr6ds3hh8i2ra6b/Sand-lio-programa.rar?rlkey=svv8ing3xq0fnenmi4ja4289h&dl=0).
*Excel and exe files have to be in the directory they are, create shortcuts if needed. There also master files created deeper in the '_internal' folder with warehouse and production history so they could be restored if main excel files become corrupted.
