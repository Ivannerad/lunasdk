"""
SDK configuration module.
"""
import os
from enum import Enum
from pathlib import Path
from typing import Union, Optional, Tuple, Any, TypeVar, Type

import FaceEngine as CoreFE
from FaceEngine import ObjectDetectorClassType, PyISettingsProvider  # pylint: disable=E0611,E0401

BI_ENUM = TypeVar("BI_ENUM", bound="BiDirectionEnum")


class BiDirectionEnum(Enum):
    """
    Bi direction enum.
    """

    @classmethod
    def getEnum(cls: Type[BI_ENUM], enumValue: Union[int, str]) -> BI_ENUM:
        """
        Get enum by value.

        Args:
            enumValue: value

        Returns:
           element of the enum with value which is equal to the enumValue.
        Raises:
              KeyError: if element not found.
        """
        for enumMember in cls:
            if enumMember.value == enumValue:
                return enumMember
        raise KeyError("Enum {} does not contain  member with value {}".format(cls.__name__, enumValue))


class CpuClass(Enum):
    """Class of cpu by supported instructions"""

    auto = "auto"
    sse4 = "sse4"
    avx = "avx"
    avx2 = "avx2"
    arm = "arm"


class VerboseLogging(BiDirectionEnum):
    """
    Level of log versobing enum
    """

    error = 0
    warnings = 1
    info = 2
    debug = 3


class DeviceClass(Enum):
    """
    Device enum
    """

    cpu = "cpu"
    gpu = "gpu"


class Distance(BiDirectionEnum):
    """
    Descriptor distance type enum.
    """

    l1 = "L1"
    l2 = "L2"


class NMS(Enum):
    """
    NMS type enum.
    """

    mean = "mean"
    best = "best"


class Point4:
    """
    Point in 4-dimensional space.
    Attributes:
        x (float): x coordinate
        y (float): y coordinate
        z (float): z coordinate
        w (float): w coordinate
    """

    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def asTuple(self) -> Tuple[float, float, float, float]:
        """
        Convert point to tuple.

        Returns:
            tuple from coordinate
        """
        return self.x, self.y, self.z, self.w


class Point3:
    """
    Point in 3-dimensional space.
    Attributes:
        x (float): x coordinate
        y (float): y coordinate
        z (float): z coordinate
    """

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def asTuple(self) -> Tuple[float, float, float]:
        """
        Convert point to tuple.

        Returns:
            tuple from coordinate
        """
        return self.x, self.y, self.z


