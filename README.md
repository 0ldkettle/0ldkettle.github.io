# Goose Clicker

A frenetic tap-the-goose browser game. Each tap builds tempo, the goose shrinks under pressure, and when the tension reaches critical mass — **BOOM**. The goose explodes in a shower of feathers and sparks, awarding a 10,000-point bonus, then respawns ready for another round.

The further you push, the smaller the goose gets, the redder the screen glows, and the louder the crowd (of one goose) cheers. Beat-driven motivational messages escalate from gentle encouragement to full alarm mode. Every 100 points earns a praise banner. The goose will also get sad if you ignore it for too long.

## About this project

> This game was created entirely by an AI agent, without human code authorship. All game logic, art direction, anti-cheat algorithm, and this README were generated autonomously. Use at your own amusement.

## Designed for mobile

Goose Clicker is built **mobile-first**. It plays best on a phone or tablet — most of the interactions assume a touchscreen, and several only work there:

- **Touchscreen required for the full experience.** Single taps work on desktop, but tempo, drag-fling, multi-touch easter eggs, and shake gestures are tuned for fingers.
- **Gyroscope / motion sensor.** Shaking the device feeds the tempo (each shake counts as a virtual tap) and bumps the goose against the screen edges. On iOS Safari you must grant motion permission via the in-game 📳 button on first launch.
- **Multi-touch.** Several effects react to having more than one finger on screen at once — including a 5-finger easter egg.
- **Haptics.** Vibration patterns fire on tap, milestone, and explosion where the browser exposes the Vibration API.

Desktop mouse play is supported as a fallback, but you'll be missing shake, multi-touch, and haptics.

## Features

- **Tempo system** — tap speed builds a 0–100% pressure meter; at 100% the goose explodes
- **Explosion & respawn** — satisfying particle burst + feather shower + screen flash; +10,000 bonus points
- **Anti-cheat v5.1** — five detection signatures (interval CV, spread, spatial clustering, rolling window) penalise bot-like input with a score deduction and a 3-second cooldown
- **Particles** — sparks, feathers, and ripple rings; secondary and tertiary bursts on explosion
- **Heat background** — red-alert overlay intensifies as tempo climbs; pulsing vignette at critical level
- **Haptics** — vibration patterns on tap, milestone, and explosion (mobile browsers)
- **Motivational messages** — four tiers (start / mid / high / boom) with randomised pick from pools
- **i18n EN / RU** — full English and Russian UI; language toggle persists via `localStorage`
- **Persistent score** — score and explosion count survive page reloads via `localStorage`
- **Single-file** — zero dependencies; pure HTML + CSS + JS

## Play Online

`https://0ldkettle.github.io/`

Once deployed, it lives at the URL above.

## Local Development

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Or just open `index.html` directly in a browser. No build step required.

## Controls

- **Tap / click the goose** to add tempo and score points.
- **Drag the goose** with your finger to fling it; hard wall hits award bonus points.
- **Shake the device** to feed tempo and bump the goose against the screen edges (mobile only; iOS asks for motion permission via the 📳 button on first launch).
- **Long-press the mute button** to open the credits dialog.
- **EN / RU button** (bottom-right corner) to switch language.

## Tuning the Explosion

The explosion difficulty is controlled by a **three-zone rate model** defined near the top of `index.html` (search for `Tempo model`). Each frame the game counts taps in a sliding 1-second window (`tapsPerSec`) and adjusts the 0–1 tempo bar based on which zone you're in:

| Zone              | Condition                                         | Effect on tempo                       |
| ----------------- | ------------------------------------------------- | ------------------------------------- |
| **Drop**          | `tapsPerSec < TEMPO_DECAY_BELOW`                  | Falls at `TEMPO_DECAY_PER_SEC` / sec  |
| **Hold (dead)**   | `TEMPO_DECAY_BELOW ≤ tapsPerSec < TEMPO_GROW_AT`  | Stays put                             |
| **Grow**          | `tapsPerSec ≥ TEMPO_GROW_AT`                      | Rises at `TEMPO_GROW_PER_SEC` / sec   |

The goose explodes when tempo reaches `TEMPO_EXPLODE = 1.0`.

### Knobs

- **`TEMPO_DECAY_BELOW`** — tps threshold below which the bar drains. Lower = more forgiving.
- **`TEMPO_GROW_AT`** — tps threshold you must hit to make progress. Higher = harder.
- **`TEMPO_GROW_PER_SEC`** — how fast the bar fills when in the grow zone. Minimum taps to explode from zero ≈ `TEMPO_GROW_AT / TEMPO_GROW_PER_SEC`.
- **`TEMPO_DECAY_PER_SEC`** — how fast the bar drains when in the drop zone. Time from full to empty = `1 / TEMPO_DECAY_PER_SEC` seconds.
- **`TEMPO_RATE_WINDOW_MS`** — sliding-window length for the tps count. Keep at `1000` unless you want sub-second responsiveness.

The tap-rate chip at the bottom-right shows `current / all-time max` tps. **Long-press the chip** to reset the max. It turns pink when you're in the grow zone.

### Example calibrations

| Goal                          | `DECAY_BELOW` | `GROW_AT` | `GROW_PER_SEC` | Min taps to explode |
| ----------------------------- | -------------:| ---------:| --------------:| -------------------:|
| Relaxed                       | 10            | 15        | 0.15           | ≈100               |
| Current (Apr 2026)            | 22            | 28        | 0.11           | ≈255               |
| Brutal                        | 35            | 45        | 0.08           | ≈565               |

After changing any of these, bump `CACHE` in `sw.js` (e.g. `v57` → `v58`) so PWA clients pick up the new build immediately.

## Anti-Cheat Notes

Anti-cheat v5.1 monitors the last 12 tap intervals and positions and flags five patterns:

1. **Low coefficient of variation** — interval standard deviation / mean < 0.10 at fast pace
2. **Tiny interval spread** — max − min ≤ 20 ms across the full buffer at fast pace
3. **Recent window spread** — same check on the latest 5 taps (threshold 10 ms)
4. **Spatial clustering (full buffer)** — all 12 tap positions within a 50 px radius at fast pace
5. **Spatial clustering (recent window)** — latest 5 taps within a 35 px radius at fast pace

Detection deducts 50 points, resets tempo to zero, and suppresses taps for 3 seconds.

## Credits

**Sound:** "Duck Quack" by *qubodup* — [freesound.org/s/442820/](https://freesound.org/s/442820/)
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
Remixed from "20130403_duck.04.wav" by *dobroide* (CC BY 3.0)

**Goose icon:** AI-generated

## License

[MIT](LICENSE) — Copyright (c) 2026 0ldkettle

---

🪿 Quack.
