# Goose Clicker

A frenetic tap-the-goose browser game. Each tap builds tempo, the goose shrinks under pressure, and when the tension reaches critical mass — **BOOM**. The goose explodes in a shower of feathers and sparks, awarding a 500-point bonus, then respawns ready for another round.

The further you push, the smaller the goose gets, the redder the screen glows, and the louder the crowd (of one goose) cheers. Beat-driven motivational messages escalate from gentle encouragement to full alarm mode. Every 100 points earns a praise banner. The goose will also get sad if you ignore it for too long.

## About this project

> This game was created entirely by an AI agent, without human code authorship. All game logic, art direction, anti-cheat algorithm, and this README were generated autonomously. The original Android version was ported to the web by the same AI. Use at your own amusement.

## Features

- **Tempo system** — tap speed builds a 0–100% pressure meter; at 100% the goose explodes
- **Explosion & respawn** — satisfying particle burst + feather shower + screen flash; +500 bonus points
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
- **Long-press the title** ("Goose Clicker") to open the credits dialog.
- **EN / RU button** (bottom-right corner) to switch language.

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

[MIT](LICENSE) — Copyright (c) 2026 Goose Clicker Contributors

---

🪿 Quack.