class Point2:
    """
    Point in 2-dimensional space.
    Attributes:
        x (float): x coordinate
        y (float): y coordinate
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def asTuple(self) -> Tuple[float, float]:
        """
        Convert point to tuple.

        Returns:
            tuple from coordinate
        """
        return self.x, self.y


class DetectorType(BiDirectionEnum):
    """
    Detector types enum
    """

    FACE_DET_DEFAULT = "Default"
    FACE_DET_V1 = "FaceDetV1"  #: todo description
    FACE_DET_V2 = "FaceDetV2"
    FACE_DET_V3 = "FaceDetV3"

    @property
    def coreDetectorType(self) -> ObjectDetectorClassType:
        """
        Convert  self to core detector type

        Returns:
            ObjectDetectorClassType
        """
        mapEnumToCoreEnum = {
            "Default": "FACE_DET_DEFAULT",
            "FaceDetV1": "FACE_DET_V1",
            "FaceDetV2": "FACE_DET_V2",
            "FaceDetV3": "FACE_DET_V3",
        }
        return getattr(ObjectDetectorClassType, mapEnumToCoreEnum[self.value])


class BaseSettingsSection:
    """
    Base class for a section of settings.

    Proxy model to core settings provider.

    Attributes:
        _coreSettingProvider (PyISettingsProvider): core settings faceEngineProvider
    """

    # (str): section name
    sectionName: str

    def __init__(self, coreSettingProvider: PyISettingsProvider):
        self._coreSettingProvider = coreSettingProvider

    def setValue(self, name: str, value: Any) -> None:
        """
        Set a value

        Args:
            name: setting name
            value: new value
        """
        self._coreSettingProvider.setValue(self.__class__.sectionName, name, CoreFE.SettingsProviderValue(value))

    def getValue(self, name: str) -> Any:
        """
        Get setting value
        Args:
            name: setting name

        Returns:
            a value
        """
        return self._coreSettingProvider.getValue(self.__class__.sectionName, name)

    def getValueAsString(self, name: str) -> str:
        """
        Get setting value as string
        Args:
            name: setting name

        Returns:
            a string
        """
        return self.getValue(name).asString()

    def getValueAsInt(self, name: str) -> int:
        """
        Get setting value as int
        Args:
            name: setting name

        Returns:
            a int
        """
        return self.getValue(name)[0]

    def getValueAsFloat(self, name: str) -> float:
        """
        Get setting value as float
        Args:
            name: setting name

        Returns:
            a float
        """
        return self.getValue(name).asFloat()


class SystemSettings(BaseSettingsSection):
    """
    Common system settings.

    Properties:
        - verboseLogging (VerboseLogging): Level of log verbosing
        - betaMode (bool): enable experimental features.
        - defaultDetectorType (DetectorType): default detector type
    """

    sectionName = "system"

    @property
    def verboseLogging(self) -> VerboseLogging:
        """
        Getter for verboseLogging

        Returns:
            verboseLogging
        """
        return VerboseLogging.getEnum(self.getValueAsInt("verboseLogging"))

    @verboseLogging.setter
    def verboseLogging(self, value: VerboseLogging) -> None:
        """
        Setter for cpuClass.

        Args:
            value: new value
        """
        self.setValue("verboseLogging", value.value)

    @property
    def betaMode(self) -> bool:
        """
        Getter for betaMode

        Returns:
            betaMode
        """
        return bool(self.getValueAsInt("betaMode"))

    @betaMode.setter
    def betaMode(self, value: bool) -> None:
        """
        Setter for betaMode
        Args:
            value: new value
        """
        self.setValue("betaMode", int(value))

    @property
    def defaultDetectorType(self) -> DetectorType:
        """
        Getter for defaultDetectorType

        Returns:
            betaMode
        """
        return DetectorType.getEnum(self.getValueAsString("defaultDetectorType"))

    @defaultDetectorType.setter
    def defaultDetectorType(self, value: DetectorType) -> None:
        """
        Setter for defaultDetectorType
        Args:
                value: new value
        """
        self.setValue("defaultDetectorType", value.value)


class RuntimeSettings(BaseSettingsSection):
    """
    Flower library is the default neural network inference engine.
    The library is used for:

        - face detectors;
        - estimators(attributes, quality);
        - face descriptors

    Properties:
        cpuClass (CpuClass): class of cpu by supported instructions
        deviceClass (DeviceClass):  execution device type cpu, gpu.
        numThreads (int): number of worker threads.
        verboseLogging (VerboseLogging): level of verbose logging
        numComputeStreams (int):  increases performance, but works only with new versions of nvidia drivers
    """

    sectionName = "Runtime"

    @property
    def deviceClass(self) -> DeviceClass:
        """
        Get device class.

        Returns:
            device class
        """

        return DeviceClass[self.getValueAsString("deviceClass")]

    @deviceClass.setter
    def deviceClass(self, value: DeviceClass) -> None:
        """
        Setter for deviceClass
        Args:
            value: new value
        """
        self.setValue("deviceClass", value.value)

    @property
    def cpuClass(self) -> CpuClass:
        """
        Getter for cpuClass

        Returns:
            cpuClass
        """
        return CpuClass[self.getValueAsString("cpuClass")]

    @cpuClass.setter
    def cpuClass(self, value: CpuClass) -> None:
        """
        Setter for cpuClass.

        Args:
            value: new value
        """
        self.setValue("cpuClass", value.value)

    @property
    def numThreads(self) -> int:
        """
        Getter for numThreads

        Returns:
            numThreads
        """
        return self.getValueAsInt("numThreads")

    @numThreads.setter
    def numThreads(self, value: int) -> None:
        """
        Setter for numThreads
        Args:
            value: new value
        """
        self.setValue("numThreads", value)

    @property
    def verboseLogging(self) -> VerboseLogging:
        """
        Getter for verboseLogging

        Returns:
            verboseLogging
        """
        return VerboseLogging.getEnum(self.getValueAsInt("verboseLogging"))

    @verboseLogging.setter
    def verboseLogging(self, value: VerboseLogging) -> None:
        """
        Setter for verboseLogging
        Args:
            value: new value
        """
        self.setValue("verboseLogging", value.value)

    @property
    def numComputeStreams(self) -> int:
        """
        Getter for numComputeStreams

        Returns:
            numComputeStreams
        """
        return self.getValueAsInt("numComputeStreams")

    @numComputeStreams.setter
    def numComputeStreams(self, value: int) -> None:
        """
        Setter for numComputeStreams
        Args:
            value: new value
        """
        self.setValue("numComputeStreams", value)


class DescriptorFactorySettings(BaseSettingsSection):
    """
    Descriptor factory settings.

    Properties:

        - model (int): CNN face descriptor version.
        - UseMobileNet (bool): mobile Net is faster but less accurate
        - distance (Distance): distance between descriptors on matching. L1 faster,L2 make better precision.
        - descriptorCountWarningLevel (float): Threshold,that limits the ratio of created  descriptors to the amount,
            defined by your liscence. Warning Level When the threshold is exceeded, FSDK prints the warning.

    """

    sectionName = "DescriptorFactory::Settings"

    @property
    def model(self) -> int:
        """
        Getter for model

        Returns:
            model
        """
        return self.getValueAsInt("model")

    @model.setter
    def model(self, value: int) -> None:
        """
        Setter for model
        Args:
            value: new value
        """
        self.setValue("model", value)

    @property
    def useMobileNet(self) -> bool:
        """
        Getter for useMobileNet

        Returns:
            useMobileNet
        """
        return bool(self.getValueAsInt("useMobileNet"))

    @useMobileNet.setter
    def useMobileNet(self, value: bool) -> None:
        """
        Setter for useMobileNet
        Args:
            value: new value
        """
        self.setValue("useMobileNet", int(value))

    @property
    def distance(self) -> Distance:
        """
        Getter for distance

        Returns:
            distance
        """
        return Distance.getEnum(self.getValueAsString("distance"))

    @distance.setter
    def distance(self, value: Distance) -> None:
        """
        Setter for distance
        Args:
            value: new value
        """
        self.setValue("distance", value.value)

    @property
    def descriptorCountWarningLevel(self) -> str:
        """
        Getter for descriptorCountWarningLevel

        Returns:
            descriptorCountWarningLevel
        """
        return self.getValueAsString("descriptorCountWarningLevel")

    @descriptorCountWarningLevel.setter
    def descriptorCountWarningLevel(self, value: str) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("descriptorCountWarningLevel", value)


class FaceDetV3Settings(BaseSettingsSection):
    """
    FaceDetV3 detector settings.

    Properties:

        - scoreThreshold (float): detection threshold in [0..1] range;
        - redetectScoreThreshold (float): redetect face threshold in [0..1] range;
        - NMSThreshold (float): overlap threshold for NMS [0..1] range;
        - minFaceSize (int): Minimum face size in pixels;
        - maxFaceSize (int): Maximum face size in pixels;
        - nms (NMS): type of NMS: mean or best;
        - redetectTensorSize (int): target face after preprocessing for redetect;
        - redetectFaceTargetSize (int): target face size for redetect;
        - paddings (Point4): paddings;
        - paddingsIR (Point4): paddingsIR;
        - planPrefix (str): planPrefix;
        - useOrientationMode (bool): use mode for rotated origin images or not;
    """

    sectionName = "FaceDetV3::Settings"

    @property
    def scoreThreshold(self) -> float:
        """
        Getter for scoreThreshold

        Returns:
            scoreThreshold
        """
        return self.getValueAsFloat("scoreThreshold")

    @scoreThreshold.setter
    def scoreThreshold(self, value: float) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("ScoreThreshold", value)

    @property
    def redetectScoreThreshold(self) -> float:
        """
        Getter for redetectScoreThreshold

        Returns:
            redetectScoreThreshold
        """
        return self.getValueAsFloat("RedetectScoreThreshold")

    @redetectScoreThreshold.setter
    def redetectScoreThreshold(self, value: float) -> None:
        """
        Setter for redetectScoreThreshold
        Args:
            value: new value
        """
        self.setValue("RedetectScoreThreshold", value)

    @property
    def NMSThreshold(self) -> float:
        """
        Getter for NMSThreshold

        Returns:
            NMSThreshold
        """
        return self.getValueAsFloat("NMSThreshold")

    @NMSThreshold.setter
    def NMSThreshold(self, value: float) -> None:
        """
        Setter for NMSThreshold
        Args:
            value: new value
        """
        self.setValue("NMSThreshold", value)

    @property
    def minFaceSize(self) -> int:
        """
        Getter for minFaceSize

        Returns:
            minFaceSize
        """
        return self.getValueAsInt("minFaceSize")

    @minFaceSize.setter
    def minFaceSize(self, value: int) -> None:
        """
        Setter for minFaceSize
        Args:
            value: new value
        """
        self.setValue("minFaceSize", value)

    @property
    def maxFaceSize(self) -> int:
        """
        Getter for maxFaceSize

        Returns:
            maxFaceSize
        """
        return self.getValueAsInt("maxFaceSize")

    @maxFaceSize.setter
    def maxFaceSize(self, value: int) -> None:
        """
        Setter for maxFaceSize
        Args:
            value: new value
        """
        self.setValue("maxFaceSize", value)

    @property
    def nms(self) -> NMS:
        """
        Getter for nms

        Returns:
            nms
        """
        return NMS[self.getValueAsString("nms")]

    @nms.setter
    def nms(self, value: NMS) -> None:
        """
        Setter for nms
        Args:
            value: new value
        """
        self.setValue("nms", value.value)

    @property
    def redetectTensorSize(self) -> int:
        """
        Getter for redetectTensorSize

        Returns:
            redetectTensorSize
        """
        return self.getValueAsInt("RedetectTensorSize")

    @redetectTensorSize.setter
    def redetectTensorSize(self, value: int) -> None:
        """
        Setter for redetectTensorSize
        Args:
            value: new value
        """
        self.setValue("RedetectTensorSize", value)

    @property
    def redetectFaceTargetSize(self) -> int:
        """
        Getter for redetectFaceTargetSize

        Returns:
            redetectFaceTargetSize
        """
        return self.getValueAsInt("RedetectFaceTargetSize")

    @redetectFaceTargetSize.setter
    def redetectFaceTargetSize(self, value: int) -> None:
        """
        Setter for redetectFaceTargetSize
        Args:
            value: new value
        """
        self.setValue("RedetectFaceTargetSize", value)

    @property
    def paddings(self) -> Point4:
        """
        Getter for paddings

        Returns:
            paddings
        """
        return Point4(*self.getValue("paddings"))

    @paddings.setter
    def paddings(self, value: Point4) -> None:
        """
        Setter for paddings
        Args:
            value: new value
        """
        self.setValue("paddings", value.asTuple())

    @property
    def paddingsIR(self) -> Point4:
        """
        Getter for paddingsIR

        Returns:
            paddingsIR
        """
        return Point4(*self.getValue("paddingsIR"))

    @paddingsIR.setter
    def paddingsIR(self, value: Point4) -> None:
        """
        Setter for paddingsIR
        Args:
            value: new value
        """
        self.setValue("paddingsIR", value.asTuple())

    @property
    def planPrefix(self) -> str:
        """
        Getter for planPrefix

        Returns:
            planPrefix
        """
        return self.getValueAsString("planPrefix")

    @planPrefix.setter
    def planPrefix(self, value: str) -> None:
        """
        Setter for planPrefix
        Args:
            value: new value
        """
        self.setValue("planPrefix", value)

    @property
    def useOrientationMode(self) -> bool:
        """
        Getter for useOrientationMode

        Returns:
            useEstimationByImage
        """
        return bool(self.getValueAsInt("useOrientationMode"))

    @useOrientationMode.setter
    def useOrientationMode(self, value: bool) -> None:
        """
        Setter for useOrientationMode
        Args:
            value: new value
        """
        self.setValue("useOrientationMode", int(value))


class FaceDetV12Settings(BaseSettingsSection):
    """
    Common class for FaceDetV1 and FaceDetV2 detector settings.

    Properties:

        - firstThreshold (float): 1-st threshold in [0..1] range;
        - secondThreshold (float): 2-st threshold in [0..1] range;
        - thirdTThreshold (float): 3-st threshold in [0..1] range;
        - minFaceSize (int): minimum face size in pixels;
        - scaleFactor (float): image scale factor;
        - paddings (Point4): paddings;
        - redetectTolerance (float): redetect tolerance;
    """

    @property
    def firstThreshold(self) -> float:
        """
        Getter for firstThreshold

        Returns:
            float in [0..1] range
        """
        return self.getValueAsFloat("FirstThreshold")

    @firstThreshold.setter
    def firstThreshold(self, value: float) -> None:
        """
        Setter for firstThreshold
        Args:
            value: new value, float in [0..1] range
        """
        self.setValue("FirstThreshold", value)

    @property
    def secondThreshold(self) -> float:
        """
        Getter for secondThreshold

        Returns:
            secondThreshold
        """
        return self.getValueAsFloat("SecondThreshold")

    @secondThreshold.setter
    def secondThreshold(self, value: float) -> None:
        """
        Setter for secondThreshold
        Args:
            value: new value, float in [0..1] range
        """
        self.setValue("SecondThreshold", value)

    @property
    def thirdThreshold(self) -> float:
        """
        Getter for thirdThreshold

        Returns:
            thirdThreshold
        """
        return self.getValueAsFloat("ThirdThreshold")

    @thirdThreshold.setter
    def thirdThreshold(self, value: float) -> None:
        """
        Setter for thirdThreshold
        Args:
            value: new value, float in [0..1] range
        """
        self.setValue("ThirdThreshold", value)

    @property
    def minFaceSize(self) -> int:
        """
        Getter for minFaceSize

        Returns:
            minSize
        """
        return self.getValueAsInt("minFaceSize")

    @minFaceSize.setter
    def minFaceSize(self, value: int) -> None:
        """
        Setter for minFaceSize
        Args:
            value: new value
        """
        self.setValue("minFaceSize", value)

    @property
    def scaleFactor(self) -> float:
        """
        Getter for scaleFactor

        Returns:
            scaleFactor
        """
        return self.getValueAsFloat("scaleFactor")

    @scaleFactor.setter
    def scaleFactor(self, value: float) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("scaleFactor", value)

    @property
    def paddings(self) -> Point4:
        """
        Getter for paddings

        Returns:
            paddings
        """
        return Point4(*self.getValue("paddings"))

    @paddings.setter
    def paddings(self, value: Point4) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("paddings", value.asTuple())

    @property
    def redetectTolerance(self) -> float:
        """
        Getter for redetectTolerance

        Returns:
            redetectTolerance
        """
        return self.getValueAsFloat("redetectTolerance")

    @redetectTolerance.setter
    def redetectTolerance(self, value: float) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("redetectTolerance", value)

    @property
    def useLNet(self) -> bool:
        """
        Getter for useLNet

        Returns:
            useEstimationByImage
        """
        return bool(self.getValueAsInt("useLNet"))

    @useLNet.setter
    def useLNet(self, value: bool) -> None:
        """
        Setter for useLNet
        Args:
            value: new value
        """
        self.setValue("useLNet", int(value))


class FaceDetV1Settings(FaceDetV12Settings):
    """
    FaceDetV1 settings.
    """

    sectionName = "FaceDetV1::Settings"


class FaceDetV2Settings(FaceDetV12Settings):
    """
    FaceDetV2 settings.
    """

    sectionName = "FaceDetV2::Settings"


class HumanDetectorSettings(BaseSettingsSection):
    """
    HumanDetector detector settings.

    Properties:

        - scoreThreshold (float): detection threshold in [0..1] range;
        - redetectScoreThreshold (float): redetect face threshold in [0..1] range;
        - NMSThreshold (float): overlap threshold for NMS [0..1] range;
        - imageSize (int): Target image size for down scaling by load side;
        - nms (NMS): type of NMS: mean or best
        - redetectNMS: type of NMS: mean or best
        - landmarks17Threshold (float): body landmarks threshold in [0..1] range;
    """

    sectionName = "HumanDetector::Settings"

    @property
    def scoreThreshold(self) -> float:
        """
        Getter for scoreThreshold

        Returns:
            scoreThreshold
        """
        return self.getValueAsFloat("scoreThreshold")

    @scoreThreshold.setter
    def scoreThreshold(self, value: float) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("ScoreThreshold", value)

    @property
    def redetectScoreThreshold(self) -> float:
        """
        Getter for redetectScoreThreshold

        Returns:
            redetectScoreThreshold
        """
        return self.getValueAsFloat("RedetectScoreThreshold")

    @redetectScoreThreshold.setter
    def redetectScoreThreshold(self, value: float) -> None:
        """
        Setter for redetectScoreThreshold
        Args:
            value: new value
        """
        self.setValue("RedetectScoreThreshold", value)

    @property
    def NMSThreshold(self) -> float:
        """
        Getter for NMSThreshold

        Returns:
            NMSThreshold
        """
        return self.getValueAsFloat("NMSThreshold")

    @NMSThreshold.setter
    def NMSThreshold(self, value: float) -> None:
        """
        Setter for NMSThreshold
        Args:
            value: new value
        """
        self.setValue("NMSThreshold", value)

    @property
    def redetectNMSThreshold(self) -> float:
        """
        Getter for redetectNMSThreshold

        Returns:
            redetectNMSThreshold
        """
        return self.getValueAsFloat("RedetectNMSThreshold")

    @redetectNMSThreshold.setter
    def redetectNMSThreshold(self, value: float) -> None:
        """
        Setter for redetectNMSThreshold
        Args:
            value: new value
        """
        self.setValue("RedetectNMSThreshold", value)

    @property
    def imageSize(self) -> int:
        """
        Getter for imageSize

        Returns:
            imageSize
        """
        return self.getValueAsInt("imageSize")

    @imageSize.setter
    def imageSize(self, value: int) -> None:
        """
        Setter for imageSize
        Args:
            value: new value
        """
        self.setValue("imageSize", value)

    @property
    def nms(self) -> NMS:
        """
        Getter for nms

        Returns:
            nms
        """
        return NMS[self.getValueAsString("nms")]

    @nms.setter
    def nms(self, value: NMS) -> None:
        """
        Setter for nms
        Args:
            value: new value
        """
        self.setValue("nms", value.value)

    @property
    def redetectNMS(self) -> NMS:
        """
        Getter for redetectMms

        Returns:
            nms
        """
        return NMS[self.getValueAsString("RedetectNMS")]

    @redetectNMS.setter
    def redetectNMS(self, value: NMS) -> None:
        """
        Setter for redetectNMS
        Args:
            value: redetectNMS value
        """
        self.setValue("RedetectNMS", value.value)

    @property
    def landmarks17Threshold(self) -> float:
        """
        Getter for landmarks17Threshold

        Returns:
            scoreThreshold
        """
        return self.getValueAsFloat("landmarks17Threshold")

    @landmarks17Threshold.setter
    def landmarks17Threshold(self, value: float) -> None:
        """
        Setter for landmarks17Threshold
        Args:
            value: new value
        """
        self.setValue("landmarks17Threshold", value)


class LNetBaseSettings(BaseSettingsSection):
    """
    Base class for configuration LNet neural network.

    Properties:

        - planName (str): plan name
        - size (int): size
        - mean (Point3): mean
        - sigma (Point3): sigma

    """

    @property
    def planName(self) -> str:
        """
        Getter for planName

        Returns:
            planName
        """
        return self.getValueAsString("planName")

    @planName.setter
    def planName(self, value: str) -> None:
        """
        Setter for planName
        Args:
            value: new value
        """
        self.setValue("planName", value)

    @property
    def size(self) -> int:
        """
        Getter for size

        Returns:
            size
        """
        return self.getValueAsInt("size")

    @size.setter
    def size(self, value: int) -> None:
        """
        Setter for size
        Args:
            value: new value
        """
        self.setValue("size", value)

    @property
    def mean(self) -> Point3:
        """
        Getter for mean

        Returns:
            mean
        """
        return Point3(*self.getValue("mean"))

    @mean.setter
    def mean(self, value: Point3) -> None:
        """
        Setter for mean
        Args:
            value: new value
        """
        self.setValue("mean", value.asTuple())

    @property
    def sigma(self) -> Point3:
        """
        Getter for sigma

        Returns:
            sigma
        """
        return Point3(*self.getValue("sigma"))

    @sigma.setter
    def sigma(self, value: Point3) -> None:
        """
        Setter for sigma
        Args:
            value: new value
        """
        self.setValue("sigma", value.asTuple())


class LNetSettings(LNetBaseSettings):
    """LNet configuration section"""

    sectionName = "LNet::Settings"


class LNetIRSettings(LNetBaseSettings):
    """LNetIR configuration section"""

    sectionName = "LNetIR::Settings"


class SLNetSettings(LNetBaseSettings):
    """SLNet configuration section"""

    sectionName = "SLNet::Settings"


class QualityEstimatorSettings(BaseSettingsSection):
    """
    Quality estimator settings section.

    Properties:

        - size (int): size
        - expLight (Point3): expLight
        - expDark (Point3): expDark
        - expBlur (Point3):  expBlur
        - logGray (Point4): logGray
        - platt (Point2): coefficient platt
    """

    sectionName = "QualityEstimator::Settings"

    @property
    def size(self) -> int:
        """
        Getter for size

        Returns:
            size
        """
        return self.getValueAsInt("size")

    @size.setter
    def size(self, value: int) -> None:
        """
        Setter for size
        Args:
            value: new value
        """
        self.setValue("size", value)

    @property
    def expLight(self) -> Point3:
        """
        Getter for expLight

        Returns:
            expLight
        """
        return Point3(*self.getValue("expLight"))

    @expLight.setter
    def expLight(self, value: Point3) -> None:
        """
        Setter for expLight
        Args:
            value: new value
        """
        self.setValue("expLight", value.asTuple())

    @property
    def expDark(self) -> Point3:
        """
        Getter for expDark

        Returns:
            expDark
        """
        return Point3(*self.getValue("expDark"))

    @expDark.setter
    def expDark(self, value: Point3) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new expDark
        """
        self.setValue("expDark", value.asTuple())

    @property
    def logGray(self) -> Point4:
        """
        Getter for logGray

        Returns:
            logGray
        """
        return Point4(*self.getValue("logGray"))

    @logGray.setter
    def logGray(self, value: Point4) -> None:
        """
        Setter for logGray
        Args:
            value: new value
        """
        self.setValue("logGray", value.asTuple())

    @property
    def expBlur(self) -> Point3:
        """
        Getter for expBlur

        Returns:
            expBlur
        """
        return Point3(*self.getValue("expBlur"))

    @expBlur.setter
    def expBlur(self, value: Point3) -> None:
        """
        Setter for expBlur
        Args:
            value: new value
        """
        self.setValue("expBlur", value.asTuple())

    @property
    def platt(self) -> Point2:
        """
        Getter for platt

        Returns:
            platt
        """
        return Point2(*self.getValue("platt"))

    @platt.setter
    def platt(self, value: Point2) -> None:
        """
        Setter for platt
        Args:
            value: new value
        """
        self.setValue("platt", value.asTuple())


