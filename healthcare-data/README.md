# Healthcare Information Chatbot

## Course Information

CS410: Text Information Systems Project

## Project Overview

This project implements a search system that helps users find appropriate over-the-counter medications based on their symptoms. The system uses the OpenFDA API and vector similarity search to provide evidence-based medication recommendations.

TODO:

- [ ] Add additional API sources, if needed
- [ ] Create LLM-powered chatbot features
- [ ] Add evaluation metrics

## Features

- Symptom-based medication search
- Real-time drug information from OpenFDA
- Vector similarity search with caching
- Natural language query processing
- Evidence-based recommendations

## Prerequisites

- Python 3.8+
- PostgreSQL 14+ with vector extension
- pip (Python package manager)
- OpenFDA API key (get one at https://open.fda.gov/apis/authentication/)

## Installation

### 1. Install PostgreSQL 14

#### macOS

Using Homebrew:

```bash
brew install postgresql@14
brew services start postgresql@14
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql-14 postgresql-contrib-14
sudo systemctl start postgresql
```

#### Windows

- Download PostgreSQL 14 installer from https://www.postgresql.org/download/windows/
- Run the installer and follow the setup wizard
- Remember the password you set for the postgres user

### 2. Install PostgreSQL Vector Extension

#### macOS

```bash
brew install postgresql@14
psql postgres -c 'CREATE EXTENSION vector;'
```

#### Linux

```bash
sudo apt-get install postgresql-14-vector
```

#### Windows

Vector extension is included in PostgreSQL 14+ installation.

### 3. Create Database (if needed)

Connect to PostgreSQL and create the database:

```bash
# macOS/Linux
psql postgres
```

```bash
# Windows
"C:\Program Files\PostgreSQL\14\bin\psql.exe" -U postgres
```

Then create the database:

```sql
CREATE DATABASE medical_db;
\q
```

### 4. Clone and Setup Project

1. Clone the repository:

```bash
git clone https://github.com/justthea/CS410-Healthcare-Assistant-Chatbot.git
cd CS410-Healthcare-Assistant-Chatbot/healthcare-data
```

2. Create a virtual environment:

```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env`:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_db
DB_USER=postgres           # default PostgreSQL user
DB_PASSWORD=your_password  # password you set during installation
FDA_API_KEY=your_api_key  # from OpenFDA
```

5. Run setup script:

```bash
python src/scripts/setup.py
```

## Usage

### Interactive Mode

Start the interactive chat interface:

```bash
python src/interactive.py
```

### Example Mode

Run example queries:

```bash
python src/main.py
```

## Troubleshooting

### PostgreSQL Issues

1. If PostgreSQL service isn't running:

```bash
# macOS
brew services restart postgresql@14

# Linux
sudo systemctl restart postgresql

# Windows
net stop postgresql-x64-14
net start postgresql-x64-14
```

2. If you can't connect to PostgreSQL:

```bash
# Check if PostgreSQL is running
# macOS/Linux
ps aux | grep postgres

# Windows
tasklist | findstr postgres
```

3. If vector extension isn't available:

```sql
-- In psql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Database Access Issues

1. Reset PostgreSQL password:

```bash
# macOS/Linux
psql postgres
\password postgres

# Windows
"C:\Program Files\PostgreSQL\14\bin\psql.exe" -U postgres
\password postgres
```

2. Grant database access:

```sql
GRANT ALL PRIVILEGES ON DATABASE medical_db TO postgres;
```

## Project Structure

```
.
├── src/
│   ├── data/
│   │   ├── fda_client.py    # OpenFDA API client
│   │   └── vector_db.py     # Vector similarity search
│   ├── scripts/
│   │   └── setup.py         # Database and extension setup
│   ├── interactive.py       # Interactive chat interface
│   └── main.py             # Example queries runner
├── .env                    # Configuration
└── README.md              # Documentation
```

## Disclaimer

This system is for informational purposes only. Always consult with a healthcare professional before taking any medication.
