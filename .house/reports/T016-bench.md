| profile | set | workers | docs | F1 exact | F1 norm | reject acc | false rejects | p50 s | p95 s | docs/min | peak RSS MB | model MB | OCR cache |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ocr | heldout | 2 | 60 | 0.9986 | 0.9986 | - | 0 | 0.12 | 1.75 | 180.1 | 329 | 30 | warm |
| ocr | skany | 2 | 30 | 0.9639 | 0.9639 | - | 0 | 0.04 | 0.38 | 516.3 | 153 | 30 | warm |
| ocr | negatywne | 2 | 12 | - | - | 100.0% | - | 1.30 | 4.26 | 55.6 | 312 | 30 | warm |
| llm | heldout | 2 | 60 | 0.9986 | 0.9986 | - | 0 | 0.18 | 118.87 | 11.4 | 5111 | 1780 | warm |
| llm | skany | 2 | 30 | 0.9707 | 0.9707 | - | 0 | 0.04 | 128.66 | 6.9 | 4973 | 1780 | warm |
| llm | negatywne | 2 | 12 | - | - | 100.0% | - | 1.21 | 3.61 | 63.3 | 313 | 1780 | warm |