class HeadPoseEstimatorSettings(BaseSettingsSection):
    """
    Head pose estimator settings section.

    Properties:
        - useEstimationByImage (bool): use head pose estimation by image
        - useEstimationByLandmarks (bool): use head pose estimation by landmarks
    """

    sectionName = "HeadPoseEstimator::Settings"

    @property
    def useEstimationByImage(self) -> bool:
        """
        Getter for useEstimationByImage

        Returns:
            useEstimationByImage
        """
        return bool(self.getValueAsInt("useEstimationByImage"))

    @useEstimationByImage.setter
    def useEstimationByImage(self, value: bool) -> None:
        """
        Setter for useEstimationByImage
        Args:
            value: new value
        """
        self.setValue("useEstimationByImage", int(value))

    @property
    def useEstimationByLandmarks(self) -> bool:
        """
        Getter for useEstimationByLandmarks

        Returns:
            useEstimationByLandmarks
        """
        return bool(self.getValueAsInt("useEstimationByLandmarks"))

    @useEstimationByLandmarks.setter
    def useEstimationByLandmarks(self, value: bool) -> None:
        """
        Setter for useEstimationByLandmarks
        Args:
            value: new value
        """
        self.setValue("useEstimationByLandmarks", int(value))


class EyeEstimatorSettings(BaseSettingsSection):
    """
    Eyes estimator settings section.

    Properties:
        - useStatusPlan (bool): use  status plan or not.
    """

    sectionName = "EyeEstimator::Settings"

    @property
    def useStatusPlan(self) -> bool:
        """
        Getter for useStatusPlan

        Returns:
            useStatusPlan
        """
        return bool(self.getValueAsInt("useStatusPlan"))

    @useStatusPlan.setter
    def useStatusPlan(self, value: bool) -> None:
        """
        Setter for useStatusPlan
        Args:
            value: new value
        """
        self.setValue("useStatusPlan", int(value))


