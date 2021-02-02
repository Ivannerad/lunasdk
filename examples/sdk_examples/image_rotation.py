"""
Module realize simple examples following features:
    * image rotation
"""
import pprint

from resources import EXAMPLE_O

from lunavl.sdk.faceengine.engine import VLFaceEngine
from lunavl.sdk.image_utils.image import VLImage, RotationAngle


def rotateNEstimateImage():
    """
    Example of image rotation.
    """
    nonRotatedImage = VLImage.load(filename=EXAMPLE_O)
    faceEngine = VLFaceEngine()
    orientationModeEstimator = faceEngine.createOrientationModeEstimator()
    #: rotate & estimate | not rotated
    image = VLImage.rotate(nonRotatedImage, RotationAngle.ANGLE_0)
    pprint.pprint(orientationModeEstimator.estimate(image))
    #: rotate & estimate | left
    image = VLImage.rotate(nonRotatedImage, RotationAngle.ANGLE_90)
    pprint.pprint(orientationModeEstimator.estimate(image))
    #: rotate & estimate | right
    image = VLImage.rotate(nonRotatedImage, RotationAngle.ANGLE_270)
    pprint.pprint(orientationModeEstimator.estimate(image))
    #: rotate & estimate | upside down
    image = VLImage.rotate(nonRotatedImage, RotationAngle.ANGLE_180)
    pprint.pprint(orientationModeEstimator.estimate(image))


if __name__ == "__main__":
    rotateNEstimateImage()
