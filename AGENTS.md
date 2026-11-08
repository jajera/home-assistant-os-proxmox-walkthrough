# Agent notes

Zensical walkthrough: **Home Assistant OS as a VM on Proxmox VE**, from the
official KVM/Proxmox qcow2 through the onboarding welcome screen.

## Commands

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/zensical serve
```

## Docs

Reading order matches `zensical.toml` nav. Use `<div class="run" markdown>` for
command + result pairs (see patina `.run` CSS). No “Looks like” labels.

Consume [Proxmox VE walkthrough](https://proxmox-ve-walkthrough.johna.kiwi/) for
host prep. Do not re-document ISO install, ZFS vs ext4 host disks, or apt
enterprise vs no-subscription.

## Non-negotiables

1. Stay generic — consumers set hostname, VMID, and guest details. Docs use
   dummy `pve.home.arpa` / `192.168.1.60` and guest `192.168.1.70`.
2. Official **HAOS KVM/Proxmox `.qcow2`** only. No Supervised, Container, or
   community helper scripts as the primary path.
3. **Secure Boot off** — untick Pre-Enroll keys on the EFI disk.
4. Keep storage as **tabs** only at the three branch points (What you need,
   Create VM System, Import disk). Labels match the Proxmox guide:
   “Two disks: ZFS mirror” / “One disk: ext4”. Do not fork the pages.
5. Do not commit qcow2/xz/ISO images, passwords, API tokens, or private keys.
