This project has been created as part of the 42 curriculum by *eloymart, juetxeba, martimar, anagomez, imugica-*.

# 1. Description

## King of the Sleep

**King of the Sleep** is a competitive web application that transforms users' real sleep data into the performance of an avatar in an automatic battle game.

The main goal of the project is to encourage users to improve their sleep habits through competition, progression and social interaction. Instead of displaying sleep information only through traditional statistics, the application uses sleep metrics as gameplay attributes that directly affect the results of each battle.

Each competition day takes place between 10:00 and 23:00. During this period, up to 100 users can participate in the same arena. Battles are organised automatically throughout the day, and the performance of each player is calculated using sleep-related metrics such as sleep duration, sleep efficiency, sleep consistency, REM sleep and deep sleep.

After every battle round, the application updates the player rankings, statistics and protocol results. This allows users to understand how their sleep habits influence their performance and compare their progress with other players.

The application includes the following key features:

- Secure user registration and JWT-based authentication.
- User profiles with avatars, levels, experience and achievements.
- A competitive automatic battle system based on sleep data.
- A shared arena (lobby) with multiple active users.
- A challenge mode to dare a rival from the lobby.
- Sleep score tracking and graphical data visualisation.
- Sleep protocol tracking and comparison.
- Real-time dashboard updates using WebSockets.
- Private and global chat systems.
- Friends management and online-status information.
- An administration panel for managing users and battle schedules.
- A secured public API that allows users to access and manage their own data.
- A guided onboarding experience that explains the dashboard and the main game mechanics.
- A responsive interface designed for desktop and mobile devices.

The project combines health tracking, gamification, social interaction and real-time web technologies to create a different approach to sleep improvement. Rather than treating sleep as an isolated personal metric, King of the Sleep turns it into a shared competitive experience.

# 2. Instructions:
Follow the steps below to set up the project using the repository's `Makefile`.

> **Note:** All `make` commands must be executed from the root of the repository, where the `Makefile` is located.

1. Create the secrets by running:

   ```bash
   make init-secrets
   ```

   This command creates a `secrets/` directory containing three files that must be configured by the user:
   - postgres_user
   - postgres_password
   - secret_key

2. Edit each file inside the `secrets/` directory and provide the corresponding values.

3. Create the environment file by running:

   ```bash
   make env
   ```

   This command creates a `.env` file by copying `.env.example`.

   > **Note:** The generated file contains default values. It is strongly recommended to review and modify these values before continuing.

4. Build the Docker images and start the application containers by running:

   ```bash
   make prod-up-build
   ```

5. Populate the application with initial data by running:

   ```bash
   make populate
   ```

6. Open the application's landing page in your default web browser by running (linux only):

   ```bash
   make open-https
   ```

7. When your browser displays a security warning because of the self-signed SSL certificate, accept the risk and continue to access the application.

# 3. Resources:

These are real references and official documentation links for the technologies used in this project:

## Frontend
- Vue 3 documentation: https://vuejs.org/guide/introduction.html
- Vite documentation: https://vite.dev/guide/
- Pinia documentation: https://pinia.vuejs.org/
- Tailwind CSS documentation: https://tailwindcss.com/docs/installation
- Axios documentation: https://axios-http.com/docs/intro
- Phaser 3 documentation: https://phaser.io/docs/3.80.0/index

## Backend and data
- FastAPI documentation: https://fastapi.tiangolo.com/
- SQLModel documentation: https://sqlmodel.tiangolo.com/
- PostgreSQL documentation: https://www.postgresql.org/docs/
- PyJWT documentation: https://pyjwt.readthedocs.io/en/stable/

## Infrastructure and real-time
- Docker Compose documentation: https://docs.docker.com/compose/
- Caddy documentation: https://caddyserver.com/docs/
- MDN WebSockets API: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
- Coraza WAF: https://www.coraza.io/docs/tutorials/introduction/
- OWASP Core Ruleset: https://coreruleset.org/docs/1-getting-started/1-1-crs-installation/
# 4. Team Information

All team members participated as developers while also taking responsibility for specific product, management and technical areas.

