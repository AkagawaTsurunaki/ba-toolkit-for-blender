from dataclasses import dataclass
from pathlib import Path
from typing import List, Union


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
