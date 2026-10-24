# Honey bee colony role plate — correction record

**Date:** 2026-10-24
**Chapter:** 5.2; plate ID `bee`.
**Asset:** `atlas_bee.svg` → generated `atlas_bee.png`.

## Corrected content
- The queen is a fertile diploid female and the primary egg-layer.
- Workers are diploid females responsible for brood care, foraging and defence; they are usually nonreproductive.
- Drones are haploid males that usually develop from unfertilized eggs and mate with queens; they lack a stinger.
- The groups are shown in parallel; the image does not imply queen → worker → drone as successive developmental stages.
- Tamil caste labels use a Tamil-capable renderer; the original overlapping caption row and misleading single-bee drawing are removed.

## Verification and release gates
- Source SVG was locally rasterized and visually previewed at 1040×720; the previous worker-label overrun was corrected before commit.
- Phase III `repair_plates_phase3.py` must rasterize the committed SVG to `atlas_bee.png` and commit the generated asset.
- The native build, screenshot export, and on-device enlargement/Tamil inspection must subsequently be checked against the generated PNG.
- This is a **role-comparison teaching schematic**, not a species-level anatomical plate. Academic reviewer and rights clearance remain pending; do not change `NOT_CLEARED` or `NOT_SIGNED_OFF` solely due to this revision.