| Team member | Assigned role(s) | Main responsibilities |
|---|---|---|
| **eloymart** | Technical Lead and Developer | Led major technical and architectural decisions, including the selection of the main frameworks and the overall application architecture. Worked across the frontend, backend and database, and implemented authentication, WebSockets, the public API, the administration panel, the friends system and several database operations. |
| **juetxeba** | Technical Lead, Project Manager and Developer | Coordinated the weekly planning process, task assignment and progress tracking. As a Technical Lead, focused mainly on infrastructure, Docker, containers, backend development and database integration. |
| **martimar** | Product Owner and Developer | Defined the product vision, game concept, page structure, visual direction and main mechanics after researching games with similar concepts. Created and maintained product design documentation, including the service blueprint, the screen-by-screen interaction flow and the description of the game's objectives and features. Also developed most of the frontend and user experience. |
| **anagomez** | Developer | Focused mainly on the game implementation, including game logic, game-related WebSocket communication and the two-player gameplay experience. |
| **imugica-** | Developer | Focused mainly on the game implementation, including game logic, game-related WebSocket communication and the two-player gameplay experience. |

## Role Distribution

### Product Owner — martimar

The Product Owner was responsible for defining and maintaining the product vision and ensuring that the different parts of the application formed a coherent user experience.

The main Product Owner responsibilities included:

- Researching other games and products with similar concepts.
- Defining the structure of the application and its main pages.
- Establishing the visual direction and overall user experience.
- Defining the game mechanics and how sleep data affects player performance.
- Describing the main objectives and features of the game.
- Creating a service blueprint to represent how the product should work across the different stages of the user experience.
- Creating a screen-by-screen interaction flow showing where each action or button leads.
- Helping prioritise features and review whether implemented functionality matched the intended product concept.

### Project Manager — juetxeba

The Project Manager was responsible for coordinating the team, organising the work and monitoring progress throughout the project.

The main Project Manager responsibilities included:

- Maintaining a weekly task list.
- Assigning a responsible team member to each task.
- Monitoring completed, pending and blocked tasks.
- Organising weekly progress meetings.
- Coordinating shorter meetings when urgent problems or important decisions appeared.
- Helping adjust the scope and priorities when required.
- Ensuring that relevant decisions and progress updates were communicated to the whole team.

### Technical Leads — eloymart and juetxeba

The Technical Leads were responsible for the main technical decisions and for ensuring that the frontend, backend, database and infrastructure worked together correctly.

**eloymart** focused on the overall software architecture and the selection of the principal frameworks and technologies. He worked across the frontend, backend and database and supported the integration of the application's main systems.

**juetxeba** focused mainly on infrastructure and deployment, including Docker, containers, backend development and database integration. He also contributed to technical coordination and project-wide implementation decisions.

### Developers — all team members

All five team members participated as developers. Each member implemented assigned functionality, tested and debugged their work, contributed to integration and documented their own areas.

The development work was broadly distributed as follows:

- **eloymart:** frontend, backend, authentication, general WebSockets, public API, administration, friends system and database operations.
- **juetxeba:** Docker, containers, infrastructure, backend and database.
- **martimar:** product definition, frontend, dashboard, user experience, responsive design, data visualisation and onboarding.
- **anagomez:** game development, game-related WebSockets and two-player gameplay.
- **imugica-:** game development, game-related WebSockets and two-player gameplay.

# 5. Project Management: 
The project has been divided into several areas, with each area assigned to a specific group. Once the responsibilities are defined, the work is broken down into smaller tasks. These tasks are organised in a timeline that allows us to monitor progress on a weekly basis.

We hold a weekly meeting to review whether the objectives of the current sprint have been completed, identify any remaining tasks and update the rest of the team on our progress. During these meetings, each group explains what they have completed, the problems they have encountered and which parts of the project may require changes or improvements.

Although the main meetings take place once a week, shorter meetings are arranged whenever an urgent problem needs to be solved, an important decision must be made or the scope of the project needs to be reviewed and adjusted.

