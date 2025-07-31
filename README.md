# Music Sales Dashboard

A fullstack dashboard app that visualizes music sales data using **FastAPI (backend)** and **Next.js with TailwindCSS (frontend)**. It shows which genres are selling and which aren’t, and allows authenticated access to deeper insights.

---

## 📁 Project Structure

```
Adaire-Assessment/
│
├── backend/         # FastAPI app
│   ├── main.py
│   ├── database/  # SQLite database
│   │     ├── db.py
│   │     └── ...
│   └── ...
│
└── frontend/        # React + Tailwind dashboard
    ├── page.tsx
    ├── components/
    │   ├── GenreSummaryTable.tsx
    │   └── UnsoldGenreTable.tsx
    └── ...
```

---

## IMPORTANT:

To run smoothly, please run the backend server first before starting the frontend. The frontend relies on the backend API for data.

Do not perform the operations below to prepare the backend and frontend from the root directory.
Instead, open the `backend` and `frontend` directories in separate windows of your code editor.

---

## 🚀 Backend (FastAPI + SQLite)

### 🔧 Setup Instructions

1. **Clone the repo and enter the backend folder**

```bash
git clone https://github.com/PJ2623/Adaire-Assessment.git
cd Adaire-Assessment/backend
```

2. **Install [uv](https://github.com/astral-sh/uv)** if not already installed

```bash
pip install uv
```

3. **Set up virtual environment and install dependencies**
```bash
uv venv # Create a virtual environment 
uv pip compile pyproject.toml -o requirements.txt
uv pip install -r requirements.txt
.venv\Scripts\activate  # Activate the virtual environment
```

Once everything is installed, close and reopen your terminal to activate the virtual environment.

4. **Start the server**

```bash
uvicorn main:app --reload
```

Server is live at: `http://localhost:8000`

---

### 🔐 Authentication

To access protected routes, you must authenticate first.

**Login Endpoint**

The endpoint does not use the password though it asks for it. As employee records do not have a password, you can use any password.
It simply fetches th user by email and if a record is found it returns a JWT token. This done just for this demonstration.

```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=john.doe&email=john.doe%40example.com&password=your_password
```

Response:

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

Use the token as:

```
Authorization: Bearer your_jwt_token
```

---

### 📊 API Endpoints

| Method | Endpoint              | Description                          |
| ------ | --------------------- | ------------------------------------ |
| POST   | `/login`              | Get JWT token                        |
| GET    | `/total-genre`        | Get total number of genres sold      |
| GET    | `/recent-sale`        | Get the most recent sale             |
| GET    | `/genre-sale-summary` | Get summary of sales by genre (auth) |
| GET    | `/not-sold`           | Get list of unsold genres            |

---

## Frontend (Next.js + TailwindCSS)

### Setup Instructions

1. **Navigate to frontend directory**

```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run the dev server**
```bash
npm run dev
```

The app will be live at: `http://localhost:3000`

---

### How It Works

* When the dashboard loads:

  1. It logs in via `/login` using stored credentials.
  2. The access token is saved and used to fetch protected genre summary data.
  3. It fetches:

     * `/total-genre`
     * `/recent-sale`
     * `/not-sold`
     * `/genre-sale-summary` (with auth)
  4. The data is displayed in 2 grid-style tables.

* **TailwindCSS** is used for simple spacing, grid layouts, and clean typography.

---

> Built by Patrick Mateus
