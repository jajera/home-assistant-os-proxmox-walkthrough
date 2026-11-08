# Download image

On the **Proxmox host** shell (**Node → Shell**, or SSH as `root`), not the
workstation. This guide pins **Home Assistant OS 18.5**. A newer release works
if you change the version and checksum.

Source:
[HAOS releases](https://github.com/home-assistant/operating-system/releases) —
asset `haos_ova-<version>.qcow2.xz` (KVM / Proxmox).

## 1. Fetch

<div class="run" markdown>

```bash
cd /var/lib/vz/template
HAOS=18.5
FILE=haos_ova-${HAOS}.qcow2.xz
curl -fL --continue-at - --progress-bar -o "$FILE" \
  "https://github.com/home-assistant/operating-system/releases/download/${HAOS}/$FILE"
ls -lh "$FILE"
```

```text {.no-copy}
-rw-r--r-- 1 root root 509M … haos_ova-18.5.qcow2.xz
```

</div>

## 2. Verify SHA256

GitHub publishes the asset digest on the release page. For 18.5:

<div class="run" markdown>

```bash
echo "9c6f53627c5db04d07b0dcd4221f05768158e84b2d39ed21bf3a287ef864c15e  $FILE" \
  | sha256sum -c
```

```text {.no-copy}
haos_ova-18.5.qcow2.xz: OK
```

</div>

!!! danger "FAILED means stop"
    Delete the file and download again. Never import a bad image.

## 3. Extract

Keep the `.xz` until import succeeds (`unxz -k`).

<div class="run" markdown>

```bash
command -v unxz >/dev/null || apt-get install -y xz-utils
unxz -k "$FILE"
ls -lh haos_ova-${HAOS}.qcow2*
```

```text {.no-copy}
-rw-r--r-- 1 root root 959M … haos_ova-18.5.qcow2
-rw-r--r-- 1 root root 509M … haos_ova-18.5.qcow2.xz
```

</div>

## Next

[Create VM](create-vm.md){ .md-button }
