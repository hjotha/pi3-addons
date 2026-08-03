# Graph Report - .  (2026-08-03)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 17 nodes · 17 edges · 9 communities (3 shown, 6 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.5)
- Token cost: 213 input · 83 output

## Graph Freshness
- Built from commit: `31c7e445`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- System Control Menu
- Temperature Display Logic
- Fan Control
- App Indicator Library
- Addons Quickstart Guide
- Image Drawing
- Addons Documentation
- Temperature Measurement

## God Nodes (most connected - your core abstractions)
1. `update_fan()` - 4 edges
2. `get_temperature()` - 3 edges
3. `fan_off()` - 3 edges
4. `update_temperature()` - 3 edges
5. `quit()` - 3 edges
6. `fan_on()` - 2 edges
7. `create_indicator_image()` - 2 edges
8. `build_menu()` - 2 edges
9. `RPi.GPIO` - 1 edges
10. `pi3-addons README` - 0 edges

## Surprising Connections (you probably didn't know these)
- `update_fan()` --calls--> `get_temperature()`  [EXTRACTED]
  temp-applet.py → temp-applet.py  _Bridges community 1 → community 2_
- `update_fan()` --calls--> `fan_off()`  [EXTRACTED]
  temp-applet.py → temp-applet.py  _Bridges community 0 → community 2_

## Import Cycles
- None detected.

## Communities (9 total, 6 thin omitted)

### Community 0 - "System Control Menu"
Cohesion: 0.47
Nodes (4): RPi.GPIO, build_menu(), fan_off(), quit()

### Community 1 - "Temperature Display Logic"
Cohesion: 0.67
Nodes (3): create_indicator_image(), get_temperature(), update_temperature()

## Knowledge Gaps
- **6 isolated node(s):** `pi3-addons README`, `pi3-addons Quickstart`, `vcgencmd measure_temp`, `RPi.GPIO`, `gi.repository.AppIndicator3` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `update_fan()` connect `Fan Control` to `System Control Menu`, `Temperature Display Logic`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `get_temperature()` connect `Temperature Display Logic` to `System Control Menu`, `Fan Control`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Why does `fan_off()` connect `System Control Menu` to `Fan Control`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **What connects `pi3-addons README`, `pi3-addons Quickstart`, `vcgencmd measure_temp` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._