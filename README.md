# home-assistant-os-proxmox-walkthrough

Home Assistant OS as a VM on Proxmox VE — from the official qcow2 through
onboarding.

Docs: [home-assistant-os-proxmox-walkthrough.johna.kiwi](https://home-assistant-os-proxmox-walkthrough.johna.kiwi/)

Prerequisite host prep: [Proxmox VE walkthrough](https://proxmox-ve-walkthrough.johna.kiwi/)

## Docs locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/zensical serve
```

Open the URL printed by the server (usually `http://127.0.0.1:8000`).

## Scope

Generic guest install on a web-UI-ready Proxmox host. Hostname, VMID, and
lab-specific follow-ups (add-ons, Zigbee mesh, reverse proxy) belong in the
consuming walkthrough — not here.

See [AGENTS.md](AGENTS.md).
