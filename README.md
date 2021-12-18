## Project Name
Run the Set!           - https://runtheset.herokuapp.com
Run the Set! - Backend - https://runtheset-backend.herokuapp.com


## Project Description
This app's goal is to provide a means where players of Street Fighter 3: 3rd Strike can record their wins and losses of matches they play. This will allow players to track their performance over time and view their match history to give them a better view of their progression. 


## Technologies Used
Django, React, Postgres, CSS, HTML


## Installation Steps
1. Clone the repo
2. Run `npm i` for the frontend in the root folder to install packages. For the backend, run `python3 -m venv venv` in the root folder to create a virtual environment 'venv'. Then, run `source venv/bin/activate` to enable the environment. Finally, run `pip3 install -r requirements.txt` to install packages.
3. 3. Run `npm start` in the frontend root directory to start the React Server. Run `python3 manage.py runserver` to start the backend server.


## User Stories
As a player, I want to select two players and their characters and record the winner and the score.
As a player, I want to be able to add players to expand who I can record matches against.
As a player, I want to be able to see the stats between players.


> Models including field names and their datatypes<br />
![Screen Shot 2021-12-18 at 9 46 30 AM](https://user-images.githubusercontent.com/43842580/146647039-4942887b-3a3a-484e-9251-e915c98eb946.png)

## Backend Routes - Base URL: https://runtheset-backend.herokuapp.com
POST /users/register - create route to make a user
POST /users/login - to sign into the user
DELETE /users/:id - to delete a user
PUT /users/:id - to update user info

GET /players - Displays a list of all players
POST /players - Creates a new player
PUT /players/:id - Updates a player's info
DELETE /players/:id - Deletes a player (Should only be used for admin purposes, not app functionality)

GET /matches - Lists all matches
POST /matches - Creates a new match
PUT /matches/:id - Updates match info
DELETE /matches/:id - Deletes Match info 

## Wireframes
![Screen Shot 2021-11-27 at 7 44 37 PM](https://media.git.generalassemb.ly/user/36937/files/511d5c00-4fbb-11ec-97d1-91dc0aad8006)
![Screen Shot 2021-11-27 at 7 27 56 PM](https://media.git.generalassemb.ly/user/36937/files/51b5f280-4fbb-11ec-8337-1f8fdf2fede0)
![Screen Shot 2021-11-27 at 7 49 28 PM](https://media.git.generalassemb.ly/user/36937/files/51b5f280-4fbb-11ec-9837-d6b4b0ddcee4)
![Screen Shot 2021-11-27 at 7 36 30 PM](https://media.git.generalassemb.ly/user/36937/files/524e8900-4fbb-11ec-9d9d-d7fa72a6b377)


## Bugs / Future Features
- Deleting Players can potentially break some match database entries - Needs attention!
- Add in set tracking
- Add in data visualization
