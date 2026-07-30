This project has been created as part of the 42 curriculum by eloymart, juetxeba, martimar, anagomez, imugica-.

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
Juetxeba , Eloy 
# 3. Resources: 

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

 1. Database : PostgreSQL.
 
 PostgreSQL was chosen as the project’s database because it is reliable, open-source, and well suited for applications that require structured data and complex relationships. It provides strong data integrity, support for transactions, good performance, and advanced SQL features. Its compatibility with SQLModel and SQLAlchemy also allows it to integrate smoothly with the FastAPI backend, making the database layer easier to maintain and scale.

 
## 6.4 Other technology:

Docker, seguridad etc

# 7. Database Schema:

# 8. Features List:

# 9. Modules:

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

