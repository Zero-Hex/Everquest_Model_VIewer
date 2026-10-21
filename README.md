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
  - V read as stored on static models and negated on skinned ones (models
    with bones: Hero's Forge pieces, Drakkin, animated items), as the client
    does; stock data shows it (the Iksar-only plate helm is the general static
    one with every V negated);
  - shading follows the client's own compiled shaders
    (`RenderEffects/SPL/SModel*.fxo`, `SkinMesh*.fxo`), read from the
    shader bytecode. The letters after `CB` in the shader name select the
    features: `S` specular, `G` glow, `E` environment.
    - **Normal maps on `G` shaders:** rebuilt as (x, y, 0.9), with blue as a
      glow mask added to the lighting.
    - **Normal maps on other shaders:** all three channels are the normal
      (stock maps keep Z in blue; a blue of 0 points the normal into the
      surface and the client then lights it by ambient only).
    - **Specular:** `min(1, pow(N·H, e_fShininess0) × mask × N·L)` times the
      light colour, where the mask is the normal map's alpha.
    - **Environment map:** sphere-mapped on the reflection vector and added
      to the texture at `e_fEnvMapStrength0 × 0.25` before lighting.
  - additive glow on `AddAlpha` materials, cut-outs and see-through
    materials;
  - animated textures;
  - stored mip levels, with a Mip control to see what shows at a distance.
- **Item animations:** an item's own `.ani` files play on its skeleton.
- **Effects:** with your client folder picked, an item's `.prt`/`.pts`
  emitters play from `actoremittersnew.edd` and the `*Effects` sprites.
- **Figure:** a body that holds the selected item (and a second one or a
  shield), or wears Heroes' Forge armor pieces as a set. Choose one of:
  - a stick figure;
  - any race from your client folder: classic races from `global_chr.s3d` in
    their standing pose, Luclin races from `global<race>_chr.s3d` in their
    default clothing (see Armor texture below), Frogloks
    from `globalpcfroglok_chr.s3d`, Drakkin from `dkm.eqg` / `dkf.eqg`, built
    as the game builds them: the base model plus the outfit parts for the armor
    material (`dkm_<MM>_00_*`), hair and tattoos, with hair and tattoo colour
    pickers, and `.ani` animations from `dkm_anims.eqg` / `dkf_anims.eqg`;
  - a race from an open `*_chr.s3d`.

  On a race body, items go on its `R_POINT`, `L_POINT`, `SHIELD_POINT` and
  `HEAD_POINT` (on Drakkin, the `ARMR_WEAP`, `ARML_WEAP`, `ARML_SHLD` and
  `HEAD_HEAD` bones), as in game. **Hand** picks where the selected weapon
  goes: Primary (right hand, an added item in the left), Secondary (left
  hand) or Both (the same weapon in each hand); shields stay on the shield
  arm. A point's scale applies to what hangs on it, so a gnome's weapons are
  drawn smaller and an ogre's larger. The last body, set, armor texture,
  animation and hand are remembered in the browser and come back when the
  figure is turned on.
- **Body panel** (for race bodies):
  - **Animation:** every animation the client has for the race, grouped as
    combat, movement, idle, poses, social and casting (`C08` is 1H
    slashing, `C03` 2H slashing, and so on). Races with no set of their own
    use the one the client shares with them, the way the stock data does.
    With **Loop** off, an animation plays once and the body goes back to
    standing; **Play** runs it again.
  - **Armor texture:** None, leather, chain, plate, monk, robes, and Velious
    materials when `global<NN>_amr.s3d` is in the folder. Each page comes
    from the race's own WLD material (`HUMCH0303_MDF`), which names the
    skin page and an armor page drawn over it (`humchsk03.dds` +
    `humch0203.dds_layer`): the armor's alpha says where it covers, and the
    skin shows where it is clear. Some point elsewhere: a Luclin plate
    chest is the chain chest's sprite, so there are no `ch03` files.
    Material 00 is the default clothing (a human's vest and trousers, an
    Iksar's harness), so None is not naked. Classic bodies swap the whole
    page.
  - **Hero's Forge set:** pick a set number. The pieces for that race are found
    through `NewArmorTagData.txt` and `OnDemandResources.txt`, put on the
    body and follow the animation. An armor piece you have open takes its
    slot in the set, replacing the set's piece, so a custom piece can be
    checked against the rest of a set. Weapons and shields are held. Body
    skin under the armor is hidden so it can't poke through: a body triangle
    goes when rays out from its corners, edge midpoints and centre all meet
    a worn piece close by, so skin in real gaps (between froglok leg pads)
    stays. A checkbox turns this off. A helm without Show Hair hides head
    page 06 (a human's ears, an Iksar's spikes), and a Hero's Forge chest,
    legs or robe replaces a Drakkin's outfit parts. Luclin females use `LF`
    rows. Drakkin use the tag file's `N` rows. Pieces hung on a point (helms, bracers,
    gloves) get the race's fit from `NewArmorAdjData.txt` (scale, offset and
    rotation per point) unless their tag row says Ignore Adjustment (-1).
    The angles are read Z-Y-X with X negated, which turns barbarian, gnome
    and halfling wrist points onto the human one.
  - **Robes:** on Luclin bodies a robe texture (10-16) covers only the chest
    and arms. In RoF2 the skirt is a model in the Robe slot, so pick a robe
    set (116-121) for the full robe.
- **Find:** open any item by ID through `OnDemandResources.txt`, by archive
  name, or by actor name inside the `.s3d` equipment archives.
- **Recently opened:** reopen models you looked at before.
- **Friendly names:** give a model a name of your own in Selected model
  (`IT62600` → "Molten Blade"). Names show in the model list, Recently
  opened, Find and on the view, Find searches them, and **Export names** /
  **Import names…** move them between browsers or share them as a `.json`
  file.
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
- **Viewing:** full screen, a phone layout, brightness, an **Ambient**
  slider (0 turns the ambient light off, so only the main lights shade the
  model), adjustable light direction and a Rotate 90° button for sideways
  `.s3d` items. Brightness, ambient, light direction, backdrop and scene are
  remembered in the browser; a zone backdrop comes back once the client
  folder is picked.
- **Backdrop:** black, grey or the page colour, or a character-select zone
  from your client folder: `load.s3d` (the marble room) or `load2.s3d`, with
  their placed objects from `load_obj.s3d` / `load2_obj.s3d`. `load2` holds
  several scenes (a library, a distillery, a great hall and more); **Scene**
  picks one, and the figure stands on its floor.
- **Sidebar:** sections remember whether you folded them, and **Sections**
  hides the ones you don't use. Both are kept in the browser.

## Browser support

Any current desktop browser. Picking a whole folder (Client folder…) needs a
desktop browser; iPhone and iPad browsers can only open single files. In
Chrome and Edge the picked folder is remembered: on your next visit a
**Reconnect** button opens it again after one permission prompt. Firefox and
Safari can't keep a folder between visits, and no browser allows it when
the page is embedded in another site, so there you pick the folder again.
Everything the page remembers (names, sections, body choices) stays in that
browser's storage on your computer.

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
  (actors). A track frame is eight 16-bit values: rotation w, x, y, z over
  16384, shift x, y, z over 256, and the bone's scale over 256, which also
  scales the bones below it. The last value is often read as a shift
  denominator, which gives the same shape for most bones but not for end
  bones: Luclin eyes are 244 (read as a scale they sit in their sockets,
  not in front of them), the human seat bone is 6, and a gnome's `R_POINT`
  is 163, so its weapons are drawn at 0.64.
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
