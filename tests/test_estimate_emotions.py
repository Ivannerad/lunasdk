import unittest
from typing import Optional

from lunavl.sdk.faceengine.setting_provider import DetectorType
from lunavl.sdk.image_utils.image import VLImage
from tests.base import BaseTestClass
from tests.resources import EMOTION_FACES, ALL_EMOTIONS

EMOTION_IMAGES = {emotion: VLImage.load(filename=imagePath) for emotion, imagePath in EMOTION_FACES.items()}


class TestEstimateEmotions(BaseTestClass):
    """
    Test estimate emotions.
    """

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.detector = cls.faceEngine.createFaceDetector(DetectorType.FACE_DET_DEFAULT)
        cls.warper = cls.faceEngine.createFaceWarper()
        cls.emotionEstimator = cls.faceEngine.createEmotionEstimator()

    def assert_emotion_reply(self, emotionDetection: dict, predominantEmotion: Optional[str] = None) -> None:
        """
        Assert emotions dict
        Args:
            emotionDetection: dict with predominant and all emotions
            predominantEmotion: expected predominant emotion
        """
        self.validate_emotion_dict(emotionDetection)
        if predominantEmotion is not None:
            assert emotionDetection["predominant_emotion"] == predominantEmotion

    @staticmethod
    def validate_emotion_dict(receivedDict: dict):
        """
        Validate emotion dict
        """
        assert {"predominant_emotion", "estimations"} == receivedDict.keys()
        assert set(ALL_EMOTIONS) == receivedDict["estimations"].keys()
        for emotion, emotionValue in receivedDict["estimations"].items():
            assert 0 <= emotionValue <= 1

    def test_estimate_emotions_as_dict(self):
        """
        Test emotion estimator 'asDict' method
        """
        for emotion in ALL_EMOTIONS:
            with self.subTest(image_emotion=emotion):
                faceDetection = self.detector.detectOne(EMOTION_IMAGES[emotion])
                warp = self.warper.warp(faceDetection)
                emotionDict = self.emotionEstimator.estimate(warp.warpedImage).asDict()
                self.validate_emotion_dict(emotionDict)

    @unittest.skip("Unstable")
    def test_estimate_emotions(self):
        """
        Test all emotions estimations
        """
        for emotion in ALL_EMOTIONS:
            with self.subTest(emotiodetectselfn=emotion):
                faceDetection = self.detector.detectOne(EMOTION_IMAGES[emotion])
                warp = self.warper.warp(faceDetection)
                emotionDict = self.emotionEstimator.estimate(warp.warpedImage).asDict()
                self.assert_emotion_reply(emotionDict, emotion)