class BestShotQualityEstimatorSettings(BaseSettingsSection):
    """
    Best shot quality estimator estimator settings section.

    Properties:
        - runSubestimatorsConcurrently (int): run sub estimators concurrently
    """

    sectionName = "BestShotQualityEstimator::Settings"

    @property
    def runSubestimatorsConcurrently(self) -> int:
        """
        Getter for runSubestimatorsConcurrently

        Returns:
            useStatusPlan
        """
        return self.getValueAsInt("runSubestimatorsConcurrently")

    @runSubestimatorsConcurrently.setter
    def runSubestimatorsConcurrently(self, value: int) -> None:
        """
        Setter for runSubestimatorsConcurrently
        Args:
            value: new value
        """
        self.setValue("runSubestimatorsConcurrently", value)


class AttributeEstimatorSettings(BaseSettingsSection):
    """
    Attribute estimator settings section.

    Properties:
        - genderThreshold (float): gender threshold in [0..1] range
        - adultThreshold (float): adult threshold in [0..1] range
    """

    sectionName = "AttributeEstimator::Settings"

    @property
    def genderThreshold(self) -> float:
        """
        Getter for genderThreshold

        Returns:
            genderThreshold
        """
        return self.getValueAsFloat("genderThreshold")

    @genderThreshold.setter
    def genderThreshold(self, value: float) -> None:
        """
        Setter for genderThreshold
        Args:
            value: new value
        """
        self.setValue("genderThreshold", value)

    @property
    def adultThreshold(self) -> float:
        """
        Getter for adultThreshold

        Returns:
            adultThreshold
        """
        return self.getValueAsFloat("adultThreshold")

    @adultThreshold.setter
    def adultThreshold(self, value: float) -> None:
        """
        Setter for adultThreshold
        Args:
            value: new value
        """
        self.setValue("adultThreshold", value)


