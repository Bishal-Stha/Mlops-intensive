from fastapi import FastAPI, Path, HTTPException, Query
import json
app = FastAPI()

def load_data():
    with open("patients.json") as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records."}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(...,description="ID of the patient in the Database.", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    
    # return {"error": "patient not found."}
    raise HTTPException(status_code=404, detail="patient not found")

@app.get("/sort")
def sort(sortby: str = Query(...,description="Sort on the basis of height, weight or bmi"), order: str = Query("asc",description="Sort in asc or desc.")):
    valid_fields = ["height","weight","bmi"]

    if sortby not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select from {valid_fields}")

    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400, detail="Invalid field. Select asc or desc.")

    data = load_data()

    sort_order = True if order == 'desc' else False  # noqa: SIM210

    sorted_data = sorted(data.values(), key = lambda x: x.get(sortby,0), reverse=sort_order)

    return sorted_data

@app.get("/wordcount/{word}")
def wordcount(word: str = Path(...,description="Enter a word or sentence or text and i will return you word count.",example="an apple a day keeps the doctor away.")):
    words = word.split(" ")
    word_length = len(words)
    return {"word": word  ,"word-length": word_length}