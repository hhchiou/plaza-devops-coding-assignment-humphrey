import os
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def hello():
    return {"message": os.environ.get('hello_message', 'Hello, World!')}


@app.get("/data")
def get_star_wars_data(num: int = 1):
    try:
        url = f"https://swapi.dev/api/people/{num}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail="API Error")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=500, detail="Data Processing Error")


# TODO: Add new endpoint to return the top 20 people in the Star Wars API with the highest BMI.


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
