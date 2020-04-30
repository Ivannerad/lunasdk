"""Module for creating warped images
"""
from typing import Union, Optional

from FaceEngine import IHumanWarperPtr  # pylint: disable=E0611,E0401
from FaceEngine import Image as CoreImage  # pylint: disable=E0611,E0401
from PIL.Image import Image as PilImage

from lunavl.sdk.detectors.humandetector import HumanDetection
from lunavl.sdk.errors.errors import LunaVLError
from lunavl.sdk.errors.exceptions import LunaSDKException, CoreExceptionWrap
from lunavl.sdk.image_utils.image import VLImage, ColorFormat


class HumanWarpedImage(VLImage):
    """
    Raw warped image.

    Properties of a warped image:

        - it's always in RGB color format
        - it always contains just a single face
        - the face is always centered and rotated so that imaginary line between the eyes is horizontal.
    """

    def __init__(
        self,
        body: Union[bytes, bytearray, PilImage, CoreImage, VLImage],
        filename: str = "",
        colorFormat: Optional[ColorFormat] = None,
    ):
        """
        Init.

        Args:
            body: body of image - bytes/bytearray or core image or pil image or vlImage
            filename: user mark a source of image
            colorFormat: output image color format
        """
        if isinstance(body, VLImage):
            self.source = body.source
            self.filename = body.filename
            self.coreImage = body.coreImage
        else:
            super().__init__(body, filename=filename, colorFormat=colorFormat)
        self.assertWarp()

    def assertWarp(self):
        """
        Validate size and format

        Raises:
            ValueError("Bad image format for warped image, must be R8G8B8"): if image has incorrect format
        Warnings:
            this checks are not guarantee that image is warp. This function is intended for debug
        """
        if self.format != self.format.R8G8B8:
            raise ValueError("Bad image format for warped image, must be R8G8B8")

    #  pylint: disable=W0221
    @classmethod
    def load(cls, *, filename: Optional[str] = None, url: Optional[str] = None) -> "HumanWarpedImage":  # type: ignore
        """
        Load imag from numpy array or file or url.

        Args:
            filename: filename
            url: url

        Returns:
            warp
        """
        warp = cls(body=VLImage.load(filename=filename, url=url), filename=filename or "")
        warp.assertWarp()
        return warp

    @property
    def warpedImage(self) -> "HumanWarpedImage":
        """
        Property for compatibility with *Warp* for outside methods.
        Returns:
            self
        """
        return self


class HumanWarp:
    """
    Structure for storing warp.

    Attributes:
        sourceDetection (HumanDetection): detection which generated warp
        warpedImage (FaceWarpedImage):
    """

    __slots__ = ["sourceDetection", "warpedImage"]

    def __init__(self, warpedImage: HumanWarpedImage, sourceDetection: HumanDetection):
        """
        Init.

        Args:
            warpedImage: warped image
            sourceDetection: detection which generated warp
        """
        self.sourceDetection = sourceDetection
        self.warpedImage = warpedImage


class HumanWarper:
    """
    Class warper.

    Attributes:
        _coreWarper (IWarperPtr): core warper
    """

    __slots__ = ["_coreWarper"]

    def __init__(self, coreWarper: IHumanWarperPtr):
        """
        Init.

        Args:
            coreWarper: core warper
        """
        self._coreWarper = coreWarper

    @CoreExceptionWrap(LunaVLError.CreationWarpError)
    def warp(self, humanDetection: HumanDetection) -> HumanWarp:
        """
        Create warp from detection.

        Args:
            humanDetection: face detection with landmarks5

        Returns:
            Warp
        Raises:
            LunaSDKException: if creation failed
        """
        error, warp = self._coreWarper.warp(humanDetection.coreEstimation)
        if error.isError:
            raise LunaSDKException(LunaVLError.fromSDKError(error))

        warpedImage = HumanWarpedImage(body=warp, filename=humanDetection.image.filename)

        return HumanWarp(warpedImage, humanDetection)