We also maintain a public record of identified bugs and suggested improvements. This helps the entire team keep track of known issues, proposed changes and pending work.

For source-code management, we use GitHub and a branch-based workflow. A separate branch is created for each project area, feature or bug fix. To reduce conflicts and avoid overlapping changes, merges into the main branch are ideally handled by one designated team member. After each merge, all team members are asked to pull the latest version of the project and verify that everything continues to work correctly.

For sharing ideas, diagrams, tables, concepts and other resources, we use Miro. This platform provides a shared workspace where the team can upload and organise different types of content, including presentations, images, documents and text. The Miro board is reviewed before major updates so that the whole team has access to the latest information and decisions.
# 6. Technical Stack:

## 6.1 Frontend:

 1. Framework Interface : Vue JS. 
 2. Framework Style: Tailwind CSS. 
 3. Libary Graphs: Chart JS.
 4. Library Game: Phaser JS.
 5. Library Store: Pinia.
 6. Library HTTP client: Axios.
 7. Library Userguide: Driver JS.
 8. Library Formatter: Prettier.
 9. Server: Caddy.
 
We chose Vue.js as the foundation of the frontend because of its simplicity, performance, and compatibility with a wide range of libraries. Its built-in reactivity system and component-based architecture make it especially suitable for a project of this size, allowing us to create an efficient, organised, and maintainable interface. Using JavaScript on the frontend also gives us direct access to its extensive ecosystem, making it easier to install and integrate the additional libraries required by the project.

Tailwind CSS was selected because of its straightforward utility-first approach and gentle learning curve. It allows us to build and modify the interface quickly without maintaining large custom CSS files. In addition, its mobile-first responsive design system helps us create a consistent user experience across different screen sizes and devices. For global state management, we use Pinia, the official state-management solution for Vue. Its close integration with the framework allows us to manage authentication tokens, user information, and other shared application states in a centralised way, improving code organisation and making the application easier to maintain and debug.

## 6.2 Backend:

 1. Framework: FastAPI.
 2. ORM: SQModel (Pydantic + SQLAlchemy).
 3. Server: Uvicorn.
 4. Library JWT: Pyjwt.

For the backend, we chose FastAPI together with Uvicorn. FastAPI provides a modern, high-performance framework for building APIs in Python, with built-in support for asynchronous operations, automatic data validation, type annotations, and interactive API documentation. Uvicorn is used as the ASGI server because it is lightweight, fast, and designed to run asynchronous Python applications efficiently. This combination simplifies both development and deployment while allowing the backend to handle multiple simultaneous requests effectively.

SQLModel was selected as the project’s ORM because it provides a simple, type-safe, and maintainable way to interact with the database through Python classes and objects. It is built on top of SQLAlchemy and Pydantic, combining SQLAlchemy’s database capabilities with Pydantic’s validation and type system. SQLModel integrates naturally with FastAPI and is fully compatible with PostgreSQL through SQLAlchemy’s PostgreSQL drivers. It also reduces duplicated code by allowing the same models to be used for database tables, data validation, and API schemas, making the backend easier to organise, maintain, and debug.

## 6.3 Database:

### 1. Database : PostgreSQL.
 
 PostgreSQL was chosen as the project’s database because it is reliable, open-source, and well suited for applications that require structured data and complex relationships. It provides strong data integrity, support for transactions, good performance, and advanced SQL features. Its compatibility with SQLModel and SQLAlchemy also allows it to integrate smoothly with the FastAPI backend, making the database layer easier to maintain and scale.

 
## 6.4 Other technology:

### 1. Docker and Docker Compose

Docker was chosen because the team already had prior experience with it, making it a good opportunity to further develop our expertise. In addition, Docker is an industry standard with extensive community support and documentation. It provides an efficient way to develop, deploy, and connect multiple services across different environments, making it well suited for a microservice-based architecture such as ours.

### 2. Caddy

Caddy was chosen because it is a modern web server written in Go that emphasizes simplicity and ease of configuration. It provides automatic HTTPS support, straightforward deployment, and requires minimal configuration compared to many alternatives.

