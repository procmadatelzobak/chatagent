# API

All endpoints are served under the `/api` prefix except for `/health`.

## `GET /health`
Returns service status.
```json
{"status": "ok"}
```

## `GET /api/scenarios`
List available scenarios.
```json
{ "scenarios": ["demo"] }
```

## `POST /api/scenarios/load`
Load a scenario by name.

Request:
```json
{ "name": "demo" }
```
Response:
```json
{
  "name": "demo",
  "tick": 0,
  "data": {"counter": 0}
}
```

## `POST /api/play`
Start the simulation.
```json
{"status": "playing"}
```

## `POST /api/pause`
Pause the simulation.
```json
{"status": "paused"}
```

## `POST /api/step`
Advance the simulation by `ticks`.

Request:
```json
{"ticks": 3}
```
Response:
```json
{"tick": 3, "data": {"counter": 3}}
```

## `GET /api/state`
Fetch the current state.
```json
{"tick": 3, "data": {"counter": 3}}
```

## `GET /api/state/export`
Export the current state. Same shape as `GET /api/state`.

## `POST /api/checkpoint`
Load checkpoint data into the current state.

Request:
```json
{"state": {"counter": 10}}
```
Response:
```json
{"status": "loaded"}
```

Errors return appropriate HTTP status codes and a JSON body with a `detail` field.
