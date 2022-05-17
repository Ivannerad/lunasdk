"""Module realize dynamic and dense index."""
import os
from enum import Enum
from pathlib import Path
from typing import List

from lunavl.sdk.descriptors.descriptors import FaceDescriptor, FaceDescriptorBatch
from lunavl.sdk.errors.exceptions import assertError

from .base import CoreIndex, IndexResult


class IndexType(Enum):
    """Available index type to save|load."""

    # dense index
    dense = "dense"
    # dynamic index
    dynamic = "dynamic"


class DynamicIndex(CoreIndex):
    """
    Dynamic Index
    """

    @property
    def descriptorsCount(self):
        """Get actual count of descriptor in internal storage."""
        return self._coreIndex.countOfIndexedDescriptors()

    def append(self, descriptor: FaceDescriptor) -> None:
        """
        Appends descriptor to internal storage.
        Args:
            descriptor: descriptor with correct length, version and data
        Raises:
            LunaSDKException: if an error occurs while adding the descriptor
        """
        error = self._coreIndex.appendDescriptor(descriptor.coreEstimation)
        assertError(error)

    def appendBatch(self, descriptorsBatch: FaceDescriptorBatch) -> None:
        """
        Appends batch of descriptors to internal storage.
        Args:
            descriptorsBatch: batch of descriptors with correct length, version and data
        Raises:
            LunaSDKException: if an error occurs while adding the batch of descriptors
        """
        error = self._coreIndex.appendBatch(descriptorsBatch.coreEstimation)
        assertError(error)

    def search(self, descriptor: FaceDescriptor, maxCount: int = 1) -> List[IndexResult]:
        """
        Search for descriptors with the shorter distance to passed descriptor.
        Args:
            descriptor: descriptor to match against index
            maxCount: max count of results (default is 1)
        Raises:
            LunaSDKException: if an error occurs while searching for descriptors
        Returns:
            list with index search results
        """
        error, resIndex = self._coreIndex.search(descriptor.coreEstimation, maxCount)
        assertError(error)
        return [IndexResult(result) for result in resIndex]

    def save(self, path: str, indexType: IndexType) -> None:
        """
        Save index as 'dynamic' or 'dense' to local storage.
        Args:
            path: path to file to be created
            indexType: index type ('dynamic' or 'dense')
        Raises:
            ValueError: if path is a directory or index type is incorrect
            PermissionError: if write access is denied
            LunaSDKException: if an error occurs while saving the index
        """
        if Path(path).is_dir():
            raise ValueError(f"{path} must not be a directory")
        if not os.access(Path(path).parent, os.W_OK):
            raise PermissionError(f"Access is denied: {path}")

        if IndexType(indexType) == IndexType.dynamic:
            error = self._coreIndex.saveToDynamicIndex(path)
        else:
            error = self._coreIndex.saveToDenseIndex(path)

        assertError(error)


class DenseIndex(CoreIndex):
    """
    Dense Index
    """

    def __delitem__(self, index: int):
        """Remove descriptor for a dense index is not supported."""
        raise AttributeError("'DenseIndex' object has no attribute '__delitem__'")

    def search(self, descriptor: FaceDescriptor, maxCount: int = 1) -> List[IndexResult]:
        """
        Search for descriptors with the shorter distance to passed descriptor.
        Args:
            descriptor: descriptor to match against index
            maxCount: max count of results (default is 1)
        Raises:
            LunaSDKException: if an error occurs while searching for descriptors
        Returns:
            list with index search results
        """
        error, resIndex = self._coreIndex.search(descriptor.coreEstimation, maxCount)
        assertError(error)
        return [IndexResult(result) for result in resIndex]
