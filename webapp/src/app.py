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


@app.get("/top-people-by-bmi")
def get_top_people_by_bmi():
    try:
        url = "https://swapi.dev/api/people"
        people = []
        while True:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            for person in data["results"]:
                if "unknown" == person["mass"] or \
                   "unknown" == person["height"]:
                    # print(person["name"], person["url"], "unknown m/h")
                    continue
                mass = float(person["mass"].replace(',', ''))
                height = float(person["height"].replace(',', '')) / 100
                bmi = mass / (height * height)
                person["bmi"] = bmi
                people.append(person)
            url = data["next"]
            if url is None:
                break
        sorted_people = sorted(people, key=lambda x: x["bmi"], reverse=True)
        top_people = sorted_people[:20]
        return top_people
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail="API Error")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=500, detail="Data Processing Error")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