class GlassesEstimatorSettings(BaseSettingsSection):
    """
    Glasses estimator settings section.

    Properties:
        - noGlassesThreshold (float): no glasses threshold in [0..1] range
        - eyeGlassesThreshold (float): eye glasses threshold in [0..1] range
        - sunGlassesThreshold (float): sun glasses threshold in [0..1] range
    """

    sectionName = "GlassesEstimator::Settings"

    @property
    def noGlassesThreshold(self) -> float:
        """
        Getter for noGlassesThreshold

        Returns:
            noGlassesThreshold
        """
        return self.getValueAsFloat("noGlassesThreshold")

    @noGlassesThreshold.setter
    def noGlassesThreshold(self, value: float) -> None:
        """
        Setter for noGlassesThreshold
        Args:
            value: new value
        """
        self.setValue("noGlassesThreshold", value)

    @property
    def eyeGlassesThreshold(self) -> float:
        """
        Getter for eyeGlassesThreshold

        Returns:
            eyeGlassesThreshold
        """
        return self.getValueAsFloat("eyeGlassesThreshold")

    @eyeGlassesThreshold.setter
    def eyeGlassesThreshold(self, value: float) -> None:
        """
        Setter for eyeGlassesThreshold
        Args:
            value: new value
        """
        self.setValue("eyeGlassesThreshold", value)

    @property
    def sunGlassesThreshold(self) -> float:
        """
        Getter for sunGlassesThreshold

        Returns:
            sunGlassesThreshold
        """
        return self.getValueAsFloat("sunGlassesThreshold")

    @sunGlassesThreshold.setter
    def sunGlassesThreshold(self, value: float) -> None:
        """
        Setter for sunGlassesThreshold
        Args:
            value: new value
        """
        self.setValue("sunGlassesThreshold", value)


