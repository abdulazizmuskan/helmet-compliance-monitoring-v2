import cv2


def draw_detections(image, detections):

    for d in detections:

        x1, y1, x2, y2 = d["bbox"]

        label = d["label"]

        conf = d["confidence"]

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            f"{label} {conf:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )

    return image