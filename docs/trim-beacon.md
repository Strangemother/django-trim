
# Beacons

A simple recording feature for small event capture, using JS Beacon API and django models.

1. Capture thin statistics, events, micro tracking 
2. Use the Beacon API to send data asynchronously
3. Store data in Django models for later analysis

The modelling should have two facets.

+ A `Beacon` model that captures the event type, timestamp, and any additional metadata. 
+ A `BeaconData` model that captures the actual data sent by the Beacon API, linked to the `Beacon` model.

This can build bulk data objects, such as page visits over the year. 
Alternatvely we may prefer something more granular, such as per session or per user.

In the second form, we consider the _event parent_ as the group. It can be a page/site/username. This allows us to aggregate data by user or session, providing insights into user behavior over time.


---

## Datetime bulking 

To handle datetime bulking, we can implement a method that aggregates data based on a specified time interval (e.g., daily, weekly, monthly). This will allow us to analyze trends over time without overwhelming the database with individual records.

The format for datetime bulking could be as follows:

1. recieve an event
2. append to a counter for _second_, _minute_, _hour_, _day_, etc...
3. After a certain threshold, bulk the data into a single record

The _parent_ record can refer to its child data, allowing us to maintain a hierarchy of events. However to lessen the load, datetime bulking can be done 
by aggregating data into a single record for each time interval, rather than storing every individual event.

Eventually a _year_ would all months, days, hours, minutes, seconds, etc... rolled up into a single record.

Therefore _live_ records (the aggreate model) is _one_ per period. Given a mminimum of 1 second, this would mean a maximum of 60 writes per minute, but then one minute, one, day, one month, and one.

---

Example flow.

1. User x99 visits a page 
2. A beacon is triggered, sending data to the server

The event is split into the datetime constituents: second, minute, hour, day, month, year. These values are then aggregated into a single record for each time interval.

At user 100 the record is bulked into a single record for the day, month, and year. 

When a period completes, the data is rolled up into a single record for that period, and stored into the parent. 

For example, if the user visits a page every second for 60 seconds, the data is aggregated into a single record for that minute.
Then every minute is aggregated into a single record for that hour, and so on.

Every-so-often, the live count is _drained_ to somehwere persistent, such as a database or file, ensuring minimal count _loss_ if the server crashes.

---

example:

A beacon event looks like this:

html:

```html
<script>
  navigator.sendBeacon('/my-beacon/page/100');
</script>
```

### Ideas

#### Page Visits

This makes it extremely easy for heuristic analysis, as we can simply query the database for the aggregated data. For example, showing visits over a month is one 30 field result, then each day is one ~31 field result etc.

To gain the _data_ for a day, we can use the datetime to match the metadata.

### Custom Events

Events such as "download button clicked" is super easy with a simple beacon tracking the unique event name (no setup required).

### Session Tracking

Session tracking can be implemented by using a session ID as the identifier for the beacon. The developer may assign a custom ID.

### Error Events

Error events can be captured by sending a beacon with the error details, such as the error message, stack trace, and any relevant metadata. This allows for easy tracking and analysis of errors in the application.

Plug in emails or other notification systems to alert developers of critical errors.

### User Actions

User actions can be tracked by sending a beacon with the action details, such as the action type (e.g., click, scroll, form submission) and any relevant metadata. This allows for easy tracking of user interactions with the application.


## Identifier 

The _identifier_ for the beacon can be a page/username/session ID... Anything that the creator prefers. They assign the setup through the possible beacon fields. Any meta-data is stored on the single record. 

Notable _single record data_ cannot be applied to bulk counters, as the aggragation would lead to a large bulk store.

Instead, for specific events, we can bridge the data to a separate model, such as `BeaconData`, which can store additional metadata or specific event details.

---

A Page beacon would be design to count page visits per minute etc. Each visit is _not_ a separate record, applied as a count. 

To track unique user flows, we can use a session ID or user ID as the identifier. This allows us to track unique visits and aggregate data accordingly. 

## Beacon Register

A creator will register an expected beacon event, such as "page". This will capture the beacon, with processing, and store the data in the database.

This parent can contain the _totaling_ record, for all children. A creator may wish to register a setup for all pages. This would be a bulk-like record:

