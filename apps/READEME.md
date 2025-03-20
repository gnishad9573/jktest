**Overview**

This project provides a FastAPI application with interactive API documentation.



**Prerequisites**

    Ensure you have the following installed:

    Python 3.9+

    pip (Python package manager)

    Virtual environment (optional but recommended)


**Installation**
    1: Clone the repository:
        git clone <repo-url>
        cd <project-directory>
    
    2: Create a virtual environment (optional but recommended):
        python -m venv venv
        source venv/bin/activate
    
    3: Install dependencies:
        pip install -r requirements.txt


**Running the FastAPI Application**

    To start the FastAPI server, run:
            `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`


`Accessing API Documentation`

    Once the server is running, visit:

    Swagger UI: http://127.0.0.1:8000/docs


`Environment Variables`

    You can configure environment variables using a .env file:

   ** changes below variables **
        POSTGRES_USER=`your_db_username`
        POSTGRES_PASSWORD=`your_db_password`
        POSTGRES_PORT=5432
        POSTGRES_SERVER=localhost
        POSTGRES_DB=bookstore
        POSTGRES_URL_DB=postg
        
**Run UnitTest** 
    PYTHONPATH=. pytest -v


Play With SWAGGER UI :
    http://127.0.0.1:8000/docs

    1: Create user 
    2: authenticate user 
    3: add books


Step 1: Install Ollama
install Ollama using:
`brew install ollama`

Step 2: Start the Ollama Server
To run the Ollama model, you need to start the Ollama server. Use the following command:
`ollama serve`
    





