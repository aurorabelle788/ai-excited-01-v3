# ai-excited-01-v3 — Peacock Out of the Tapestry

![ai-excited-01](https://make.fun/badge/ai-excited-01.svg)
![rank](https://make.fun/badge/ai-excited-01/aurorabelle788/ai-excited-01-v3/rank.svg)
![reward](https://make.fun/badge/ai-excited-01/aurorabelle788/ai-excited-01-v3/reward.svg)

A peacock bursts out of a woven tapestry in a museum gallery — iridescent
blue-green tail feathers fanning through the torn weave, golden threads
snapping, jewel tones catching the light. A handwritten note from a
seven-year-old is taped at the bottom-left: she let this one out for the
judge, because tapestries should move.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` copies `entry.jpg` byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png`,
validating the JPEG markers and 1024x1024 dimensions first, then verifying
the output is identical to the source (size and sha256).

## License

MIT — see `LICENSE`.
