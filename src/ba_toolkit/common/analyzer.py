from pathlib import Path
from typing import List

from .schema import Animator, Texture


def _get_textures_schema(dir: Path, ch_name: str, anim_type: str) -> List[Texture]:
    # `ch_name` and `anim_type` use for checking the consistency only.
    textures = []

    for texture_file in dir.glob('*.png'):
        assert texture_file.stem.split('_')[0] == ch_name
        # assert texture_file.stem.split('_')[1] == anim_type
        part_name = texture_file.stem.split('_')[2]
        try:
            type_name = texture_file.stem.split('_')[3]
        except IndexError:
            type_name = None
        # print(f"{ch_name} {part_name} {type_name}")
        texture = Texture(type=type_name, part=part_name, path=texture_file)
        textures.append(texture)

    return textures


def get_animator_schema(dir: Path, anim_type="Original"):
    # `anim_type` should be "Original" only.
    # `anim_type` is the suffix of the name of the output folder from Assets Studio.
    assert dir.exists(), f'No such directory: {dir}\nPlease check your Assets Studio output.'
    fbx_paths = []
    for fbx_file in dir.glob('*.fbx'):
        fbx_paths.append(fbx_file)
    assert len(fbx_paths) == 1, (f'There should be only 1 FBX model file in {dir}:\n'
                                 f'{fbx_paths}')
    fbx_path: Path = fbx_paths[0]
    print(fbx_path)

    ch_name = fbx_path.stem.split('_')[0]
    print(ch_name)

    textures = _get_textures_schema(dir=dir, ch_name=ch_name, anim_type=anim_type)

    result = Animator(ch_name=ch_name, fbx_path=fbx_path, textures=textures)
    return result