Another advantage of Caddy is its plugin system, which allows developers to easily extend its functionality. In this project, the Coraza Web Application Firewall (WAF) plugin was integrated to improve the security of the application's endpoints by providing protection against common web attacks.

# 7. Database Schema:
![Image of Schema DB.](/KOTS_DB_SCHEMA.jpeg)

# 8. Features List:

The following table summarises the features implemented in the final application, the team members who worked on each one and their main functionality. When a feature involved several layers of the project, all principal contributors are listed.

| Implemented feature | Team member(s) | Functionality |
|---|---|---|
| **User registration and login** | **eloymart** | Allows users to create an account and log in through the Vue interface. The FastAPI backend validates the submitted data, hashes passwords and issues JWT bearer tokens for authenticated requests. |
| **Authentication state and protected routes** | **eloymart** | Stores the authenticated session in the Pinia store, attaches the bearer token to API requests and prevents unauthenticated users from opening protected frontend views. |
| **Profile management** | **eloymart, martimar** | Lets users view and update their account information, change their email or password and manage their profile from the dashboard interface. |
| **Profile avatar uploads** | **eloymart, martimar** | Allows users to upload a personal image, stores the avatar on the backend and displays it in profiles, rankings and other dashboard sections. |
| **Sleep-data entry** | **eloymart, martimar** | Provides a form for recording daily sleep metrics such as time in bed, sleep phases, disturbances, performance, consistency and efficiency. The submitted data is stored in PostgreSQL and used by the dashboard and game systems. |
| **Centralised dashboard data loading** | **eloymart, martimar, juetxeba** | Retrieves the information required by the dashboard in a central request and distributes it to its components, reducing duplicated requests and keeping the displayed data consistent. |
| **Weekly sleep-score visualisation** | **martimar, eloymart** | Displays recent sleep performance in a Chart.js graph, including daily values, current results and comparisons across the week. |
| **Player ranking and Elo progression** | **eloymart, martimar, juetxeba** | Builds a leaderboard from the latest player scores and shows ranking position, Elo points, position changes, avatar and experience. |
| **Sleep protocols** | **juetxeba, eloymart, martimar** | Lets users select the protocols followed during the day and displays their estimated impact. It also calculates global protocol usage and win-rate rankings. |
| **Today's statistics and battle history** | **juetxeba, martimar, eloymart** | Shows daily wins and losses and provides a detailed history of scheduled battles, including opponents, result, avatars, protocols and sleep statistics. |
| **Experience, levels and achievements** | **martimar, eloymart, juetxeba** | Rewards participation with experience points, calculates the user's level and displays progression and achievement badges in the profile and ranking interfaces. |
| **Real-time WebSocket connection system** | **eloymart, anagomez, imugica-** | Authenticates connected users and carries presence updates, chats, lobby movement, battle events, reconnection state and dashboard-refresh notifications in real time. |
| **Private chat** | **eloymart** | Enables direct real-time messages between two users and organises them into individual conversations with unread-message indicators. |
| **Global chat** | **eloymart** | Provides a shared real-time chat room in which all connected users can communicate. |
| **Friends and online presence** | **eloymart** | Allows users to add or remove friends, view their friend list, see who is currently online and open related social interactions. |
| **Multiplayer lobby** | **anagomez, imugica-** | Places connected players in a shared Phaser arena, represents each user with a character and synchronises movement and disconnection events between clients. |
| **Player-to-player challenges** | **anagomez, eloymart, imugica-** | Lets a player challenge another connected user from the lobby. The recipient can accept or decline, after which the server starts or cancels the battle flow. |
| **Real-time combat system** | **imugica-, anagomez** | Runs two-player battles using health, attack, defence and attack-speed statistics derived from sleep data. The server validates attacks and synchronises damage and health updates between both players. |
| **Combat animations, audio and visual effects** | **imugica-** | Adds character animations, health and attack-progress bars, sound effects, hit particles, death animations, victory effects, battle backgrounds and scene transitions to the Phaser game. |
| **Battle reconnection and resume** | **imugica-** | Pauses an active battle when a player disconnects and restores the player, current health and battle state when they reconnect. |
| **Automatic matchmaking and scheduled battles** | **anagomez, juetxeba, imugica-** | Matches users who submitted sleep data, calculates combat results from their real metrics, records scheduled battles and allows the battle interval or extra battles to be managed. |
| **Administrator panel and permissions** | **eloymart, juetxeba** | Provides administrator-only user management, including viewing, editing, activating, deactivating and deleting accounts, as well as controls for battle scheduling. Admin accounts can be created through a Makefile command. |
| **API-key management** | **eloymart** | Allows authenticated users to generate named API keys, view their prefixes and usage information, and revoke keys that are no longer required. |
| **Secured public sleep-data API** | **eloymart** | Exposes five API-key-protected operations for listing, retrieving, creating, updating and deleting only the sleep records owned by the API-key holder. |
| **Public API documentation and playground** | **eloymart** | Documents the available endpoints, headers and payloads and provides an interactive page where users can generate a key and test public API requests. |
| **Guided onboarding and dashboard tour** | **martimar, eloymart** | Introduces new users to the dashboard through a welcome flow and Driver.js tour, using demonstration data to explain rankings, battles, sleep scores and protocols. |
| **Landing page, navigation and legal pages** | **martimar, eloymart** | Provides the public landing experience, application navigation, login and registration entry points, and dedicated privacy-policy and terms-of-use pages. |
| **Responsive desktop and mobile interface** | **martimar** | Adapts the landing page, dashboard, forms, dialogs, navigation and game-related interfaces for different screen sizes and supported browsers. |
| **PostgreSQL data model and ORM integration** | **juetxeba, eloymart** | Stores users, profiles, friendships, sleep entries, protocols, rankings, API keys and combat history through SQLModel relationships and backend queries. |
| **Initial data and administration utilities** | **juetxeba, eloymart** | Provides commands and scripts for creating an administrator, populating development data, seeding protocol records and preparing the application for testing. |
| **Docker-based development and production environments** | **juetxeba** | Packages PostgreSQL, FastAPI, Vue and Caddy as connected services and provides separate development and production configurations. |
| **Makefile workflow** | **juetxeba** | Supplies simplified commands for environment preparation, builds, startup, shutdown, logs, database operations, population, administrator creation and browser access. |
| **Caddy reverse proxy and application protection** | **juetxeba** | Routes frontend, REST API and WebSocket traffic, provides HTTPS for the configured environment and integrates rate limiting, Coraza WAF rules and Docker-managed secrets. |

