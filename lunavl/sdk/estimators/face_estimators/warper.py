"""Module for creating warped images
"""
from typing import Union, Optional

from numpy.ma import array

from lunavl.sdk.faceengine.facedetector import FaceDetection, Landmarks68, Landmarks5
from lunavl.sdk.image_utils.image import VLImage
from FaceEngine import IWarperPtr, Transformation  # pylint: disable=E0611,E0401
from FaceEngine import Image as CoreImage  # pylint: disable=E0611,E0401


class WarpedImage(VLImage):
    """
    Raw warped image.

    Properties of a warped image:

        - its size is always 250x250 pixels
        - it's always in RGB color format
        - it always contains just a single face
        - the face is always centered and rotated so that imaginary line between the eyes is horizontal.
    """

    def __init__(self, body: Union[bytes, array, CoreImage], filename: str = "", vlImage=None):
        """
        Init.

        Args:
            body: body of image - bytes numpy array or core image
            filename: user mark a source of image
            vlImage: source is vl image.
        """
        if vlImage is None:
            super().__init__(body, filename=filename)
            self.assertWarp()
        else:
            self.source = vlImage.source
            self.filename = vlImage.filename
            self.coreImage = vlImage.coreImage

    def assertWarp(self):
        """
        Validate size and format

        Raises:
            ValueError("Bad image size for warped image"): if image has incorrect size
            ValueError("Bad image format for warped image, must be R8G8B8"): if image has incorrect format
        Warnings:
            this checks are not guarantee that image is warp. This function is intended for debug
        """
        if self.rect.size.height != 250 or self.rect.width != 250:
            raise ValueError("Bad image size for warped image")
        if self.format != self.format.R8G8B8:
            raise ValueError("Bad image format for warped image, must be R8G8B8")

    @classmethod
    def load(cls, *_, filename: Optional[str] = None, url: Optional[str] = None) -> 'WarpedImage':
        """
        Load imag from numpy array or file or url.

        Args:
            *_: for remove positional argument
            filename: filename
            url: url

        Returns:
            warp
        """
        warp = cls(vlImage=VLImage.load(filename=filename, url=url))
        warp.assertWarp()
        return warp

    @property
    def warpedImage(self) -> 'WarpedImage':
        """
        Property for compatibility with *Warp* for outside methods.
        Returns:
            self
        """
        return self


class Warp:
    """
    Structure for storing warp.

    Attributes:
        sourceDetection (FaceDetection): detection which generated warp
        warpedImage (WarpedImage):
    """
    __slots__ = ["sourceDetection", "warpedImage"]

    def __init__(self, warpedImage: WarpedImage, sourceDetection: FaceDetection):
        """
        Init.

        Args:
            warpedImage: warped image
            sourceDetection: detection which generated warp
        """
        self.sourceDetection = sourceDetection
        self.warpedImage = warpedImage


class Warper:
    """
    Class warper.

    Attributes:
        _coreWarper (IWarperPtr): core warper
    """
    __slots__ = ["_coreWarper"]

    def __init__(self, coreWarper: IWarperPtr):
        """
        Init.

        Args:
            coreWarper: core warper
        """
        self._coreWarper = coreWarper

    def _createWarpTransformation(self, faceDetection: FaceDetection) -> Transformation:
        """
        Create warp transformation.

        Args:
            faceDetection: face detection with landmarks5

        Returns:
            transformation
        Raises:
            ValueError: if detection does not contain a landmarks5
        """
        if faceDetection.landmarks5 is None:
            raise ValueError("detection must contains landmarks5")
        return self._coreWarper.createTransformation(faceDetection.coreEstimation.detection,
                                                     faceDetection.landmarks5.coreEstimation)

    def warp(self, faceDetection: FaceDetection) -> Warp:
        """
        Create warp from detection.

        Args:
            faceDetection: face detection with landmarks5

        Returns:
            Warp
        """
        transformation = self._createWarpTransformation(faceDetection)
        warpResult = self._coreWarper.warp(faceDetection.image.coreImage, transformation)
        if warpResult[0].isError:
            raise ValueError("1234567")

        warpedImage = WarpedImage(body=warpResult[1], filename=faceDetection.image.filename)

        return Warp(warpedImage, faceDetection)

    def makeWarpTransformationWithLandmarks(self, faceDetection: FaceDetection,
                                            typeLandmarks: str) -> Union[Landmarks68, Landmarks5]:
        """
        Make warp transformation with landmarks

        Args:
            faceDetection: face detection  with landmarks5
            typeLandmarks: landmarks for warping ("L68" or "L5")

        Returns:
            warping landmarks
        Raises:
            ValueError: if landmarks5 is not estimated
        """
        transformation = self._createWarpTransformation(faceDetection)
        if typeLandmarks == "L68":
            warpResult = self._coreWarper.warp(faceDetection.landmarks68.coreEstimation, transformation)
        elif typeLandmarks == "L5":
            warpResult = self._coreWarper.warp(faceDetection.landmarks5.coreEstimation, transformation)
        else:
            raise ValueError("Invalid value of typeLandmarks, must be 'L68' or 'L5'")
        if warpResult[0].isError:
            raise ValueError("1234567")
        if typeLandmarks == "L68":
            return Landmarks68(warpResult[1])
        return Landmarks5(warpResult[1])