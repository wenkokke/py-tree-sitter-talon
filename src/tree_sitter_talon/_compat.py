import sys

################################################################################
# Python 3.7 and 3.8 compatibility: _removeprefix
################################################################################

if sys.version_info >= (3, 9):

    def _removeprefix(text: str, prefix: str) -> str:
        return text.removeprefix(prefix)

else:

    def _removeprefix(text: str, prefix: str) -> str:
        if prefix == text[: len(prefix)]:
            return text[len(prefix) :]
        else:
            return text
