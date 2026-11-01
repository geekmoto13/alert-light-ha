# Changelog

## 1.0.0

First public release.

- Script with five modes: evacuate (flashing red plus a critical notification), storm, wind, heat, and all clear
- Dashboard cards: plain, colored, and HA-LCARS
- Printable 8.5 x 11 chart readable from 15-20 feet, plus a generator script

### Design notes from the prototype

- **Wind changed from yellow to cyan.** In testing, yellow (wind) and orange (heat) looked almost the same on RGB bulbs, and other people would likely confuse them too. Cyan is clearly different from every other mode. The first printed chart used yellow; the current one uses cyan.
- **Bulbs are grouped.** Commands sent to three separate Zigbee bulbs landed a fraction of a second apart, which was visible as out-of-step flashing, especially out of the corner of the eye. Sending one command to a group made the flash much more consistent.
- **Transition 0.** A transition of 0 gives the crispest flash, but some bulbs ignore it. Bulbs that honor it flash in step; others lag slightly.
