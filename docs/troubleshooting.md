# Troubleshooting

| Symptom | Likely cause | What to try |
| --- | --- | --- |
| UEFI “Access Denied” / boot loop | Secure Boot / Pre-Enroll keys | Shut down; **Hardware → EFI Disk → Edit** and disable Pre-Enroll keys; or recreate the EFI disk with `pre-enrolled-keys=0` |
| Boots into UEFI shell or PXE | Wrong boot order / no disk | Confirm `scsi0` exists and `boot: order=scsi0` in `qm config` |
| `import-from` path error | Wrong path or missing extract | Check `/var/lib/vz/template/haos_ova-*.qcow2` exists; use absolute path |
| Import storage error | Wrong `STORAGE` | Match [What you need](prerequisites.md) tabs (`local-zfs` vs `local-lvm`) |
| Checksum `FAILED` | Truncated download | Delete `.xz`, download again, re-verify |
| `unxz: command not found` | Missing xz tools | `apt-get install -y xz-utils` |
| No IP in console | Bridge / VLAN / cable | Confirm `net0` on `vmbr0`; same LAN as DHCP; check `qm agent … network-get-interfaces` |
| `homeassistant.local` fails | mDNS blocked across VLANs | Use the guest IP from the console or guest agent |
| `:8123` refused / endless preparing | Still first-boot | Wait up to ~20 minutes; watch console; retry `curl` |
| Guest agent “not running” | Agent off or guest not ready | Enable QEMU Guest Agent in Hardware; wait until HAOS finishes boot |
| USB dongle missing in HA | Not passed through | **Hardware → Add → USB Device**; restart VM |
| Disk too small later | 32 GB default | **Hardware → Disk → Resize Disk**; reboot HAOS |
| Prefer the older two-step import | Habit / older docs | `qm importdisk 100 /path/to/haos.qcow2 $STORAGE` then attach the unused disk in Hardware and set boot order |

## Next

[References](references.md)
