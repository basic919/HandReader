def predict_number(model, image):
    if image:
        return model.predict(image)
    return -1
