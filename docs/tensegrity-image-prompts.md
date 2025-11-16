# Tensegrity Concept Image Prompts

Based on best practices from Nina Panickssery's blog and Ideogram/Imagen prompting guides.

## Approach

- **Style**: Minimalist, watercolor, abstract (avoid uncanny valley)
- **Composition**: Simple, geometric, emphasizing balance of forces
- **Mood**: Harmony, stability through tension, elegant equilibrium
- **Technique**: Specific, descriptive, define style early
- **Post-processing**: Python-based color correction if needed

---

## Prompt 1: Geometric Force Balance (Ideogram/Imagen)

**Prompt:**
```
A minimalist abstract watercolor illustration showing a suspended geometric structure floating in space. Five colored tension lines (blue, purple, green, orange, pink) pull from different directions toward a central floating polyhedron, creating visible tension and balance. The lines are taut and slightly translucent. Soft lighting from above, clean white background with subtle gradient. Style: modern minimalist technical illustration, Bauhaus-influenced, clean lines, harmonious color palette. The structure appears weightless yet stable, held in perfect equilibrium by the opposing forces.
```

**Use case:** Header image for vision document, represents five forces in equilibrium

---

## Prompt 2: Architectural Tensegrity Form (Imagen)

**Prompt:**
```
An elegant abstract architectural form inspired by Kenneth Snelson's tensegrity sculptures. Slender white compression struts floating in space, connected by invisible tension cables creating a geodesic dome structure. Soft diffused lighting from multiple angles creating subtle shadows. Watercolor wash background in pale blues and grays, fading to white. Style: architectural sketch meets minimalist watercolor, Buckminster Fuller influence, ethereal and weightless. The structure shows stability through balanced forces, not rigid connections.
```

**Use case:** README header, represents architectural inspiration

---

## Prompt 3: Force Vector Diagram (Ideogram)

**Prompt:**
```
A clean technical diagram in minimalist watercolor style showing a central sphere with five arrows extending outward in different directions labeled "Velocity", "Quality", "Coherence", "Learning", "Scope". Each arrow has a different color (electric blue, deep purple, emerald green, warm orange, soft pink) and varying thickness representing force intensity. The arrows appear to be pulling the sphere, creating dynamic tension. White background with subtle grid pattern, soft drop shadows. Style: modern infographic meets watercolor art, clean typography, technical yet artistic.
```

**Use case:** Explanatory diagram, can include text labels

---

## Prompt 4: Balanced Scales Abstraction (Imagen)

**Prompt:**
```
An abstract watercolor composition showing two opposing forces in perfect balance. On one side, a cluster of rapid brush strokes suggesting speed and movement (cool blues and whites). On the other side, geometric precise shapes suggesting structure and control (warm oranges and grays). Between them, a delicate point of equilibrium represented by a thin vertical line with a small geometric form balanced at center. Soft atmospheric background, minimalist composition, generous negative space. Style: Japanese ink wash meets modern abstract, meditative and harmonious, emphasis on balance and restraint.
```

**Use case:** Blog post header, represents velocity vs governance balance

---

## Prompt 5: Biological Cell Tensegrity (Imagen)

**Prompt:**
```
A microscopic view of a biological cell structure showing tensegrity principles. Soft translucent spherical form with internal structural elements - thin filaments creating geometric patterns inside, suggesting the cytoskeleton. Gentle bioluminescent glow from within, organic yet geometric. Watercolor rendering with scientific illustration accuracy but artistic interpretation. Background gradient from deep blue to soft teal. Style: scientific illustration meets contemporary watercolor art, emphasis on natural geometry and organic structural integrity. The cell appears alive yet architecturally sound.
```

**Use case:** "Why Tensegrity" section illustration, shows biological connection

---

## Prompt 6: Software System as Structure (Ideogram)

**Prompt:**
```
An abstract representation of a software system as a tensegrity structure. Multiple floating geometric nodes (cubes, spheres, pyramids) representing system components, connected by glowing lines of varying colors. Some lines are solid (current connections), others are dashed (planned features). The entire structure maintains balance despite asymmetry. Dark gradient background (deep navy to charcoal), with nodes emitting soft glows. Text labels float near nodes: "Agents", "Governance", "Storage", "Learning". Style: technical diagram meets futuristic UI design, cyberpunk-influenced color palette (neon blues, purples, oranges), clean and modern.
```

