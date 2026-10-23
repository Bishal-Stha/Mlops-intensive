from fastapi import FastAPI, Path, HTTPException, Query 
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
app = FastAPI()

# class Patient(BaseModel):
#     name: str
#     age: int
#     email: EmailStr
#     allergies: Optional[List[str]] = None
#     married: Optional[bool] = False
#     contact_detail: Dict[str,str]
#     linkedin_url = AnyUrl

# patient_info = {"name":"Bishal Shrestha","age": 20,"email":"bishal@gmail.com","contact_detail":{"email_address":"bishal@gmail.com","phone":"9876543210"},"linkedin_url":"https://linkedin.com/in/bishal-ml"}

# patient01 = Patient(**patient_info)
# print(patient01)

class Patient(BaseModel):
    id: Annotated[str, Field(...,description="ID of the patient",examples=["P001"])]
    name: Annotated[str,Field(...,description="Name of the patient")]
    city: Annotated[str, Field(description="Name of city")]
    age: Annotated[int, Field(description="Age of the patient", gt=0, lt=120)]
    gender: Annotated[Literal['male','female','others'], Field(...,description="Gender of the patient")]
    height: Annotated[float, Field(...,gt=0, description="Height of patient in meters")]
    weight: Annotated[float, Field(...,gt=0, description= "Weight of Patient in KG.")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height **2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

def load_data():
    with open("patients.json") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data,f)

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
def view_patient(patient_id: str = Path(...,description="ID of the patient in the Database.", examples="P001")):
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
def wordcount(word: str = Path(...,description="Enter a word or sentence or text and i will return you word count.",examples="an apple a day keeps the doctor away.")):
    words = word.split(" ")
    word_length = len(words)
    return {"word": word  ,"word-length": word_length}

@app.post("/create")
def create(patient: Patient):

    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        # raise ValueError("Patient Already Exists.")
        raise HTTPException(status_code=400, detail="Patient already exists.")

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=["id"])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content= {"message": "Patient created successfully."})