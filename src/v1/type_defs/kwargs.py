from typing_extensions import TypedDict


class UvicornKwargs(TypedDict):
  host: str
  port: int
  reload: bool