**Use case:** Technical architecture visualization, can include labels

---

## Prompt 7: Force Flow Visualization (Imagen)

**Prompt:**
```
An abstract visualization of forces in motion and equilibrium. Flowing watercolor washes in five distinct colors (velocity blue, quality purple, coherence green, learning orange, scope pink) stream from different directions, meeting at a central point where they swirl together without mixing, creating a stable vortex. The flows appear dynamic yet balanced, none overpowering the others. Generous white space around the central convergence. Style: fluid dynamics visualization meets abstract expressionism, minimalist approach, emphasis on movement frozen in balance. Soft lighting, ethereal quality.
```

**Use case:** Social media header, dynamic yet balanced

---

## Prompt 8: Human-System Interaction (Imagen)

**Prompt:**
```
A minimalist illustration showing a human silhouette (simple geometric form, not detailed) positioned above a complex abstract structure of interconnected geometric shapes below. The human figure appears to be gently adjusting control points represented by glowing nodes. Five colored threads (representing the five forces) extend from the structure, passing through the human's hands like puppet strings, but reversed - the human tunes the structure, not controls it. Watercolor style, soft pastels with strategic bright accents. Background fades from warm cream to cool gray. Style: instructional diagram meets contemplative art, suggests agency without domination.
```

**Use case:** "How It Works" section, shows human steering role

---

## Prompt 9: Before/After Equilibrium (Ideogram)

**Prompt:**
```
A split-screen minimalist watercolor illustration. Left side: chaotic arrangement of geometric shapes in disarray, conflicting angles, harsh color clashes (reds, blacks), visual tension and instability. Right side: the same shapes now arranged in harmonious tensegrity structure, balanced and stable, soft harmonious colors (blues, greens, grays), peaceful composition. A subtle dividing line with an arrow pointing from left to right. Style: comparative technical illustration, before/after diagram aesthetic, clean and educational. Both sides share same elements but different arrangement demonstrates transformation from chaos to equilibrium.
```

**Use case:** Problem/solution visualization

---

## Prompt 10: Abstract Code Structure (Imagen)

**Prompt:**
```
An abstract representation of evolving codebase as a growing organic-geometric structure. Start with simple geometric form at bottom (foundation), branching upward with increasingly complex but balanced tensegrity-like connections. Each level shows growth while maintaining structural integrity. Watercolor technique with subtle gridlines suggesting code. Color gradient from foundational gray/blue at bottom to vibrant varied colors at top (suggesting diversity of features). Style: architectural axonometric drawing meets organic growth patterns, isometric perspective, clean lines with artistic watercolor washes, suggests both planning and emergence.
```

**Use case:** Roadmap visualization, codebase evolution

---

## Technical Notes

### Ideogram vs Imagen Selection

**Use Ideogram for:**
- Images needing text labels (Prompts 3, 6, 9)
- Typography-heavy designs
- More stylized/graphic outputs

**Use Imagen for:**
- Pure abstract compositions (Prompts 2, 4, 5, 7, 8, 10)
- Watercolor/painterly effects
- Complex conceptual metaphors

### Post-Processing (Python)

If backgrounds aren't pure white or colors need correction:

```python
from PIL import Image
import numpy as np

def clean_background(image_path, output_path):
    img = Image.open(image_path)
    data = np.array(img)

    # Set near-white pixels to pure white
    white_threshold = 240
    mask = (data[:,:,0] > white_threshold) & \
           (data[:,:,1] > white_threshold) & \
           (data[:,:,2] > white_threshold)
    data[mask] = [255, 255, 255]

    cleaned = Image.fromarray(data)
    cleaned.save(output_path)
```

### Iteration Strategy

Per Ideogram best practices:
1. Start with basic prompt
2. Generate first version
3. Identify what needs refinement
4. Add ONE specific detail at a time
5. Compare results
6. Iterate until satisfied

### Color Palette (Consistent Across Images)

- **Velocity**: Electric blue (#2196F3)
- **Quality**: Deep purple (#7B1FA2)
- **Coherence**: Emerald green (#388E3C)
- **Learning**: Warm orange (#F57C00)
- **Scope**: Soft pink (#C2185B)
- **Neutral**: Grays, whites, subtle blues

This maintains visual consistency across all concept images.
