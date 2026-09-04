def check_ppe_compliance(detections):

    helmet = False
    vest = False
    mask = False

    for d in detections:

        label = d["label"].lower()

        if label == "helmet":
            helmet = True

        elif label == "vest":
            vest = True

        elif label == "mask":
            mask = True

    return {
        "helmet": helmet,
        "vest": vest,
        "mask": mask
    }