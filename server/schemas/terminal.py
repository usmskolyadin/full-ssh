from pydantic import BaseModel


class SSHSchema(BaseModel):
    hostname: str | None = "185.251.90.58"
    port: int | None = 22
    username: str | None = "root"
    password: str | None = "ufexwepukawead"
