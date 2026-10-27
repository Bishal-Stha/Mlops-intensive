import pickle
import pandas as pd

# import the ml model
with open('model/model.pkl','rb') as f:
    model = pickle.load(f)

#MLFlow
MODEL_VERSION = '1.0.0'

# Get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(userinput: dict):

    df = pd.DataFrame([userinput])

    # predict the class
    predict_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    # create mapping {class_name: probability}
    class_probs = dict(zip(class_labels, map(lambda p: round(p,4), probabilities)))

    return {
        "predicted_category": predict_class,
        "confidence": confidence,
        "class_probabilities": class_probs
    }