"""
Credibility check estimation example
"""
import pprint

from lunavl.sdk.faceengine.engine import VLFaceEngine
from lunavl.sdk.faceengine.setting_provider import DetectorType
from lunavl.sdk.image_utils.image import VLImage
from resources import EXAMPLE_1


def estimateCredibilityCheck():
    """
    Create warp to detection.
    """
    image = VLImage.load(filename=EXAMPLE_1)
    faceEngine = VLFaceEngine()
    detector = faceEngine.createFaceDetector(DetectorType.FACE_DET_V1)
    faceDetection = detector.detectOne(image)
    warper = faceEngine.createFaceWarper()
    warp = warper.warp(faceDetection)

    credibilityCheckEstimator = faceEngine.createCredibilityCheckEstimator()
    pprint.pprint(credibilityCheckEstimator.estimate(warp.warpedImage).asDict())


if __name__ == "__main__":
    estimateCredibilityCheck()
