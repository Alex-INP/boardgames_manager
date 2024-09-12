from pydantic import BaseModel


class HeaderBase(BaseModel):
    value: str


class HeaderCreate(HeaderBase):
    pass


class Header(HeaderBase):
    id: int
    template_id: int

    class ConfigDict:
        from_attributes = True


class TemplateBase(BaseModel):
    name: str


class TemplateCreate(TemplateBase):
    name: str


class Template(TemplateBase):
    id: int
    headers: list[Header] = []

    class ConfigDict:
        from_attributes = True
