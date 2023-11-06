import cv2
import mediapipe as mp
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('pose landmarker result: {}'.format(result))
    annotated_image = draw_landmarks_on_image(imgRGB, result)
    image_result = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    cv2.imshow("frame", image_result)
    cv2.waitKey(1)

def draw_landmarks_on_image(rgb_image, detection_result):
  pose_landmarks_list = detection_result.pose_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected poses to visualize.
  for idx in range(len(pose_landmarks_list)):
    pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      pose_landmarks_proto,
      solutions.pose.POSE_CONNECTIONS,
      solutions.drawing_styles.get_default_pose_landmarks_style())
  return annotated_image

# def draw_landmarks_on_image(rgb_image, detection_result):
#     face_landmarks_list = detection_result.face_landmarks
#     annotated_image = np.copy(rgb_image)
#     for idx in range(len(face_landmarks_list)):
#         face_landmarks = face_landmarks_list[idx]
#         face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
#         face_landmarks_proto.landmark.extend([
#           landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
#         ])
#         solutions.drawing_utils.draw_landmarks(
#             image=annotated_image,
#             landmark_list=face_landmarks_proto,
#             connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp.solutions.drawing_styles
#             .get_default_face_mesh_tesselation_style())
#         solutions.drawing_utils.draw_landmarks(
#             image=annotated_image,
#             landmark_list=face_landmarks_proto,
#             connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
#             landmark_drawing_spec=None,
#             connection_drawing_spec=mp.solutions.drawing_styles
#             .get_default_face_mesh_contours_style())
#         solutions.drawing_utils.draw_landmarks(
#             image=annotated_image,
#             landmark_list=face_landmarks_proto,
#             connections=mp.solutions.face_mesh.FACEMESH_IRISES,
#               landmark_drawing_spec=None,
#               connection_drawing_spec=mp.solutions.drawing_styles
#               .get_default_face_mesh_iris_connections_style())
#     return annotated_image


options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='pose_landmarker_lite.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

i = 0

with PoseLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0)
    while True:
        succes, img = cap.read()
        i += 1
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        landmarker.detect_async(mp_image, i)
        print(i)