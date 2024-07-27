# Grow Mood

Backend Services for Grow Mood Application

## Local Setup

### Prerequisites

- Python 3.12.4
- pip
- virtualenv

### Clone the Repository

```bash
git clone https://github.com/zuhalal/grow_mood_be
cd grow_mood_be
```

### Create and Activate Virtual Environment

```bash
# Create virtual environment
py -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate

# On Unix or MacOS
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Add Firebase Service Account

Add service account for firebase admin with name `firebase-config.json` in the root directory

### Run the Application

```bash
uvicorn app.main:app --reload
```

Your application will be available at `http://127.0.0.1:8000`.

## Deployment with Docker Compose

### Prerequisites

- Docker
- Docker Compose

### Clone the Repository

```bash
git clone https://github.com/zuhalal/grow_mood_be
cd grow_mood_be
```

### Set Up Environment Variables

Create a `.env` file in the root directory of your project and add the necessary environment variables.

```bash
cp .env.example .env
# Edit .env to add your environment variables
```

### Add Firebase Service Account

Add service account for firebase project with name `firebase-config.json` in the root directory

### Build and Run with Docker Compose

```bash
docker-compose up -d --build
```

This will build and start the containers defined in the `docker-compose.yml` file.

### Access the Application

Your application will be available at `http://127.0.0.1:8000`.

### Stopping the Application

To stop the application, run:

```bash
docker-compose down
```