class OverlapEstimatorSettings(BaseSettingsSection):
    """
    OverlapThreshold any object settings section.

    Properties:
        - overlapThreshold (float): overlap threshold for any object in [0..1] range
    """

    sectionName = "OverlapEstimator::Settings"

    @property
    def overlapThreshold(self) -> float:
        """
        Getter for overlapThreshold

        Returns:
            overlapThreshold
        """
        return self.getValueAsFloat("overlapThreshold")

    @overlapThreshold.setter
    def overlapThreshold(self, value: float) -> None:
        """
        Setter for overlapThreshold
        Args:
            value: new value
        """
        self.setValue("overlapThreshold", value)


class ChildEstimatorSettings(BaseSettingsSection):
    """
    childThreshold settings section.

    Properties:
        - childThreshold (float):  if estimate value less than threshold object is a children.
    """

    sectionName = "ChildEstimator::Settings"

    @property
    def childThreshold(self) -> float:
        """
        Getter for childThreshold

        Returns:
            childThreshold
        """
        return self.getValueAsFloat("childThreshold")

    @childThreshold.setter
    def childThreshold(self, value: float) -> None:
        """
        Setter for childThreshold
        Args:
            value: new value
        """
        self.setValue("childThreshold", value)


class LivenessIREstimatorSettings(BaseSettingsSection):
    """
    LivenessIREstimator settings section.

    Properties:
        - cooperativeMode (bool): whether liveness is checking in cooperative mode
        - irCooperativeThreshold (float): liveness threshold for cooperative mode in [0..1] range
        - irNonCooperativeThreshold (float): liveness threshold for non cooperative mode in [0..1] range
    """

    sectionName = "LivenessIREstimator::Settings"

    @property
    def cooperativeMode(self) -> bool:
        """
        Getter for cooperativeMode

        Returns:
            cooperativeMode
        """
        return bool(self.getValueAsInt("cooperativeMode"))

    @cooperativeMode.setter
    def cooperativeMode(self, value: bool) -> None:
        """
        Setter for cooperativeMode
        Args:
            value: new value
        """
        self.setValue("cooperativeMode", int(value))

    @property
    def irCooperativeThreshold(self) -> float:
        """
        Getter for irCooperativeThreshold

        Returns:
            irCooperativeThreshold
        """
        return self.getValueAsFloat("irCooperativeThreshold")

    @irCooperativeThreshold.setter
    def irCooperativeThreshold(self, value: float) -> None:
        """
        Setter for irCooperativeThreshold
        Args:
            value: new value
        """
        self.setValue("irCooperativeThreshold", value)

    @property
    def irNonCooperativeThreshold(self) -> float:
        """
        Getter for irNonCooperativeThreshold

        Returns:
            irNonCooperativeThreshold
        """
        return self.getValueAsFloat("irNonCooperativeThreshold")

    @irNonCooperativeThreshold.setter
    def irNonCooperativeThreshold(self, value: float) -> None:
        """
        Setter for irNonCooperativeThreshold
        Args:
            value: new value
        """
        self.setValue("irNonCooperativeThreshold", value)


class MaskEstimatorSettings(BaseSettingsSection):
    """
    MaskEstimatorSettings settings section.

    Properties:
        - medicalMaskThreshold (float): medical mask state threshold in [0..1] range
        - missingThreshold (float): missing mask state threshold in [0..1] range
        - occludedThreshold (float): occluded mask state threshold in [0..1] range
    """

    sectionName = "MedicalMaskEstimator::Settings"

    @property
    def medicalMaskThreshold(self) -> float:
        """
        Getter for medicalMaskThreshold

        Returns:
            medicalMaskThreshold
        """
        return self.getValueAsFloat("maskThreshold")

    @medicalMaskThreshold.setter
    def medicalMaskThreshold(self, value: float) -> None:
        """
        Setter for medicalMaskThreshold
        Args:
            value: new value
        """
        self.setValue("maskThreshold", value)

    @property
    def missingThreshold(self) -> float:
        """
        Getter for missingThreshold

        Returns:
            missingThreshold
        """
        return self.getValueAsFloat("noMaskThreshold")

    @missingThreshold.setter
    def missingThreshold(self, value: float) -> None:
        """
        Setter for missingThreshold
        Args:
            value: new value
        """
        self.setValue("noMaskThreshold", value)

    @property
    def occludedThreshold(self) -> float:
        """
        Getter for occludedThreshold

        Returns:
            occludedThreshold
        """
        return self.getValueAsFloat("occludedFaceThreshold")

    @occludedThreshold.setter
    def occludedThreshold(self, value: float) -> None:
        """
        Setter for occludedThreshold
        Args:
            value: new value
        """
        self.setValue("occludedFaceThreshold", value)


