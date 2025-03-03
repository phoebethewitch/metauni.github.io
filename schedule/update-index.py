#!/usr/bin/env python
import os
import yaml

BEGIN_WHATS_ON = "<!-- BEGIN WHATS ON -->"
END_WHATS_OFF = "<!-- END WHATS OFF -->"
BEGIN_WHATS_OFF = "<!-- BEGIN WHATS OFF -->"
END_WHATS_ON = "<!-- END WHATS ON -->"

def seminar_to_markdown(seminar):
    name = next(iter(seminar))
    data = seminar[name]

    time = data.get("time")
    organizer = data.get("organizer")
    desc = data.get("desc")
    note = data.get("note")
    website = data.get("website")
    location = data.get("location")

    text = "* "
    if website:
        text += f"**[{name}]({website})**"
    else:
        text += f"**{name}**"
    if time:
        text += f" **{time}**"
    if organizer:
        text += f" (*{organizer}*)"
    if desc or note:
        text += ":"
        if desc:
            text += f" {desc}"
        if note:
            text += f" {note}"

    return text

# Load schedule.yml into dictionary
schedule = None
with open(os.environ["SCHEDULE_PATH"], "r", encoding="utf-8") as f:
    schedule = yaml.safe_load(f)

# Generate markdown for seminars
whats_on_md = ""
whats_off_md = ""
for seminar in schedule["whats on"]:
    whats_on_md += seminar_to_markdown(seminar) + "\n"
for seminar in schedule["whats off"]:
    whats_off_md += seminar_to_markdown(seminar) + "\n"

# Insert generated markdown into index.md
with open("index.md", "r+", encoding="utf-8") as f:
    lines = []
    inside_tags = False # Used to skip over existing what's on text

    # TODO: Throw if the tags don't exist

    for line in f.readlines():
        if line.startswith(BEGIN_WHATS_ON):
            inside_tags = True
            lines.append(f"{BEGIN_WHATS_ON}\n{whats_on_md}{END_WHATS_ON}\n")
        elif line.startswith(BEGIN_WHATS_OFF):
            inside_tags = True
            lines.append(f"{BEGIN_WHATS_OFF}\n{whats_off_md}{END_WHATS_OFF}\n")
        elif line.startswith(END_WHATS_ON):
            inside_tags = False
        elif line.startswith(END_WHATS_OFF):
            inside_tags = False
        elif not inside_tags: # Skips over lines between BEGIN and END tags
            lines.append(line)

    f.seek(0) # Move cursor to start of file
    f.truncate(0) # Clear file
    f.writelines(lines)