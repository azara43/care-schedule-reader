---
name: "care-schedule-reader"
description: "Read photos of handwritten or printed care schedules — home-nursing monthly rosters, therapy calendars, wall calendars covered in sticky notes — and turn them into structured, confidence-tagged records with deadlines and transport arrangements extracted. Use this skill whenever the user mentions a schedule photo, a monthly roster, a care calendar, a nursing visit plan, respite or short-stay bookings, therapy appointments, pickup and drop-off arrangements, sticky notes on a calendar, or a submission deadline for next month's requests. Also use it for turning those photos into calendar events, for deadline reminders, and for daily schedule summaries."
---

# Care Schedule Reader

Turns a photo of a paper care schedule into structured records that a human can check in under a minute.

Care runs on paper. Nursing agencies fax monthly rosters. Therapy centers send printed grids. The family calendar on the kitchen wall is layered with sticky notes. Several organizations each keep their own paper, and **nobody has a view across all of them** — which is exactly where double-bookings and missed deadlines come from.

This skill does not try to replace the paper. It reads it.

## Core principle: paper is the source of truth

If the digital record and the paper disagree, **the paper wins**. Your job is to transcribe and flag, never to correct or override. When you cannot read something, say so — do not fill the gap with a plausible guess.

A wrong entry in a care schedule is worse than a missing one. A missing entry gets noticed. A wrong one gets trusted.

## Step 1: load the legend

Every household and every agency uses its own shorthand. Before reading anything, look for a legend file in this order:

1. `legend.md` in the current working directory
2. `care-legend.md` in the current working directory
3. `~/.claude/care-legend.md`

The legend maps the user's own abbreviations, symbols, staff names, and organization names to their meanings. See `legend.example.md` in this skill's directory for the format.

**If no legend file exists**, read the photo anyway, then list every symbol and abbreviation you could not interpret and offer to help the user build a legend file from them. Do not invent meanings.

## Step 2: identify what kind of paper this is

**Agency roster** — a grid issued by one organization, usually with staff names, time ranges, and a submission deadline for the following month's requests. One organization per sheet.

**Household calendar** — a month view the family maintains, mixing written entries with sticky notes. Multiple organizations appear on one sheet. Sticky notes often carry transport arrangements in a separate block.

**Mixed or unknown** — treat as a household calendar and flag the ambiguity.

## Step 3: extract deadlines first

Deadlines are the highest-consequence item on the page and the easiest to miss. Miss one and the family loses a month of requested care.

Check **both** places:

- The header or cover note (`"Please return by the 20th, 5:00 PM"`)
- Marked cells inside the grid itself (often circled)

Report every deadline with its date, time, what it is for, and where it goes. If the deadline has already passed relative to today's date, say so loudly at the top of your output.

## Step 4: extract one record per appointment

For each visit or appointment, capture:

| Field | Notes |
|---|---|
| Date | Cross-check against the printed weekday |
| Start–end time | Leave blank rather than guessing |
| Type | Nursing visit, therapy, medical, day service, respite |
| Staff | As written; do not expand initials |
| Organization | From the sheet header or the legend |
| Confidence | See below |

Keep the family's own annotations — notes about who is available to provide care, personal commitments, work shifts — in a **separate layer**. They are not appointments and must never be mixed into the appointment list.

## Step 5: tag confidence on every row

Paper schedules routinely carry confirmed and requested items in the same handwriting. Conflating them creates phantom appointments.

- **Confirmed** — printed or written on an agency roster with a time, or a recurring visit already established
- **Requested** — applications not yet granted: respite bookings, therapy date requests, anything marked as a candidate or preference, anything with a strikethrough
- **Uncertain** — you could not read it cleanly and inferred from context

Every row gets one of these three. No exceptions.

## Hard rules

These exist because each one represents a real failure mode.

1. **Never resolve illegible handwriting by guessing.** Write what you can see, mark it Uncertain, and add it to the follow-up list. `"Reads as 'M-something', possibly a staff name"` is useful. A confident wrong name is not.

2. **Never assert which day a sticky note belongs to.** Sticky notes physically shift. If a note sits between two dates, output both candidates and ask.

3. **Never treat color as meaningful** unless the legend says so. The color may encode a category, or it may be the pad that was within reach.

4. **Always report date/weekday mismatches.** If the sheet says Tuesday the 14th but the 14th is a Wednesday, surface it. These mismatches are how you catch a misplaced sticky note or a transcription error on the agency's side — this is one of the most valuable things the skill does.

5. **Never silently drop something you cannot categorize.** An unexplained mark goes in the follow-up list.

## Output format

Omit sections that have no rows. Always include the follow-up section, even when empty.

```
## ⚠️ Deadlines
| Due | For | Submit to | Days remaining |

## Confirmed
| Date | Day | Time | What | Organization / staff |

## Requested — not yet confirmed
| Date | What | Status |

## Transport
| Date | Day | Outbound | Return |

## Family availability
| Date | Time | Note |

## ❓ Needs confirmation
| Where on the page | What is legible | Question for the user |
```

## Handling common requests

**"Read this photo"** — Full output in the format above. Always end with the follow-up section.

**"Add these to my calendar"** — Add **Confirmed** rows only by default. If the user asks for requested items too, prefix each title with `[REQUESTED]` so they are visually distinct in the calendar. Never add Uncertain rows without explicit confirmation.

**"What's happening today?"** — Today's appointments, then transport, then family availability, then any deadline within the next three days. Keep it to one screen.

**"What deadlines are coming up?"** — Pull deadlines across every sheet you have read, sorted soonest first. This cross-organization view is the thing no single piece of paper provides.

## Privacy

Care schedules contain health information about a person who often cannot consent for themselves, plus the names of care staff.

- **Never transmit externally without a human in the loop.** Draft the email or message; let the user press send.
- **Restrict any drafted recipient** to the user or their household unless the user has explicitly confirmed that a given organization accepts email. Many still work by fax or paper only.
- **Do not write the person's health details into filenames, calendar event titles, or anything else that syncs broadly.** Use a short label instead.
- When the user shares a photo for troubleshooting or examples, remind them to redact names first.
