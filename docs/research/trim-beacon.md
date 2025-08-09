
## Trim Beacons: lightweight event capture with the Beacon API

A small, low-friction event capture system built on the browser Beacon API and Django models. Goals:

- Capture micro-events and thin stats without blocking the UI
- Send reliably on page unload using `navigator.sendBeacon`
- Store compact, queryable aggregates for fast reporting


## Design overview

We separate concerns into three conceptual layers:

1) Definition: what events exist and how they’re identified (optional, but helpful)
2) Ingest: accepting beacons with minimal overhead
3) Aggregation: rolling events into time buckets for efficient reads


### Core data shapes

- BeaconAggregate: one row per (event_type, identifier, granularity, period_start), with counters
- BeaconEvent (optional/raw): individual payloads when you need the details (error logs, custom metadata)
- BeaconDefinition (optional/config): declares valid event types, identifiers, retention, and bucketing rules

This allows both high-level reporting and—when needed—deeper inspection.


## Time-bucket aggregation (formerly “datetime bulking”)

Instead of storing every hit, we increment counters in coarse-grained buckets. For example:

1) Receive an event
2) Compute keys for second, minute, hour, day, month, year
3) Upsert counters for the requested granularities

You can choose which granularities to maintain. Commonly day + hour is enough for reporting; second/minute are optional for high-traffic or diagnostics.

Rollups can be hierarchical or direct:

- Hierarchical: second rolls into minute, minute into hour, hour into day…
- Direct: increment each selected granularity at ingest time (simpler, avoids later jobs)

“Live” records are one-per-period per (event_type, identifier). With second granularity, worst case is up to 60 writes per minute for a single identifier; for most apps, day/hour is appropriate.


## Example flow

1) User visits a page
2) A beacon posts a tiny payload to the server
3) The server resolves the identifier (e.g., page path, session, user) and upserts aggregates for the selected buckets
4) Periodically (optional), raw events are drained/compacted, and old aggregates are archived


## Minimal Django models (sketch)

These reflect the shapes above and can be adapted to project conventions.

```python
from django.db import models

class BeaconGranularity(models.TextChoices):
    SECOND = "S", "second"
    MINUTE = "M", "minute"
    HOUR   = "H", "hour"
    DAY    = "D", "day"
    MONTH  = "MO", "month"
    YEAR   = "Y", "year"


class BeaconAggregate(models.Model):
    event_type   = models.CharField(max_length=64)
    identifier   = models.CharField(max_length=256, blank=True, default="")  # page path, user id, session id, etc.
    granularity  = models.CharField(max_length=2, choices=BeaconGranularity.choices)
    period_start = models.DateTimeField()  # aligned to the bucket boundary (e.g., start of day)
    count        = models.PositiveBigIntegerField(default=0)
    meta         = models.JSONField(blank=True, null=True)  # optional, keep small

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["event_type", "identifier", "granularity", "period_start"],
                name="uniq_beacon_aggregate_bucket",
            )
        ]
        indexes = [
            models.Index(fields=["event_type", "granularity", "period_start"]),
            models.Index(fields=["identifier", "granularity", "period_start"]),
        ]


class BeaconEvent(models.Model):  # optional raw storage
    event_type = models.CharField(max_length=64)
    identifier = models.CharField(max_length=256, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    payload    = models.JSONField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    ip_hash    = models.CharField(max_length=64, blank=True)  # if you need dedupe or abuse detection
```


## Ingest API

Keep the write path minimal and robust to page unloads.

- Endpoint: POST /beacon (CSRF-exempt)
- Body: `Content-Type: application/json` or `text/plain` (Beacon will send either)

Example payload:

```json
{
  "event_type": "page_view",
  "identifier": "/docs/home",
  "meta": {"ref": "utm:home"}
}
```

Server responsibilities:

- Validate `event_type`
- Derive `identifier` when absent (e.g., from Referer or path segment)
- Upsert `BeaconAggregate` for chosen buckets (e.g., hour and day)
- Optionally store `BeaconEvent` for specific event types (errors, custom analytics)


## Client usage

HTML/JS example:

```html
<script>
  window.addEventListener('load', function () {
    const data = {
      event_type: 'page_view',
      identifier: location.pathname,
      meta: { ref: document.referrer || null }
    };
    const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
    navigator.sendBeacon('/beacon', blob);
  });
  // Custom events: navigator.sendBeacon('/beacon', new Blob([JSON.stringify({event_type:'download_click', identifier:'doc-123'})], {type:'application/json'}));
</script>
```


## Querying aggregates

Common reporting queries become cheap:

- Monthly page views for a page:
  - Filter: event_type=page_view, identifier=/docs/home, granularity=MONTH
- Daily trend for the last 30 days:
  - Filter: event_type=page_view, granularity=DAY, period_start in range
- Top pages this week:
  - Filter: event_type=page_view, granularity=DAY, period_start in week; group by identifier; sum(count)


## Performance and failure considerations

- Upserts: use database-native UPSERT (e.g., PostgreSQL `ON CONFLICT DO UPDATE`) to avoid races
- Idempotency: consider a lightweight request hash for dedupe in high-churn custom events
- Back-pressure: drop raw events first; never block page unload
- Clock skew: compute bucket boundaries on the server using received-at time
- Bot noise: filter via user-agent heuristics or challenge lists


## Privacy and compliance

- Default to no PII in payloads; prefer opaque identifiers (hash session/user id)
- Provide retention policies per event_type (e.g., raw events 7 days, aggregates 12 months)
- Disclose usage and honor consent where required


## Variations and extensions

- Identifier strategy: page path, canonical URL, session id, user id, site section, or custom key
- Aggregation policy per event_type: e.g., page_view -> day/hour; error -> minute/hour
- Transport: Beacon API primarily; fall back to `fetch(..., keepalive:true)` when Beacon is unavailable
- Fast path: optionally use Redis/in-memory counters and periodically flush to DB if throughput demands


## Example: page visits

With `event_type=page_view` and `identifier=location.pathname`, you get compact per-page counters across chosen buckets. Rendering a month view becomes fetching ~30 rows and plotting `count` over `period_start`.


## Example: error tracking

Store raw `BeaconEvent` for `event_type=error` with stack/message fields under `payload`. Aggregate by hour/day to drive alerts and dashboards.


## Beacon registry (optional)

Creators can register expected event types and defaults:

- Allowed identifiers and how to derive them
- Default granularities and retention windows
- Whether raw events are retained

This provides guardrails and consistent behavior across an app.


---

This document proposes a pragmatic, low-overhead approach to event capture in Django using the Beacon API. It prioritizes write-path reliability, compact aggregates for fast reads, and extensibility for richer use cases when needed.

