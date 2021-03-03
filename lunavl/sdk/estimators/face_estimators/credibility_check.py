"""
Module for estimate a credibility check from warped image.
"""
from typing import Union, Dict, Any

from FaceEngine import ICredibilityCheckEstimatorPtr
from FaceEngine import CredibilityCheckEstimation

from lunavl.sdk.errors.errors import LunaVLError
from lunavl.sdk.errors.exceptions import CoreExceptionWrap, LunaSDKException
from ..base import BaseEstimator
from ..face_estimators.facewarper import FaceWarp, FaceWarpedImage
from ...base import BaseEstimation


class CredibilityCheck(BaseEstimation):
    """
    Structure credibility check

    Estimation properties:

        - credibility_check
    """

    @property
    def credibilityCheck(self) -> float:
        """
        The credibility check

        Returns:
            float in range(0, 1)
        """
        return self._coreEstimation.value

    def asDict(self) -> Dict[str, float]:
        """
        Convert to dict.

        Returns:
            self.credibilityCheck
        }
        """
        return {"credibility_check": self.credibilityCheck}


class CredibilityCheckEstimator(BaseEstimator):
    """
    Warp credibility check estimator.
    """

    @CoreExceptionWrap(LunaVLError.CredibilityCheckError)
    def estimate(self, warp: Union[FaceWarp, FaceWarpedImage]) -> CredibilityCheck:
        """
        Estimate credibility check from a warp.

        Args:
            warp: raw warped image or warp

        Returns:
            estimated credibility check
        Raises:
            LunaSDKException: if estimation failed
        """
        error, credibilityCheck = self._coreEstimator.estimate(warp.warpedImage.coreImage)
        if error.isError:
            raise LunaSDKException(LunaVLError.fromSDKError(error))
        return CredibilityCheck(credibilityCheck)
