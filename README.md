# Blue Archive Toolkit for Blender

This toolkit is a helpful Blender add‑on for creating 3D animations using Blue Archive models. 
It assists with model import, attempts to fix texture issues, 
and automatically separates the mouth mesh then binds it to a mouth controller, enabling faster animation setup.

## Installation

Minimum Blender version: 4.5.6 LTS

Tested Blender version: 4.5.6 LTS, 5.2.0 LTS

Other versions are untested.

**Instructions:**
1. Download the latest `.zip` from [Releases](https://github.com/AkagawaTsurunaki/ba-toolkit-for-blender/releases/latest).
2. Drag and drop the `.zip` directly into the Blender window.

## How to use?

### Import from Folder

Import model from specific folder containing FBX and texture files (`.png`) exported from Assets Studio.  
For example, `D:/AssetsStudioOutput/Animator/Aris_Original`

We recommend that import `<Character>_Original`.

If the textures of `<Character>_Original` are lost, then delete the imported one, and try to import `<Character>_Original_Mesh`.

---

### Auto Fix Textures (EXP)

Automatically assigns textures to the corresponding meshes of the imported model by matching texture file names.

> [!WARNING] 
> This feature is experimental; it may fail or assign textures to incorrect meshes.
> If there is no texture issue, DO NOT click this button!

**Instructions:**
1. Select the imported model's root object in the Hierarchy panel.
2. Click `Auto Fix Textures (EXP)`.

---

### Auto Separate Mouth

Automatically separate the mouth area of the selected character model as a new mesh object.

Raycast based algorithm is used and may not be successful for all models.

**Instructions:**
1. Select the imported model's root object in the Hierarchy panel.
2. Click `Auto Separate Mouth`.

If it fails, try separating the mouth area manually:
1. Select the mouth faces in Edit Mode.
2. Press `L` to link faces.
3. Press `Alt+M` to split the linked faces.
4. Press `P` to separate the selected faces as a new mesh object.

---

### Bind Mouth to Selected

Bind mouth controller to selected mesh.

> [!WARNING] 
> This operation will remove all materials of the selected mesh.

**Instructions:**
1. Select the mouth mesh (e.g., `Aris_Origin_Body_Mouth`).
2. Click `Bind Mouth to Selected`. A mouth controller will be added to the scene.
3. Switch to Pose Mode.
4. Click the little selection box on the surface of the `Mouth Sprite Sheet`.
5. Press `G` to move it around and pick the mouth shape you like.

> Thanks to [BlackMaLou](https://www.bilibili.com/video/BV1z6PYebE7g) for sharing the `Mouth Sprite Sheet`.


## Contact me

Email: [AkagawaTsurunaki@outlook.com](AkagawaTsurunaki@outlook.com)

Github: [AkagawaTsurunaki](https://github.com/AkagawaTsurunaki)

Bilibili: [赤川鹤鸣_Channel](https://space.bilibili.com/1076299680)