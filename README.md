## Log 1 - 23/04/25

##### Started with the weekly planning feature.

- Completed adding events to the calendar with end dates, notes, and its GUI.

## Log 2 - 23/04/25

##### Started with the weekly planning feature.

- Added delete functionality to each event, no bugs observed yet.

## Log 3 - 26/04/25

##### Edit functionality.

- Can edit notes and end-time now.
- Used event-binding to trigger edit event - dialouge box.
- DB is only edited if new note/time is different, instead of editing it always regardless of change.
- Auto-Destroys edit widget and Auto-Updates event widgets after clicking save.
- Events are deleted when the day ends.

## Agenda for next update

- Introduce try/error blocks.
- Introduce only one global db.connect and one db.close to minimize connection management overhead and allows for easier db transaction management.
- Remove redundant code.
- Improve GUI - labels, grid, favicon, etc.
