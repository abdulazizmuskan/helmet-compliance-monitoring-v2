import cv2


class PPEDetector:

    def __init__(self, model):
        self.model = model

    def detect(self, image):

        results = self.model(image)

        detections = []

        for result in results:

            boxes = result.boxes

            for box in boxes:

                cls_id = int(box.cls[0])
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                label = result.names[cls_id]

                detections.append({
                    "label": label,
                    "confidence": conf,
                    "bbox": [x1, y1, x2, y2]
                })

        return detections