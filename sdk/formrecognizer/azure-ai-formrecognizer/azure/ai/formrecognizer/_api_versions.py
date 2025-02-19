# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class DocumentAnalysisApiVersion(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Form Recognizer API versions supported by DocumentAnalysisClient and DocumentModelAdministrationClient."""

    #: This is the default version
    V2023_02_28_PREVIEW = "2023-02-28-preview"
    V2022_08_31 = "2022-08-31"


class FormRecognizerApiVersion(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Form Recognizer API versions supported by FormRecognizerClient and FormTrainingClient."""

    #: This is the default version
    V2_1 = "2.1"
    V2_0 = "2.0"


def validate_api_version(api_version: str, client_kind: str) -> None:
    """Raise ValueError if api_version is invalid"""

    if client_kind == "form":
        try:
            FormRecognizerApiVersion(api_version)
        except ValueError:
            err_message = "Unsupported API version '{}'. Please select from: {}".format(
                api_version, ", ".join(v.value for v in FormRecognizerApiVersion)
            )
            try:
                DocumentAnalysisApiVersion(api_version)
                err_message += (
                    "\nAPI version '{}' is only available for "
                    "DocumentAnalysisClient and DocumentModelAdministrationClient.".format(api_version)
                )
            except ValueError:
                pass
            raise ValueError(err_message)
    else:
        try:
            DocumentAnalysisApiVersion(api_version)
        except ValueError:
            err_message = "Unsupported API version '{}'. Please select from: {}".format(
                api_version, ", ".join(v.value for v in DocumentAnalysisApiVersion)
            )
            try:
                FormRecognizerApiVersion(api_version)
                err_message += (
                    "\nAPI version '{}' is only available for "
                    "FormRecognizerClient and FormTrainingClient.".format(api_version)
                )
            except ValueError:
                pass
            raise ValueError(err_message)
