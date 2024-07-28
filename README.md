# Grow Mood

Backend Services for Grow Mood Application. This backend services use Firebase Admin for Auth and OpenAI API for training our personalized prompt.

## The Flow of Our Backend Application:
We have 2 recommendation system:
- /recommendation -> more reliable but slower
- /recommendation2 -> Faster but uses only a limited database as preknowledge.

### /recommendation
1. We train the OpenAI API with the embeddings model using our knowledge base consisting of 5000 cleaned datasets from:
- https://www.kaggle.com/datasets/graphquest/restaurant-menu-items
2. We use prompt engineering techniques to generate recommendations from OpenAI using our context. The context is enhanced with the help of the Faiss library, which uses similarity search to get the top-10 recommendations.
3. After receiving the result from OpenAI, we process it to get the full data matching the documents in Firestore. We focus only on important data when prompting OpenAI to prevent rate limiting.

### /recommendation2
1. We train OpenAI using a limited dataset from Firestore (up to 20 entries).
2. We use prompt engineering techniques to generate recommendations based on these limited data.

API Required Body:
- mood: "very unpleasant", "unpleasant", "neutral", "pleasant", "very pleasant"
- description: Based on previous answers in the widget. For example, if the user chooses "pleasant", there will be a "calm" option.

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

### Add Embedding Models
1. Download [Embedding Models](https://drive.google.com/file/d/19LeB2J_bw2mpVns_H4tp6XrXogdTelMB/view?usp=sharing)
2. Move the json data into `app/data`

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
docker compose up -d --build
```

This will build and start the containers defined in the `docker-compose.yml` file.

### Access the Application

Your application will be available at `http://127.0.0.1:8000`.

### Stopping the Application

To stop the application, run:

```bash
docker compose down
```