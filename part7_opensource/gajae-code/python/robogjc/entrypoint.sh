#!/usr/bin/env bash
# robogjc container entrypoint. No per-boot pip installs — everything is baked
# into the image; we only sanity-check the runtime mount and create state dirs.
#
# Used by both the orchestrator (CMD: `python -m robogjc serve`) and the
# sibling gh-proxy (compose command: `python -m robogjc.proxy serve`). The
# proxy role does NOT need a $PI_ROOT pi checkout — it never runs gjc.
set -euo pipefail

# Shared git metadata under /data/workspaces/_pool is intentionally group
# writable by the `gjc` group so interrupted work can resume on a different
# slot user. Keep new files and directories compatible with that model.
umask 0002

# Detect the proxy role by inspecting the command. Compose passes `command:`
# as $@ here (after tini --), so $1=python, $2=-m, $3=robogjc.proxy is the
# canonical shape; we also accept a single concatenated arg for safety.
is_proxy_role=0
if [ "${1:-}" = "python" ] && [ "${2:-}" = "-m" ] && [[ "${3:-}" == robogjc.proxy* ]]; then
    is_proxy_role=1
elif [[ "${1:-}" == *"robogjc.proxy"* ]]; then
    is_proxy_role=1
fi

/usr/sbin/groupadd -f -g 2000 gjc
max_slots="${ROBGJC_MAX_CONCURRENCY:-8}"
for i in $(seq 1 "$max_slots"); do
    user="gjc-$i"
    slot_group="gjc-$i"
    slot_id=$((2000 + i))
    /usr/sbin/groupadd -f -g "$slot_id" "$slot_group"
    id -u "$user" >/dev/null 2>&1 || /usr/sbin/useradd -u "$slot_id" -g "$slot_group" -G gjc -M -N -s /usr/sbin/nologin "$user"
    /usr/sbin/usermod -g "$slot_group" -a -G gjc "$user"
done

if [ "$is_proxy_role" -eq 1 ]; then
    exec "$@"
fi

: "${PI_ROOT:=/work/pi}"
if [ ! -d "$PI_ROOT/packages/coding-agent" ]; then
    echo "robogjc: PI_ROOT=$PI_ROOT does not look like a pi checkout (no packages/coding-agent/)" >&2
    exit 1
fi

mkdir -p /data/workspaces /data/workspaces/_pool /data/logs
# Persistent build caches under the /data volume. CARGO_HOME,
# CARGO_TARGET_DIR, and RUSTUP_HOME are pinned to these paths in the image ENV
# so every per-issue worktree shares one cargo target/toolchain. Bun install
# cache is workspace-private; a shared cache is unsafe across slot users
# because bun may chmod/chown its cache root to the first writer.
mkdir -p /data/cache/cargo /data/cache/cargo-target /data/cache/rustup /data/cache/pi-natives
chown -R root:gjc /data/cache /data/workspaces/_pool
find /data/cache /data/workspaces/_pool -type d -exec chmod 2770 {} +
find /data/cache /data/workspaces/_pool -type f -perm /111 -exec chmod 0770 {} +
find /data/cache /data/workspaces/_pool -type f ! -perm /111 -exec chmod 0660 {} +
chmod 0700 /data/logs


rm -rf /srv/agent-home/.agent /srv/agent-home/.gjc/agent
mkdir -p /srv/agent-home/.agent /srv/agent-home/.gjc/agent
if [ -e /srv/agent-home-stage/.agent ]; then
    cp -a /srv/agent-home-stage/.agent/. /srv/agent-home/.agent/
fi
if [ -e /srv/agent-home-stage/.gjc/agent ]; then
    cp -a /srv/agent-home-stage/.gjc/agent/. /srv/agent-home/.gjc/agent/
fi
chown -R root:root /srv/agent-home || true
find /srv/agent-home -type d -exec chmod 0755 {} +
find /srv/agent-home -type f -exec chmod 0644 {} +

touch /data/robogjc.sqlite
chown root:root /data/robogjc.sqlite
chmod 0600 /data/robogjc.sqlite
for db_file in /data/robogjc.sqlite-wal /data/robogjc.sqlite-shm; do
    if [ -e "$db_file" ]; then
        chown root:root "$db_file"
        chmod 0600 "$db_file"
    fi
done

exec "$@"
