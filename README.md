# EQG Model Viewer

A browser tool for looking at EverQuest Rain of Fear 2 (RoF2) client models
outside the game. Open an `.eqg` or `.s3d` archive, or point it at your
EverQuest folder, and inspect items, armor and characters roughly the way
the client draws them. Pre-flight checks catch the mistakes that make custom
items fail in game.

Everything runs in your browser. **Files you open are read on your computer
and never uploaded.** No game files are included in this repository.

## Use it

- **Online:** <https://zero-hex.github.io/Everquest_Model_VIewer/> (GitHub
  Pages, served from this repository's `main` branch).
- **Offline:** download the repository and open `index.html`. The three.js and
  pako libraries it needs are in `vendor/`.

Then either **Open .eqg / .s3d…** to look at one archive, or **Client
folder…** to pick your EverQuest folder (the one with `eqgame.exe`) and use
**Find** to open any item by ID.

## Features

- **Models:** EQGM `.mod` models from `.eqg` archives, WLD actors and meshes
  from `.s3d` archives, and DDS, BMP and TGA textures.
- **Drawn like the client:**
  - one-sided faces;
  - V read as stored;
  - normal maps, with the normal map's alpha as the specular mask;
  - environment shine on `*E` shaders, additive glow on `AddAlpha` materials,
    cut-outs and see-through materials;
  - animated textures;
  - stored mip levels, with a Mip control to see what shows at a distance.
- **Item animations:** an item's own `.ani` files play on its skeleton.
- **Effects:** with your client folder picked, an item's `.prt`/`.pts`
  emitters play from `actoremittersnew.edd` and the `*Effects` sprites.
- **Figure:** a body that holds the selected item (and a second one or a
  shield), or wears Heroes' Forge armor pieces as a set. Choose one of:
  - a stick figure;
  - any race from your client folder: classic races from `global_chr.s3d` in
    their standing pose, Luclin races from `global<race>_chr.s3d`;
  - a race from an open `*_chr.s3d`.

  On a race body, items go on its `R_POINT`, `L_POINT`, `SHIELD_POINT` and
  `HEAD_POINT`, as in game.
- **Body panel** (for race bodies):
  - **Animation:** every animation the client has for the race, grouped as
    combat, movement, idle, poses, social and casting (`C08` is 1H
    slashing, `C03` 2H slashing, and so on). Races with no set of their own
    use the one the client shares with them, the way the stock data does.
  - **Armor texture:** None, leather, chain, plate, monk, robes, and Velious
    materials when `global<NN>_amr.s3d` is in the folder.
  - **Hero's Forge set:** pick a set number. The pieces for that race are found
    through `NewArmorTagData.txt` and `OnDemandResources.txt`, put on the
    body and follow the animation. An armor piece you have open takes its
    slot in the set, replacing the set's piece, so a custom piece can be
    checked against the rest of a set. Weapons and shields are held. The tag
    file's Hide Mesh flag is applied: the body's legs or feet under such a
    piece are hidden, as in game.
  - **Robes:** on Luclin bodies a robe texture (10-16) covers only the chest
    and arms. In RoF2 the skirt is a model in the Robe slot, so pick a robe
    set (116-121) for the full robe.
- **Find:** open any item by ID through `OnDemandResources.txt`, by archive
  name, or by actor name inside the `.s3d` equipment archives.
- **Recently opened:** reopen models you looked at before.
- **Compare:** two models side by side, with cameras linked or separate, effects on
  both sides and a stats table.
- **Export:**
  - the view as PNG;
  - transparent icon PNGs (40, 64 or 256 px);
  - all textures as PNG;
  - the model as glTF (`.glb`).
- **Pre-flight checks:**
  - materials over 2,400 triangles (the client skips them without an error);
  - stored or dark mip levels;
  - missing textures and animation frames;
  - UVs that look upside down;
  - registry lines, case and ID prefix clashes in `OnDemandResources.txt`.
- **Client checks:** scan the whole client folder, filtered to your own IDs
  (`IT62` or `62000-62999`). It reports:
  - registry lines whose archive is missing, or whose file isn't in the archive;
  - IT models no registry line points at;
  - IDs listed for more than one archive;
  - ID prefix clashes;
  - `NewArmorTagData.txt` rows that use unregistered models.

  Click a finding to open the model.
- **Viewing:** full screen, a phone layout, adjustable light direction and a
  Rotate 90° button for sideways `.s3d` items.

## Browser support

Any current desktop browser. Picking a whole folder (Client folder…) needs a
desktop browser; iPhone and iPad browsers can only open single files. In
Chromium-based browsers the picked folder is remembered between visits.

## How accurate is it?

The viewer tries to match the client, and it is honest about where it can't.

**Checked against the client:**

| Area | What was checked |
| --- | --- |
| UVs | V read as stored, matched against in-game screenshots of two items |
| Faces | One-sided, as stock models are wound and outline shells need |
| BMP textures in `.s3d` | Read in file row order; stock axe heads only join up that way |
| Effect colour | `red/green/blue_tint1` and `tint2` set the colour |
| Effect size | `total_scale` scales the effect |
| Effect attachment | `.pts` points, which can name a bone (then bone-local) |
| Effect blending | Alpha by default; stock blood drops draw dark red |
| Particles | World-space sprites that face the camera and trail a moving item |

**Read from the data, not confirmed:**

| Area | Current reading |
| --- | --- |
| Lighting | Ambient plus a light at the camera, tuned to a few screenshots |
| Effect motion | Speed, direction, spread and timing |
| Effect lifetime | `fadeout_time` |
| Additive effects | Only when field70 = 1 and field71 = 2 |
| Zero particle scales | Sized by `total_scale × image_stretch` |
| Figure | Static Heroes' Forge pieces (helm, bracers, hands) placed by size |

Effect field names follow `data.h` from EQEmuParticleEditor; most have no
published meaning.

## File formats used

- **PFS archives** (`.eqg`, `.s3d`) are zlib blocks with a name table.
- **EQGM `.mod`** holds materials and properties, vertices (32 or 44 bytes),
  triangles, bones and weights.
- **EQGA `.ani`** keeps one key track per bone.
- **EQPT `.pts`** lists attachment points.
- **PTCL `.prt`** (v4 and v5) lists emitter entries.
- **EDD** is `name[64]`, `texture[32]` and 80 fields per emitter.
- **WLD** (`.s3d`) uses fragments 0x03/04/05/30/31 (materials), 0x36
  (meshes), 0x2D, 0x10/0x11/0x12/0x13 (skeletons and tracks) and 0x14
  (actors).
- **Textures:** DDS (DXT1/3/5 and uncompressed, with stored mips), BMP (8, 24
  and 32-bit) and TGA (24/32-bit, raw or RLE).

## Development

`eqg_viewer.html` is the source: the page body, loading three.js and pako
from CDNs. `build.py` turns it into `index.html`, a full page that loads them
from `vendor/`:

```sh
python3 build.py
```

## Credits

- [quail](https://github.com/xackery/quail) by xackery, for its EQG format
  readers.
- [EQEmuParticleEditor](https://github.com/Zaela/EQEmuParticleEditor) by
  Zaela, for the EDD emitter field names.
- The EQEmu community, for the format knowledge this builds on.
- [three.js](https://threejs.org/) (MIT) and
  [pako](https://github.com/nodeca/pako) (MIT and Zlib).

## Disclaimer

EverQuest is a registered trademark of Daybreak Game Company LLC. This
project is not affiliated with or endorsed by Daybreak. It ships no game
files; it only reads files you already have.

## License

MIT, © 2026 Zero-Hex. See `LICENSE`.