class MouthEstimatorSettings(BaseSettingsSection):
    """
    MouthEstimator settings section.

    Properties:
        - occlusionThreshold (float): occlusion mouth threshold in [0..1] range
        - smileThreshold (float): smile threshold in [0..1] range
        - openThreshold (float): open mouth threshold in [0..1] range
    """

    sectionName = "MouthEstimator::Settings"

    @property
    def occlusionThreshold(self) -> float:
        """
        Getter for occlusionThreshold

        Returns:
            occlusionThreshold
        """
        return self.getValueAsFloat("occlusionThreshold")

    @occlusionThreshold.setter
    def occlusionThreshold(self, value: float) -> None:
        """
        Setter for medicalMaskThreshold
        Args:
            value: new value
        """
        self.setValue("occlusionThreshold", value)

    @property
    def smileThreshold(self) -> float:
        """
        Getter for smileThreshold

        Returns:
            smileThreshold
        """
        return self.getValueAsFloat("smileThreshold")

    @smileThreshold.setter
    def smileThreshold(self, value: float) -> None:
        """
        Setter for smileThreshold
        Args:
            value: new value
        """
        self.setValue("smileThreshold", value)

    @property
    def openThreshold(self) -> float:
        """
        Getter for openThreshold

        Returns:
            openThreshold
        """
        return self.getValueAsFloat("openThreshold")

    @openThreshold.setter
    def openThreshold(self, value: float) -> None:
        """
        Setter for occludedThreshold
        Args:
            value: new value
        """
        self.setValue("openThreshold", value)


class HeadAndShouldersLivenessEstimatorSettings(BaseSettingsSection):
    """
    HeadAndShouldersLiveness settings section.

    Properties:
        - shouldersHeightKoeff (float): shouldersHeightKoeff
        - shouldersWidthKoeff (float): shouldersWidthKoeff
        - headWidthKoeff (float): headWidthKoeff
        - headHeightKoeff (float): headHeightKoeff
    """

    sectionName = "HeadAndShouldersLivenessEstimator::Settings"

    @property
    def headWidthKoeff(self) -> float:
        """
        Getter for betaMode

        Returns:
            betaMode
        """
        return self.getValueAsFloat("headWidthKoeff")

    @headWidthKoeff.setter
    def headWidthKoeff(self, value: float) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("headWidthKoeff", value)

    @property
    def headHeightKoeff(self) -> float:
        """
        Getter for betaMode

        Returns:
            betaMode
        """
        return self.getValueAsFloat("headHeightKoeff")

    @headHeightKoeff.setter
    def headHeightKoeff(self, value: float) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("headHeightKoeff", value)

    @property
    def shouldersWidthKoeff(self) -> float:
        """
        Getter for betaMode

        Returns:
            betaMode
        """
        return self.getValueAsFloat("shouldersWidthKoeff")

    @shouldersWidthKoeff.setter
    def shouldersWidthKoeff(self, value: float) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("shouldersWidthKoeff", value)

    @property
    def shouldersHeightKoeff(self) -> float:
        """
        Getter for betaMode

        Returns:
            betaMode
        """
        return self.getValueAsFloat("shouldersHeightKoeff")

    @shouldersHeightKoeff.setter
    def shouldersHeightKoeff(self, value: float) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("shouldersHeightKoeff", value)


class LivenessV1Estimator(BaseSettingsSection):
    """
    LivenessV1(LivenessOneShotRGBEstimator) settings section.

    Properties:
        - realThreshold (float): realThreshold
        - useFilter (bool): useFilter
        - minDetSize (int): minDetSize
        - borderDistance (int): borderDistance
        - principalAxes(int): principalAxes
    """

    sectionName = "LivenessOneShotRGBEstimator::Settings"

    @property
    def realThreshold(self) -> float:
        """
        Getter for realThreshold

        Returns:
            realThreshold
        """
        return self.getValueAsFloat("realThreshold")

    @realThreshold.setter
    def realThreshold(self, value: float) -> None:
        """
        Setter for realThreshold
        Args:
            value: new value
        """
        self.setValue("realThreshold", value)

    @property
    def useFilter(self) -> bool:
        """
        Getter for useFilter

        Returns:
            useFilter
        """
        return bool(self.getValueAsInt("useFilter"))

    @useFilter.setter
    def useFilter(self, value: bool) -> None:
        """
        Setter for useFilter
        Args:
            value: new value
        """
        self.setValue("useFilter", int(value))

    @property
    def minDetSize(self) -> int:
        """
        Getter for minDetSize

        Returns:
            minDetSize
        """
        return self.getValueAsInt("minDetSize")

    @minDetSize.setter
    def minDetSize(self, value: int) -> None:
        """
        Setter for descriptorCountWarningLevel
        Args:
            value: new value
        """
        self.setValue("minDetSize", value)

    @property
    def borderDistance(self) -> int:
        """
        Getter for borderDistance

        Returns:
            borderDistance
        """
        return self.getValueAsInt("borderDistance")

    @borderDistance.setter
    def borderDistance(self, value: int) -> None:
        """
        Setter for borderDistance
        Args:
            value: new value
        """
        self.setValue("borderDistance", value)

    @property
    def principalAxes(self) -> int:
        """
        Getter for principalAxes

        Returns:
            principalAxes
        """
        return self.getValueAsInt("principalAxes")

    @principalAxes.setter
    def principalAxes(self, value: int) -> None:
        """
        Setter for principalAxes
        Args:
            value: new value
        """
        self.setValue("principalAxes", value)


class BaseSettingsProvider:
    """
    Runtime SDK Setting faceEngineProvider.

    Proxy model.

    Attributes:
        pathToConfig (str): path to a configuration file. Config file is getting from
                          the folder'data'  in "FSDK_ROOT".
        _coreSettingProvider (PyISettingsProvider): core settings provider
    """

    # default configuration filename.
    defaultConfName = ""

    def __init__(self, pathToConfig: Optional[Union[str, Path]] = None):
        """
        Init.

        Args:
            pathToConfig: path to config.
        Raises:
             ValueError: if pathToConfig is None and environment variable *FSDK_ROOT* does not set.
        """
        if pathToConfig is None:
            if "FSDK_ROOT" in os.environ:
                self.pathToConfig = Path(os.environ["FSDK_ROOT"]).joinpath("data", self.defaultConfName)
            else:
                raise ValueError(
                    "Failed on path to faceengine luna data folder, set variable pathToData or set"
                    "environment variable *FSDK_ROOT*"
                )
        elif isinstance(pathToConfig, str):
            self.pathToConfig = Path(pathToConfig)
        else:
            self.pathToConfig = pathToConfig

        # todo: check existance

        self._coreSettingProvider = CoreFE.createSettingsProvider(str(self.pathToConfig))

    @property
    def coreProvider(self) -> PyISettingsProvider:
        """
        Get core settings provider
        Returns:
            _coreSettingProvider
        """
        return self._coreSettingProvider


