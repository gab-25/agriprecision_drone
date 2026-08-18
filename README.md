# agriprecision_drone
AgriPrecision Drone

## Development

Requirements: [uv](https://docs.astral.sh/uv/), Docker with Docker Compose.

```bash
cp .env.example .env          # then fill in the database credentials
docker compose up -d          # start PostgreSQL 18 + PostGIS 3.6
uv sync                       # install Python dependencies
uv run python manage.py migrate
uv run python manage.py runserver
```

`.env` drives both Docker Compose and Django settings: `POSTGRES_DB`, `POSTGRES_USER`
and `POSTGRES_PASSWORD` create and authenticate against the database, while `DB_HOST`
(`localhost`) and `DB_PORT` (`5432`) tell Django where to reach it. Change `DB_PORT` if
port 5432 is already taken on the host.

The database runs as the `postgres` service defined in [compose.yaml](compose.yaml), with
data stored in the named volume `pgdata` — it survives `docker compose down`; use
`docker compose down -v` to wipe it.

Note that the credentials in `.env` are only applied when the database is initialized:
the Postgres entrypoint runs `initdb` on an empty data directory only. After changing
`POSTGRES_DB`, `POSTGRES_USER` or `POSTGRES_PASSWORD`, recreate the volume with
`docker compose down -v && docker compose up -d`.

### Geometries and area

Geometries are stored as GeoJSON in a `JSONField`, so no GDAL/GEOS libraries are needed on
the Python side. `Workspace.polygon` must hold a bare GeoJSON *geometry* object
(`{"type": "Polygon", "coordinates": [...]}`) — a `Feature` or `FeatureCollection` is
rejected by PostGIS and makes the insert fail.

`Workspace.area` is a PostgreSQL generated column (`STORED`), computed by PostGIS as
`ST_Area(ST_GeomFromGeoJSON(polygon)::geography) / 10000`, i.e. **hectares** measured on
the spheroid. It is read-only from Django: assigning to it has no effect, the value is
always recomputed by the database whenever `polygon` changes.

The PostGIS extension is available through raw SQL:

```bash
docker compose exec postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT postgis_version();"
```
