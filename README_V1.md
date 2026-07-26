This project has been created as part of the 42 curriculum by eloymart, juetxeba, martimar, anagomez, imugica-.

# 1. Description:
 Martimar 
# 2. Instructions: 
Juetxeba , Eloy 
# 3. Resources: 
# 4. Team Information: 

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
