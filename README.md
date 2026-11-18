# mlb-pitch-mix

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/noahowsh/mlb-pitch-mix/blob/main/pitch_mix.ipynb)

A pitcher's arsenal, what he throws in each count, and how his fastball velocity holds up inning by inning, from every pitch of a season. One Python script, MLB since 2015.

```bash
pip install -r requirements.txt
export FASTBALLAPI_API_KEY=your_key      # free: https://fastballapi.com/signup (500 credits a month)

python pitch_mix.py "Tarik Skubal" --season 2025
python pitch_mix.py "Paul Skenes" --season 2025 --csv skenes_2025.csv
```

It prints three tables:

- **Arsenal:** each pitch type's usage, average and top velocity, whiff rate per swing and ball rate.
- **By count:** the share of each pitch on the first pitch, ahead, even, behind and with two strikes. This is where a pitcher's plan shows: the pitch he trusts at 0-0 is rarely the one he finishes with.
- **Velocity by inning:** his main fastball's average speed in each inning with 20 or more of them, the simplest fatigue check there is.

The arsenal for Tarik Skubal's 2025 (real output):

```
Tarik Skubal 2025: 3,152 pitches
         name  usage  avg_velocity  max_velocity  whiff_rate  ball_rate
     Changeup  0.309          87.6            92       0.488      0.300
 Four-seam FB  0.302          97.2           102       0.291      0.293
       Sinker  0.233          96.9           101       0.189      0.272
       Slider  0.129          89.8            94       0.262      0.324
Knuckle Curve  0.022          80.7            85       0.318      0.435
        Curve  0.005          82.0            85       0.500      0.400
```

`--csv` also writes every pitch (count, inning, type, velocity, location, result) for your own analysis.

## The data

[FastballAPI](https://fastballapi.com/data/mlb-pitch-by-pitch?utm_source=github&utm_medium=readme&utm_campaign=mlb-pitch-mix) holds every MLB pitch from 2015 (about 98% of games in 2015 to 2017, every game from 2018), with the count, pitch type, velocity, location and result, plus every plate appearance with base-out state, win probability and run value.

Credits: a player search costs 1, the arsenal 5, and every pitch of a season 10 for each 2,000 pitches (about 20 for a starter's season).

## Ideas to extend it

- Compare two seasons to find who added a pitch or lost velocity.
- Join to `get_plate_appearances` for what happened at the end of each at-bat, and find each pitcher's put-away pitch.
- Run it for a whole rotation with `list_teams` and `get_player`.

Uses the [fastballapi](https://pypi.org/project/fastballapi/) Python client (no dependencies). FastballAPI is also a hosted MCP server for Claude, ChatGPT and Cursor: https://fastballapi.com/mcp?utm_source=github&utm_medium=readme&utm_campaign=mlb-pitch-mix

MIT licensed.
