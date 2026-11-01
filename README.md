# HA Light Alerts

Turn a room's lights into a simple, color-coded alert display for Home Assistant. One script, one dashboard card, and a printable chart so anyone who walks past a window can read what the colors mean.

| Light | Meaning |
|---|---|
| Flashing red | **EVACUATE** - leave now (also sends a critical phone notification) |
| Solid purple | **STORM** - stay inside, take shelter |
| Solid cyan | **HIGH WIND** - secure outdoor items |
| Solid orange | **EXTREME HEAT** - stay cool, drink water |
| Solid green, then white | **ALL CLEAR** - also cancels a running alert |

Colors, wording and modes are all easy to change. See [Customize](#customize).

## Important safety notice

This is a convenience display. **It is not a substitute for official emergency alerts.** Keep Wireless Emergency Alerts on, use a NOAA weather radio, and follow your local authorities. Smart-home gear fails: power outages, Wi-Fi/Zigbee problems, and Home Assistant restarts can all stop the lights from working.

**Flashing lights:** the evacuation flash runs at about 1 flash per second, below the commonly cited photosensitivity threshold of 3 per second. Do not raise the flash rate, and tell household members who are photosensitive before using it.

**Color vision:** red/green and orange/yellow are hard to tell apart for many people. That is why evacuate is the only flashing mode, and why wind is cyan rather than yellow (see the [changelog](CHANGELOG.md)). Test your colors with the people who will rely on them.

## Requirements

- Home Assistant 2024.8 or newer (uses the `action:` and `perform-action` syntax)
- One or more RGB lights. Zigbee, Z-Wave, Wi-Fi or other integrations all work
- A phone with the Home Assistant Companion app, for the evacuation notification
- Optional: card-mod or UIX for colored dashboard buttons; the HA-LCARS theme for the LCARS card

## Install

1. **(Recommended) Group your bulbs.** Separate commands reach each bulb at slightly different times, so they can flash out of step. A group sends one command to all of them. In ZHA: Settings > Devices & Services > Zigbee Home Automation > Configure > Groups. Otherwise use Settings > Devices & Services > Helpers > Create helper > Group > Light group. Note the new group's entity ID.
2. **Create the script.** Settings > Automations & Scenes > Scripts > Add Script > Create new script > three-dot menu > Edit in YAML. Paste [`script/alert_lights.yaml`](script/alert_lights.yaml) and edit the `variables:` block (your light or group, your notify service). Save it as **Alert Lights** so the entity is `script.alert_lights`.
3. **Add a dashboard card.** Edit dashboard > Add card > Manual, and paste one of:
   - [`dashboard/card_plain.yaml`](dashboard/card_plain.yaml): no dependencies, no colors
   - [`dashboard/card_colored.yaml`](dashboard/card_colored.yaml): colored buttons (needs card-mod or UIX)
   - [`dashboard/card_lcars.yaml`](dashboard/card_lcars.yaml): HA-LCARS look (needs the theme and card-mod or UIX)
4. **Print the chart.** [`printable/alert_chart.pdf`](printable/alert_chart.pdf) is a one-page 8.5 x 11 chart with text sized to read from 15-20 feet. Print at 100% / "Actual size" and tape it where it's visible.
5. **Test quietly first.** See [Testing](#testing).

## Customize

All settings are in the `variables:` block at the top of the script:

| Variable | What it does |
|---|---|
| `lights` | The light or group entities to use |
| `notify_service` | Who gets the evacuation notification, e.g. `notify.mobile_app_your_phone` |
| `flash_seconds` | How long the evacuation flash runs (one flash per second) |
| `fade_seconds` | Transition time per flash step. `0` is a hard snap, but some bulbs ignore it |
| `brightness` | Brightness of the steady weather colors (1-255) |
| `colors` | `[red, green, blue]` for storm, wind and heat |

### Adding modes for your region

Different parts of the US need different alerts: tornado, hurricane, flood, wildfire smoke, winter storm or freeze, earthquake. To add one:

1. Add a color under `colors:` (for example `cold: [0, 80, 255]`).
2. Add the mode name to the `options:` list under `fields:`.
3. Add a button to your card that calls `script.alert_lights` with `mode: cold`.
4. Add a row to `ROWS` in [`printable/make_chart.py`](printable/make_chart.py) and run it to regenerate the PDF.

**Choose colors that are clearly different from each other on your actual bulbs.** Many bulbs shift colors (orange often looks yellow, blue can look purple). Look at each color from across the room, and ideally from outside, before you rely on it.

### Triggering from automations

Any automation can call the script, for example when a weather alert sensor goes active:

```yaml
action: script.alert_lights
data:
  mode: wind
```

## Testing

- Close the blinds, or use a short test run: set `flash_seconds: 6` and remove the `critical` push block, so you don't flash a window at your neighbors or set off a loud phone alert. Put them back afterwards.
- Pressing **All Clear** at any time stops a running evacuation flash (the script uses `mode: restart`).
- Check each color in daylight and at night.

## Troubleshooting

- **"Malformed" or "can't save" in the YAML editor:** an indent got shifted when pasting. Select everything, delete, paste again, and don't press Tab or Enter before saving. If it persists, paste into a text editor first and check that nothing wrapped onto a second line.
- **Comments disappeared after saving:** normal, the UI editor drops YAML comments. Keep the repo file as your reference.
- **Bulbs flash out of step:** use a light group (step 1), and replace any bulbs that ignore `transition: 0` with ones that honor it.
- **Card colors don't show:** in each `style:` line change `ha-card` to `hui-card` (newer card-mod/UIX versions).
- **No notification:** check `notify_service`. Mobile app services look like `notify.mobile_app_<device name>`; look yours up in Developer Tools > Actions.

## Files

```
script/alert_lights.yaml        the script
dashboard/card_plain.yaml       dashboard card, no dependencies
dashboard/card_colored.yaml     dashboard card, colored buttons
dashboard/card_lcars.yaml       dashboard card, HA-LCARS style
printable/alert_chart.pdf       printable color chart
printable/make_chart.py         regenerate the chart with your own colors and wording
CHANGELOG.md
LICENSE
```

## License

MIT. See [LICENSE](LICENSE).
