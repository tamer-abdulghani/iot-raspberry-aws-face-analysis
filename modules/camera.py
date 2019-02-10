import time


def capture_picture_from_raspberry(file_path):
    from picamera import PiCamera
    count = 3
    for i in range(count):
        print(count - i)
        time.sleep(1)
    with PiCamera() as camera:
        camera.vflip = True
        camera.hflip = True
        camera.capture(file_path)


def capture_picture_from_windows(file_path):
    import cv2

    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    time.sleep(0.1)
    return_value, image = camera.read()
    cv2.imwrite(file_path, image)
    del camera