# 9. Modules:

## 1. Use a framework for both the frontend and backend (Major - All)
We used different frameworks for the project: Vue.js for the frontend and Tailwind CSS for styling, while the backend is built with FastAPI.

## 2. Implement real-time features using WebSockets or similar technology. (Major - eloymart, imugica-, anagomez)
We used WebSockets throughout the project for several core features:
- Global chat, allowing users to communicate with everyone.
- Private chat, enabling one-to-one conversations.
- Chat notifications, indicating unread messages.
- Dashboard updates, triggering refreshes when new data is available.
- The lobby, where online users can be seen in real time and challenged to battles.
- The game itself, synchronizing combat actions and states.
- The online user list, showing which users are currently connected.

## 3. Allow users to interact with other users (Major - eloymart, martimar)
Users can interact with one another through private and group chats, add or remove friends, and view each other’s connection status. They can also access another user’s profile, statistics, and relevant sleep information when they have battled that person. To access these features, users can click on a player in the ranking.

## 4. A public API to interact with the database with a secured API key, rate limiting, documentation, and at least 5 endpoints (Major - eloymart)
We built a public API that allows users to create API keys to view, update, or delete their own data. After logging in, users can access /public_api to generate a unique API key, give it a name, and manage it. The same page also includes an API playground where users can test the endpoints in real time. The API provides five different endpoints (PATCH, PUT, DELETE, and GET) and its documentation is available at /api_docs.

