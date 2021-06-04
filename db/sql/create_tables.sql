CREATE TABLE IF NOT EXISTS iot_telemetry (
    env_id SERIAL PRIMARY KEY,
    ts DOUBLE PRECISION NOT NULL,
    device CHAR(17) NOT NULL,
    co DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    light SMALLINT,
    lpg DOUBLE PRECISION,
    motion SMALLINT,
    smoke DOUBLE PRECISION,
    temp DOUBLE PRECISION
);
CREATE TABLE IF NOT EXISTS device_00 (
    device_00_id SERIAL PRIMARY KEY,
    ts DOUBLE PRECISION NOT NULL,
    device CHAR(17) NOT NULL,
    co DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    light BOOLEAN,
    lpg DOUBLE PRECISION,
    motion BOOLEAN,
    smoke DOUBLE PRECISION,
    temp DOUBLE PRECISION
);
CREATE TABLE IF NOT EXISTS device_1c (
    device_1c_id SERIAL PRIMARY KEY,
    ts DOUBLE PRECISION NOT NULL,
    device CHAR(17) NOT NULL,
    co DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    light BOOLEAN,
    lpg DOUBLE PRECISION,
    motion BOOLEAN,
    smoke DOUBLE PRECISION,
    temp DOUBLE PRECISION
);
CREATE TABLE IF NOT EXISTS device_b8 (
    device_b8_id SERIAL PRIMARY KEY,
    ts DOUBLE PRECISION NOT NULL,
    device CHAR(17) NOT NULL,
    co DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    light BOOLEAN,
    lpg DOUBLE PRECISION,
    motion BOOLEAN,
    smoke DOUBLE PRECISION,
    temp DOUBLE PRECISION
);