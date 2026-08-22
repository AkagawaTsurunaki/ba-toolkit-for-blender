from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, List, Union


def _json_default(obj: Any) -> Any:
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(
        f"Object of type {type(obj).__name__} is not JSON serializable")


@dataclass
class Texture:
    type: Union[str, None]
    part: str
    path: Path

    def __str__(self) -> str:
        type_name = f' ({self.type})' if self.type else ""
        return f'{self.part}{type_name}: {self.path}'


@dataclass
class Animator:
    ch_name: str
    fbx_path: Path
    textures: List[Texture]

    def __str__(self) -> str:
        texture_str = ""
        for texture in self.textures:
            texture_str += f"  {texture}\n"
        return (f'Character Name: {self.ch_name}\n'
                f'FBX path: {self.fbx_path}\n'
                f'Textures: \n'
                f'{texture_str}')


@dataclass
class Metadata:
    animator: Animator
    version: Union[List[int], None] = None

    def __post_init__(self):
        if self.version is None:
            self.version = [0, 1, 0]

    def to_json(self) -> str:
        return json.dumps(
            asdict(self),
            default=_json_default,
            ensure_ascii=False,
            indent=4
        )