class FaceEngineSettingsProvider(BaseSettingsProvider):
    """
    SDK Setting faceEngineProvider.

    Proxy model.
    """

    # default configuration filename.
    defaultConfName = "faceengine.conf"

    @property
    def systemSettings(self) -> SystemSettings:
        """
        Getter for system settings section.

        Returns:
            Mutable system section
        """
        return SystemSettings(self._coreSettingProvider)

    @property
    def descriptorFactorySettings(self) -> DescriptorFactorySettings:
        """
        Getter for descriptor factory settings section.

        Returns:
            Mutable descriptor factory section
        """
        return DescriptorFactorySettings(self._coreSettingProvider)

    @property
    def faceDetV3Settings(self) -> FaceDetV3Settings:
        """
        Getter for FaceDetV3 settings section.

        Returns:
            Mutable FaceDetV3 section
        """
        return FaceDetV3Settings(self._coreSettingProvider)

    @property
    def faceDetV1Settings(self) -> FaceDetV1Settings:
        """
        Getter for FaceDetV1 settings section.

        Returns:
            Mutable FaceDetV1 section
        """
        return FaceDetV1Settings(self._coreSettingProvider)

    @property
    def faceDetV2Settings(self) -> FaceDetV2Settings:
        """
        Getter for FaceDetV2 settings section.

        Returns:
            Mutable FaceDetV2 section
        """
        return FaceDetV2Settings(self._coreSettingProvider)

    @property
    def humanDetectorSettings(self) -> HumanDetectorSettings:
        """
        Getter for human body settings section.

        Returns:
            Mutable HumanDetectorSettings section
        """
        return HumanDetectorSettings(self._coreSettingProvider)

    @property
    def lNetSettings(self) -> LNetSettings:
        """
        Getter for LNet settings section.

        Returns:
            Mutable LNet section
        """
        return LNetSettings(self._coreSettingProvider)

    @property
    def lNetIRSettings(self) -> LNetIRSettings:
        """
        Getter for LNetIR settings section.

        Returns:
            Mutable LNetIR section
        """
        return LNetIRSettings(self._coreSettingProvider)

    @property
    def slNetSettings(self) -> SLNetSettings:
        """
        Getter for SLNet settings section.

        Returns:
            Mutable SLNet section
        """
        return SLNetSettings(self._coreSettingProvider)

    @property
    def qualityEstimatorSettings(self) -> QualityEstimatorSettings:
        """
        Getter for QualityEstimator settings section.

        Returns:
            Mutable QualityEstimator section
        """
        return QualityEstimatorSettings(self._coreSettingProvider)

    @property
    def headPoseEstimatorSettings(self) -> HeadPoseEstimatorSettings:
        """
        Getter for HeadPoseEstimator settings section.

        Returns:
            Mutable HeadPoseEstimator section
        """
        return HeadPoseEstimatorSettings(self._coreSettingProvider)

    @property
    def eyeEstimatorSettings(self) -> EyeEstimatorSettings:
        """
        Getter for EyeEstimator settings section.

        Returns:
            Mutable EyeEstimator section
        """
        return EyeEstimatorSettings(self._coreSettingProvider)

    @property
    def attributeEstimatorSettings(self) -> AttributeEstimatorSettings:
        """
        Getter for AttributeEstimator settings section.

        Returns:
            Mutable AttributeEstimator section
        """
        return AttributeEstimatorSettings(self._coreSettingProvider)

    @property
    def glassesEstimatorSettings(self) -> GlassesEstimatorSettings:
        """
        Getter for GlassesEstimator settings section.

        Returns:
            Mutable GlassesEstimator section
        """
        return GlassesEstimatorSettings(self._coreSettingProvider)

    @property
    def overlapEstimatorSettings(self) -> OverlapEstimatorSettings:
        """
        Getter for OverlapEstimator settings section.

        Returns:
            Mutable OverlapEstimator section
        """
        return OverlapEstimatorSettings(self._coreSettingProvider)

    @property
    def childEstimatorSettings(self) -> ChildEstimatorSettings:
        """
        Getter for ChildEstimator settings section.

        Returns:
            Mutable ChildEstimator section
        """
        return ChildEstimatorSettings(self._coreSettingProvider)

    @property
    def livenessIREstimatorSettings(self) -> LivenessIREstimatorSettings:
        """
        Getter for LivenessIREstimator settings section.

        Returns:
            Mutable LivenessIREstimator section
        """
        return LivenessIREstimatorSettings(self._coreSettingProvider)

    @property
    def headAndShouldersLivenessEstimatorSettings(self) -> HeadAndShouldersLivenessEstimatorSettings:
        """
        Getter for HeadAndShouldersLivenessEstimator settings section.

        Returns:
            Mutable HeadAndShouldersLivenessEstimator section
        """
        return HeadAndShouldersLivenessEstimatorSettings(self._coreSettingProvider)

    @property
    def bestShotQualityEstimator(self) -> BestShotQualityEstimatorSettings:
        """
        Getter for BestShotQualityEstimatorSettings settings section.

        Returns:
            Mutable BestShotQualityEstimatorSettings section
        """
        return BestShotQualityEstimatorSettings(self._coreSettingProvider)

    @property
    def livenessV1Estimator(self) -> LivenessV1Estimator:
        """
        Getter for LivenessV1Estimator (LivenessOneShotRGBEstimator) settings section.

        Returns:
            Mutable LivenessV1Estimator section
        """
        return LivenessV1Estimator(self._coreSettingProvider)


class RuntimeSettingsProvider(BaseSettingsProvider):
    """
    Runtime SDK Setting faceEngineProvider.

    Proxy model.
    """

    defaultConfName = "runtime.conf"

    @property
    def runtimeSettings(self) -> RuntimeSettings:
        """
        Getter for runtime settings section.

        Returns:
            Mutable runtime section
        """
        return RuntimeSettings(self._coreSettingProvider)