## 5. Use an ORM for the database (Minor - eloymart, juetxeba)
We use SQLModel as our ORM, combining Pydantic and SQLAlchemy to provide a simple and expressive way to manage the database.

## 6. Support for additional browsers (Minor - All)
The project has been tested in multiple browsers, including Brave, Mozilla Firefox, Safari, and Google Chrome.

## 7. Standard user management and authentication (Major - eloymart)
Users can update their profile information, such as email and password, and upload an avatar to the server through the profile settings page. The friends system also lets them see each other’s online status and receive chat notifications when a friend is online.

## 8. Game statistics and match history (Major - All)
The app includes a complete statistics system. From the dashboard, users can view rankings, wins and losses, level, Elo, and match history. Scheduled battles (excluding lobby battles) are stored and can be reviewed in detail from the “See all” section in the Today Stats module. Achievements linked to experience are visible on the dashboard above the level bar, and ranking positions and progress changes can be consulted at any time.

## 9. Advanced permissions system (Major - eloymart)
By default, all users are regular users. A user can create an admin account with the make admin command, which prints the admin username and password in the console. After logging in, the admin can access /admin, where they can manage users through a full CRUD interface. This view is only available to administrators. The admin panel can also be used to schedule extra battles for debugging and testing purposes.

## 10. User activity analytics and insights dashboard (Minor - martimar)
Users can access their recorded activity data, including their daily sleep entries, and review analytics and progress across different areas such as sleep protocol impact, combat history, and experience-based achievements.

## 11. Implement a complete web-based game where users can play against each other (Major - anagomez, imugica-)
The game is composed of several areas:
- The lobby, where online users can see one another in real time and challenge each other to battles.
- Real-time combat, where users are matched based on the statistics generated that day and fight synchronously in an autobattle experience.
- Backend-scheduled battles, where automated battles are generated regularly in the backend so the game continues to evolve even when users are not directly interacting with the frontend.

## 12. Remote players (Major - anagomez, imugica-)
The lobby and gameplay are fully online and synchronized. Presence and game state are managed in real time, allowing users to connect and reconnect smoothly from different locations.

## 13. A gamification system to reward users for their actions (Minor - martimar)
The app includes achievements, complete leaderboards, experience points, levels, and a visual progression system in the user profile that reflects progress after each battle round.

## 14. Optional module, development utils (Minor - juetxeba)
This module focuses on making the development workspace easier to use, building on the project's existing integrations to streamline the development process. A Makefile system lets developers interact with the container setup without needing to run Docker commands directly. The developer build supports live reloading (FastAPI's --reload flag on the backend and Vite on the frontend) so changes appear immediately without rebuilding images, thanks to a shared volume system. The Makefile also includes populate and admin commands for generating test data.

The main challenges were designing a system usable without prior knowledge of containers, and doing so while accounting for Python's learning curve. Overall, this module supports manual testing and a smoother development workflow.

# 10. Individual Contributions:

## 10.1 Eloymart

1.  **Initial Setup:** I installed and tested Vue.js and established its initial connection with FastAPI. I also contributed to the design and architectural decisions of the application.
    
2.  **Login and Registration:** I implemented the complete JWT-based authentication system across both the frontend and backend. This includes user registration, login, token storage and authentication checks.
    
3.  **WebSockets:** I implemented WebSocket communication for several modules of the project. This includes authentication when the application starts, real-time dashboard updates through broadcasts to all connected users, private and global chat systems, and connection and disconnection management.
    
4.  **Public API:** I developed a public API key system and its corresponding documentation. Users can generate an API key and use it to securely access, update or delete their own data through the public API endpoints.
    
5.  **Admin View:** I developed an administration panel with CRUD functionality for managing users. Administrators can view, edit and delete user accounts, as well as manage and update the battle scheduling system.
    
6.  **Friends System:** I implemented the friends system, allowing users to add and remove friends, view their current online status and access related social features within the application.
    
7.  **Database Integration:** I also contributed to the implementation of database operations and queries. This included retrieving, creating, updating and deleting data, connecting backend endpoints to the database and helping ensure that the information returned by the API was handled correctly.

