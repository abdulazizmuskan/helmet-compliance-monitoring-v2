from ultralytics import YOLO

# Load pre-trained classification model
model = YOLO("yolo11n-cls.pt")

# Train on your helmet dataset
model.train(
    data="helmet_dataset",
    epochs=10,
    imgsz=224
)

