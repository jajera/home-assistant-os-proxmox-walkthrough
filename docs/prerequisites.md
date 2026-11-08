# What you need

!!! note "Do the host guide first"
    Complete the whole
    [Proxmox VE walkthrough](https://proxmox-ve-walkthrough.johna.kiwi/) —
    ISO → install → first boot → update host → prove web UI. Stop when that
    guide’s web UI check works, then return here.

| Item | Detail |
| --- | --- |
| Proxmox host | Web UI on `:8006`, `kvm_ok`, updated packages |
| Free VM storage | About 34 GB on `local-zfs` or `local-lvm` |
| Temp space | About 1 GB on `local` (`/var/lib/vz`) for the download |
| RAM to spare | 4 GB for the guest (plus headroom for the host) |
| Workstation | Same LAN as the host, browser for the UIs |
| Shell | Root on the Proxmox node (SSH or **Node → Shell**) |

## Pick your storage

Match the layout you chose in the Proxmox guide.

=== "Two disks: ZFS mirror"

    VM disks live on `local-zfs`. Confirm:

    <div class="run" markdown>

    ```bash
    pvesm status
    ```

    ```text {.no-copy}
    Name             Type     Status     Total (KiB)      Used (KiB) Available (KiB)        %
    local             dir     active       …
    local-zfs     zfspool     active       …
    ```

    </div>

    Set `STORAGE=local-zfs` for the import step.

=== "One disk: ext4"

    VM disks live on `local-lvm`. Confirm:

    <div class="run" markdown>

    ```bash
    pvesm status
    ```

    ```text {.no-copy}
    Name             Type     Status     Total (KiB)      Used (KiB) Available (KiB)        %
    local             dir     active       …
    local-lvm     lvmthin     active       …
    ```

    </div>

    Set `STORAGE=local-lvm` for the import step.

## Values this guide uses

Change them to suit. Pick a free VMID with `pvesh get /cluster/nextid`.

| Setting | Example |
| --- | --- |
| Proxmox UI | `https://192.168.1.60:8006/` (`pve.home.arpa`) |
| VM name / VMID | `haos` / `100` |
| Guest RAM / vCPU | 4096 MiB / 2 (`host`) |
| Guest example IP | `192.168.1.70` (DHCP; prefer `homeassistant.local`) |
| HAOS image | `haos_ova-18.5.qcow2.xz` |

## Next

[Download image](download.md){ .md-button }