The main challenge was adapting to Vue and its reactive system, as I had previously worked with other frameworks that manage state and component updates differently.

One of the most significant technical difficulties involved managing the dashboard state. The dashboard needs to be updated whenever a battle takes place, while ensuring that all users see the latest information without constantly sending unnecessary requests to the server.

To solve this, we designed a WebSocket-based notification system. When a battle occurs, the server sends a message to the frontend indicating that the dashboard data must be refreshed. The frontend then performs a new request to retrieve the updated information.

We also implemented a centralised data hydration system. Instead of allowing every dashboard subcomponent to make its own separate request, a single request retrieves all the necessary data and distributes it among the different subcomponents. This approach reduces duplicated requests, improves performance and keeps the dashboard state consistent across the application.

## 10.2 Martimar

1. **Product Ownership and Research:** I acted as the Product Owner of King of the Sleep. I researched games and digital products with similar concepts in order to define the structure of the application, its visual direction, its main mechanics and the way users would interact with the product.

2. **Product Definition:** I defined the main concept of King of the Sleep and translated it into a complete product experience. This included establishing the objective of the game, its main features, how sleep data affects player performance and how the daily competition should work.

3. **Service Blueprint and User Flow:** I created a service blueprint describing how the product should operate across the different stages of the user experience. I also documented the application screen by screen, showing what happens when users interact with each button and where every action leads.

4. **Frontend Design and Architecture:** I designed and implemented most of the frontend using Vue.js and Tailwind CSS. I helped establish the visual identity of the application, including its colour system, typography, reusable card layouts, spacing and responsive behaviour.

5. **Dashboard Interface:** I developed and integrated several dashboard components, including  today's statistics, player rankings, protocol rankings, user profile, sleep score graph and protocol-impact sections. I also worked on the distribution of dashboard data between these components.

6. **Data Visualisation:** I implemented graphical and numerical representations of sleep data using Chart.js. This included the weekly sleep-score graph, latest-score calculations, average-score calculations and score comparisons between different days.

7. **Guided Dashboard Tour:** I implemented the onboarding and user-guide system using Driver.js. The tour introduces users to the main dashboard sections and explains how battles, rankings, sleep statistics and protocols work. I also integrated the tour with the authentication and routing flow so that it is displayed to new users.

8. **Responsive Design:** I adapted the application interface for different screen sizes. This included restructuring the dashboard for mobile devices, correcting overflowing elements, adapting the sleep form and ensuring that navigation and interactive components remained usable on smaller screens.

9. **Demo and Tutorial Data:** I implemented demonstration data for the dashboard tour. This ensures that rankings, statistics, protocols, sleep scores and other dashboard sections contain meaningful information while the application is being introduced to a new user.

10. **Frontend Debugging and Integration:** I worked on resolving frontend problems related to Vue reactivity, component properties, conditional rendering, list keys, responsive layouts and interactions between dialogs, routes and the Driver.js tour. I also helped integrate frontend components with the data structures provided by the backend.

One of the main product challenges was transforming sleep data into a game experience that was understandable and engaging. The service blueprint, game-definition document and screen-by-screen interaction flow helped us clarify the product logic before and during implementation.

One of the main technical challenges was creating a dashboard with many independent components while keeping the information consistent and avoiding duplicated logic. Several components depend on the same dashboard response, and changes in one part of the application can affect rankings, statistics, profiles and protocol information at the same time.

To address this, the dashboard data was centralised and distributed to the different components through properties and computed values. This made the components easier to maintain and reduced unnecessary requests and duplicated state.

## 10.3 imugica-

My main contribution to the project was the design and implementation of the complete **real-time combat system**, together with the **game artwork and visual presentation**.

Although the multiplayer lobby and player movement were primarily developed by another team member, I was responsible for everything that happens once a battle starts and some parts prior to it.

1. **Combat System:**

I designed and implemented the complete combat system using **Phaser.js**, creating the entire battle flow from the moment a fight begins until a winner is declared. The combat mechanics include player statistics such as health, attack, defense, and attack speed, together with an attack system that handles damage calculation, health reduction, and attack cooldowns.

