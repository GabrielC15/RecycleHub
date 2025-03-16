## Inspiration
RecycleHub was born from the need for sustainable waste management solutions in small communities, high school students, artist. Many small towns struggle with efficiently recycling materials, and we saw an opportunity to empower residents by turning recyclable waste into economic value. Our goal is to transform waste into a community resource by facilitating the exchange, donation, and sale of recyclable items.

## What it does
RecycleHub is a web-based platform that:
- **Lists Recyclable Items:** Users can post items they wish to sell, donate, or exchange.
- **Enables Image Uploads:** Users can attach images to their listings for better clarity.
- **Filters & Sorts:** Users can filter listings based on material type and recycling action (e.g., buy, sell, donate).
- **Secures User Data:** Includes secure user authentication with signup and login functionality.
- **Promotes Community Engagement:** Fosters a local recycling economy to promote sustainable practices.

## How we built it
### Backend:
- **Flask:** Our primary web framework to build a RESTful API.
- **Flask-SQLAlchemy:** An ORM for database operations (using SQLite by default, with a plan for PostgreSQL).
- **Flask-JWT-Extended:** For JWT-based user authentication.
- **Flask-CORS:** To enable cross-origin resource sharing between the backend and the frontend.
- **Werkzeug:** For secure password hashing and file upload handling.
- **SQLite:** Our initial database for storing users and listings.

### Frontend:
- **React:** Used for building a responsive and interactive user interface.
- **Axios/Fetch API:** For making HTTP requests to our backend API.

## Challenges we ran into
- **Authentication Setup:** Debugging JWT token issues, such as ensuring the token subject is a string.
- **File Uploads:** Integrating and securing image uploads, and validating file types.
- **CORS Configuration:** Enabling smooth communication between our frontend (localhost:3000) and backend (localhost:5000).
- **Database Schema Updates:** Managing migrations as we evolved our data models.

## Accomplishments that we're proud of
- **Robust Authentication:** We successfully implemented secure user authentication using JWT.
- **Feature-Rich API:** Our API supports CRUD operations, image uploads, filtering, and sorting.
- **Community Impact:** Built a solution that addresses real sustainability challenges in small communities.

## What we learned

## What's next for RecycleHub
