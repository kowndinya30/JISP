# JISP database container — PostgreSQL 16 + TimescaleDB + PostGIS.
#
# The Timescale "-ha" image already bundles PostGIS and the required
# extensions; no custom installation needed. Schema / extensions SQL
# will be mounted in a later step (when `spatial/db/` grows real DDL).
#
# Not active in Step 4's compose stack — Dockerfile exists per the
# approved folder structure and will be activated once ingestion /
# spatial / timeseries begin writing data.

FROM timescale/timescaledb-ha:pg16

# Default port — unchanged from the base image, declared for documentation.
EXPOSE 5432
