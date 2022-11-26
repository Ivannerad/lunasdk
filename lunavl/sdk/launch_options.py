from enum import Enum
from platform import platform
from typing import Optional

import FaceEngine as CoreFE  # pylint: disable=E0611,E0401


class DeviceClass(Enum):
    """
    Device enum
    """

    cpu = "cpu"
    gpu = "gpu"


class LaunchOptions:
    """
    Estimator launch options. Some parameters are set for future evaluations.

    Parameters:
      deviceClass: type of device for estimation performing.
      deviceId: device number, actual for gpu and npu
      runConcurrently:

    Attributes:
        _coreLaunchOptions: core launch options
    """

    def __init__(
        self,
        deviceClass: Optional[DeviceClass] = None,
        deviceId: Optional[int] = None,
        runConcurrently: bool = True,
    ):
        self._coreLaunchOptions = CoreFE.LaunchOptions()
        if deviceClass:
            if deviceClass == DeviceClass.gpu:
                device = CoreFE.DeviceClass.GPU
            else:
                device = CoreFE.DeviceClass.CPU_ARM if "arm" in platform() else CoreFE.DeviceClass.CPU_AVX2
        else:
            device = CoreFE.DeviceClass.CPU_ARM if "arm" in platform() else CoreFE.DeviceClass.CPU_AVX2
        self._coreLaunchOptions.deviceClass = device
        if deviceId:
            self._coreLaunchOptions.deviceId = deviceId
        self._coreLaunchOptions.runConcurrently = runConcurrently

    @property
    def deviceClass(self) -> DeviceClass:
        """Get device class"""
        if self._coreLaunchOptions.deviceClass == CoreFE.DeviceClass.CPU_AVX2:
            return DeviceClass.cpu
        else:
            return DeviceClass.gpu

    @property
    def runConcurrently(self) -> bool:
        """Get runConcurrently"""
        return self._coreLaunchOptions.runConcurrently

    @property
    def deviceId(self) -> int:
        """Get runConcurrently"""
        return self._coreLaunchOptions.deviceId

    @property
    def coreLaunchOptions(self) -> CoreFE.LaunchOptions:
        """Get core launch options"""
        return self._coreLaunchOptions

    def __repr__(self) -> str:
        """Get representation"""
        return (
            f"{self.__class__.__name__}(deviceClass={self.deviceClass.name}, "
            f"deviceId={self.deviceId}, runConcurrently={self.runConcurrently})"
        )