To improve the gameplay experience, I implemented synchronized health and attack progress bars, victory and defeat screens, sound effects, character animations, and several visual effects including hit particles, death animations, jewel rain during victory, and scene transition effects. I also implemented the automatic cleanup of battle resources once a fight has finished.

2. **Multiplayer Synchronization:**

I implemented the real-time combat synchronization using **WebSockets**, ensuring that both players always share the same battle state. The combat system follows a **server-authoritative** model, where all attacks and damage calculations are validated on the backend to prevent cheating or inconsistent game states.

The synchronization system keeps both clients updated with attacks, damage, health changes, battle start events, and battle completion, while preventing invalid or excessively frequent attacks through server-side validation.

3. **Reconnection System:**

A significant part of my contribution was developing the reconnection system for ongoing battles. When a player disconnects, the battle is automatically paused until they reconnect.

Upon reconnection, the player is returned directly to the battle with their latest combat state restored, including their current health and battle statistics. The system resumes gameplay seamlessly by restoring the battle state and synchronizing both players before combat continues.

4. **Art and Visual Design:**

I also created and integrated the game's visual assets, including character animations, backgrounds, user interface elements, icons, particle textures, combat effects, and scene transitions.

These assets were integrated into Phaser to provide a cohesive and polished visual experience during battles, complementing the gameplay mechanics with responsive animations and effects.

## 10.4 anagomez

1. **Multiplayer lobby:** Through the already built web-socket I stablished the communication bewteen the online user's avatars in order for them to be able to explore the lobby and meet in real time. Every player has their own avatar, represented by a sheep. The sheep's movements are shared with every online user, they then represent said movement with a slight tilt as a moving indicator.

2. **Between users challenges:** Users preent in the loobby are able to challenge eachother and start a battle, which pulls their real data from the server and begins a new battle bewteen them. Challenged users are also able to decline a battle.

3. **Matchmaking:** Other than the manual challenging, the server pairs up the users with data entries of the day and compares them in order to build up a ranking for the day based on real data.

4. **Mathematical model:** The comparisons are completely objective, based on different mathematical equations with real data entered by the user.

The main challenge was the communication through web socket, as I had never used them before.

## 10.5 Juetxeba

1. **Architecture Design and Implementation:** Designed and implemented the Docker-based microservice architecture, integrating the Database (PostgreSQL), Backend (FastAPI), Frontend (Vue), and Server (Caddy), while configuring the required communication between all services.

2. **Development Utilities:** Designed and implemented multiple `Makefile` commands that abstracted the complexity of the development environment, minimizing the interaction required from team members and simplifying development, debugging, and deployment tasks.

3. **Database Design:** Contributed to the design and implementation of the database schema, including tables, relationships, and data organization.

4. **Backend Development:** Developed and optimized multiple API endpoints with a focus on reducing unnecessary traffic between the backend and the database. Also contributed to data generation systems and restructured the backend project organization.

5. **Security:** Integrated a Web Application Firewall (WAF) into the Caddy server and implemented Docker secrets for sensitive information such as the application secret key, database username, and database password.

6. **Production Deployment:** Developed an environment management system that allows users to prepare either the development or production environment using simple `Makefile` commands.

7. **Frontend Development:** Connected backend endpoints to several frontend components and proposed optimizations that reduced unnecessary database requests.

8. **Project Management:** Coordinated the team's work throughout the project, maintaining an organized development workflow and ensuring clear communication of objectives, especially during high-pressure stages of development.

One of the main challenges arose at the beginning of the project when the technology stack was still being defined and the final project requirements were uncertain. The architecture therefore needed to be flexible enough to accommodate future features without requiring structural changes.

To address this, I designed a modular Docker architecture based on shared volumes. This approach allowed the backend and frontend containers to share the project files while automatically reloading whenever changes were made, providing a reactive development environment for all team members. Additionally, the frontend dependencies (`node_modules`) were also managed through shared volumes, allowing new packages to be installed without rebuilding the container, significantly improving the development workflow and making the architecture scalable as the project evolved.
