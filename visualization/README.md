# Fair best responses for Leontief donations

[Download the interactive explorer (ZIP)](https://github.com/DannyExperiments/fair-leontief-donation-dynamics/raw/refs/heads/main/visualization/fair-leontief-explorer.zip). Unzip it and open `index.html` in your browser to rotate the 3D aggregate plot and step through the exact example. The explorer runs offline and displays the active donor’s old allocation, the other donors’ contributions, and the unique best response. The ZIP also includes the [animated figure](fair-schedule.gif) for rounds 3–15 and the rendering source.

## Worked example

The plot axes are the amounts donated to projects X, Y, and Z. The dot marks the total after the indicated turn. The ring marks the Nash aggregate `(1, 1, 1)`. A donor’s weight 0 excludes that project from her utility minimum.

| Donor | Budget | X | Y | Z |
| --- | ---: | ---: | ---: | ---: |
| A | 1 | 1 | 1 | 0 |
| B | 1 | 0 | 1 | 1 |
| C | 1 | 1 | 0 | 2 |

Start at zero. For each integer `k ≥ 1`, select A then B, repeat this pair `k` times, then select C. The first blocks are `AB C | ABAB C | ABABAB C`. C plays at rounds `k(k + 2)`; from one turn of C to the next the gaps are 5, 7, 9, …. This is a fair schedule with unbounded gaps. The picture starts after round 3, once all three budgets have been allocated. It shows the part of the budget plane where all three coordinates are at least 1/2.

In round 8, the two other donors contribute 11/16 to X and 9/32 to Z. C puts her unit on Z, attaining utility `41/64 < 11/16`. Keeping any portion on X would lower the binding Z utility. The aggregate changes from `(15/16, 33/32, 33/32)` to `(11/16, 33/32, 41/32)`.

After round 8, holding C’s full unit on Z, A’s next Y contribution is half B’s prior Z contribution. B then puts half A’s new Y contribution on Z. A’s X contribution increases and B’s Z contribution decreases. Hence the round-8 inequality `(1 + B_Z)/2 ≤ A_X` continues to hold whenever C plays again. Each C turn leaves her allocation fixed. After the first such pair, both `A_Y` and `B_Z` shrink by a factor of four per additional A–B pair. The total tends to `(1, 1, 1)`.

The full theorem guarantees aggregate convergence for every fair schedule with arbitrary weights. Its proof freezes the outside blocks up to the first outside update and uses equality of potential on the slice to identify the limiting aggregate. [Paper and reference](https://doi.org/10.5281/zenodo.24564949)

## Replay

Run the exact checks with Python 3.

```sh
python3 render.py --check-only
```

With Pillow and a regular/bold TrueType font pair available, the renderer generates the GIF, refreshes the embedded exact data, and rebuilds the ZIP. On macOS it defaults to system Arial, and on common Linux installations to DejaVu Sans. Font and Pillow versions can change rendered bytes.

```sh
python3 render.py
shasum -a 256 -c SHA256SUMS.txt
```

The generator checks 48 best responses with rational arithmetic and asserts the round-8 calculation and the recurrence after round 8. Plot coordinates and camera geometry are rendered with floating-point arithmetic. The plot never interpolates a fictitious intermediate donation profile.
