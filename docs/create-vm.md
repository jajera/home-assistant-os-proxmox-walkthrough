# Create VM

In the Proxmox web UI, open **Create VM**. Leave **Start after created** off —
you import the disk next.

![Create VM, General: name haos, VMID 100](assets/create-vm/01-general.jpg)

## General

Tick **Advanced** at the bottom of the wizard once. It keeps the extra fields
(Start at boot, CPU flags, memory ballooning) visible on every tab.

| Field | Value |
| --- | --- |
| Node | your Proxmox node (example `pve`) |
| VM ID | free ID (example `100`; use `pvesh get /cluster/nextid`) |
| Name | `haos` |
| Start at boot | on (shown with **Advanced** ticked) |

## OS

| Field | Value |
| --- | --- |
| ISO image | **Do not use any media** |
| Guest OS type | Linux |
| Version | Leave the default (`7.x - 2.6 Kernel` on current Proxmox VE) |

![OS tab: Do not use any media](assets/create-vm/02-os.jpg)

## System

=== "Two disks: ZFS mirror"

    Put the EFI disk on `local-zfs`.

=== "One disk: ext4"

    Put the EFI disk on `local-lvm`.

| Field | Value |
| --- | --- |
| Graphic card | Default |
| Machine | **q35** |
| BIOS | **OVMF (UEFI)** |
| Add EFI Disk | on |
| EFI Storage | `local-zfs` or `local-lvm` (match your tab) |
| Pre-Enroll keys | **off** (Secure Boot breaks HAOS) |
| SCSI Controller | **VirtIO SCSI single** |
| QEMU Guest Agent | **on** |

![System tab: q35, OVMF, Pre-Enroll keys off](assets/create-vm/03-system.jpg)

!!! danger "Pre-Enroll keys"
    Leave **Pre-Enroll keys** unticked. With Secure Boot on, HAOS fails to boot
    (UEFI “Access Denied” or a boot loop).

## Disks

Delete the wizard’s default hard disk. You attach the HAOS image in the next
page — do not keep an empty unused disk.

![Disks tab: remove the default disk](assets/create-vm/04-disks.jpg)

## CPU

| Field | Value |
| --- | --- |
| Sockets | 1 |
| Cores | 2 |
| Type | `host` |

![CPU tab: 2 cores, type host](assets/create-vm/05-cpu.jpg)

## Memory

| Field | Value |
| --- | --- |
| Memory | **4096** MiB (official minimum is 2048) |

![Memory tab: 4096 MiB](assets/create-vm/06-memory.jpg)

## Network

| Field | Value |
| --- | --- |
| Bridge | `vmbr0` |
| Model | VirtIO (`virtio`) |
| Firewall | off (lab default) |

![Network tab: virtio on vmbr0](assets/create-vm/07-network.jpg)

## Confirm

Review the summary. Keep **Start after created** off, then **Finish**.

![Confirm tab before Finish](assets/create-vm/08-confirm.jpg)

## Next

[Import disk](import-disk.md){ .md-button }
