import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str = field(repr=False)


def get_credentials() -> Credentials | None:
    username = os.getenv("HUDL_USERNAME")
    password = os.getenv("HUDL_PASSWORD")
    if not username or not password:
        return None
    return Credentials(username, password)
