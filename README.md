# KoboTolinoFindings

### This is targeted specifically toward the Kobo Libra Colour, Clara BW/Colour and their Tolino counterparts


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

# Upgrading to 5.x

- Before upgrading i recommend making a backup of your recovery partition `/dev/disk/by-partlabel/recovery` as it contains a base kobo fw image and can help you to get back to the stable 4.x branch
- Links to most firmware versions can be found at [mytolino.de/software-updates-tolino-ereader](https://mytolino.de/software-updates-tolino-ereader/) (English site is missing new updates)
- Conversion fw for Libra Colour is at `https://ereaderfiles.kobo.com/firmwares/kobo11/Jul2024/tolino-qt5-qt6-update-5.1.184318/KoboRoot.tgz`
- Conversion fw for Clara BW/Coulour is at `https://ereaderfiles.kobo.com/firmwares/kobo12/May2024/tolino-qt5-qt6-update-5.0.175773/KoboRoot.tgz`
- You will not be able to use the built in update mechanism unless you switch to Tolino inside dev settings, you will instead have to sideload all updates manually by placing them inside `/mnt/onboard/.kobo` folders

# Enabling devmode on 5.x firmware

- Drop the [update.tar](https://github.com/notmarek/KoboTolinoFindings/raw/refs/heads/master/EnableDevmode/update.tar) file into `/mnt/onboard/.kobo`
- After the update fails/applies search `devmodeon` - devmode should be enabled :)

# Downgrading from 5.x back to stock 4.x

- the update.tar in DowngradePackages is universal for the Clara (Shine 5) bw/c and Libra (Vision) Colour

  ### How do i do it?

  0. If you in Kobo mode already skip to step 2
  1. [enable devmode on your tolino](#enabling-devmode-on-5x-firmware) and switch to kobo `(this may not be required but i haven't tried it in tolino mode)`
  2. sideload update.tar into your `.kobo` folder
  3. eject your ereader
  4. profit!

# Updates

- Updates have changed quite a bit since 4.x firmware
- if `/etc/init.d/ota` finds one `update.tar|Kobo.tgz|serial.txt`

  ### Normal update

  ```
  update.tar
  |- driver.sh # main file does most of the work
  |- decompressor # sh file used to decompress other files - this just has exec unzstd inside
  |- rootfs.img # flashed in stage2 - main part of the update a zstd packed ext4 image of the whole rootfs
  |- sha2-256sums # zstd packed list of sha256 hashes of the update files in HASH\tFILE_NAME\n format
  |- bl2.img # flashed in stage1
  |- uboot.img # flashed in stage1
  |- tee.img # flashed in stage1
  |- monza
     |- kernel.img # flashed in stage1
     |- ntxfw.img # flashed in stage1
  |- spa-bw
     |- same as monza
  |- spa-colour
     |- same as monza
  ```

  - Normal update similar to KoboRoot.tgz
  - Can be found at `https://ereaderfiles.kobo.com/firmwares/kobo11/{Month}{Year}/tolino-qt6-update-{version}/update.tar` - kobo11 is vision/libra colour and kobo12 is Clara/Shine bw/c
  - Step 1. ota service extracts and executes the driver.sh while still in rootfs `/tmp/update/driver.sh $update stage1 $PRODUCT`
  - Step 2. if stage1 finishes without an error ota service proceeds to reboot into the recovery partition
  - Step 3. recovery notices an unfinished update and executes stage2 of the driver, it then reboots back to rootfs

  ### Recovery update

  ```
  update.tar
  |- driver.sh # main file does most of the work
  |- decompressor # sh file used to decompress other files - this just has exec unzstd inside
  |- recoveryfs.img # flashed in stage1 - main part of the update a zstd packed ext4 image of the whole recoveryfs
  |- stock-rootfs # an empty file telling driver.sh stage2 to skip looking for a rootfs.img and instead flash the one thats included in the recovery
  |- sha2-256sums # zstd packed list of sha256 hashes of the update files in HASH\tFILE_NAME\n format
  |- bl2.img # flashed in stage1
  |- uboot.img # flashed in stage1
  |- tee.img # flashed in stage1
  |- monza
     |- kernel.img # flashed in stage1
     |- ntxfw.img # flashed in stage1
  |- spa-bw
     |- same as monza
  |- spa-colour
     |- same as monza
  ```

  - This type of update replaces the recoveryfs meaning that you will stay on this update trough force resets using the right button + power combo
  - Can be found at `https://ereaderfiles.kobo.com/firmwares/kobo11/{Month}{Year}/tolino-qt6-recovery-{version}/update.tar` - kobo11 is vision/libra colour and kobo12 is Clara/Shine bw/c
  - This type of update is applied the same as a normal udpate, only difference is inside the driver.

  ### /usr/local/Kobo only updates

  ```
  Kobo.tgz
  |- libnickel.so
  |- # etc whatever you want unpacked in /usr/local/Kobo
  ```

  - You can use this type of update to enable devmode on the firmware by overriding `/usr/local/Kobo/branch` with a non-release branch eg. devmode (libnickel.so only checks for `release/` in this file to decide if it should run in release mode)
  - ota service extracts Kobo.tgz over /usr/local/Kobo

  ### serial.txt

  - Let's you change your serial number, this is the regex it's verified againts, i have no clue what `,[0-9a-f]{32}$` is meant to be
    `^SN-[TN][0-9]{4}[1-9A-C][0-9]{7},[0-9a-f]{32}$`
  - after verifying that the serial number is acceptable its dded into `/dev/disk/by-partlabel/hwcfg`

# Known FW versions

| Name       | Function                                                                                                           |
|------------|--------------------------------------------------------------------------------------------------------------------|
| Conversion | An update allowing conversion from the 4.x to the 5.x branch of the fw, uses old update format (KoboRoot.tgz)      | 
| Recovery   | Replaces the whole recoveryfs, also contains a rootfs image inside /recovery folder that is applied during stage2. |
| Normal     | Replaces the whole rootfs, the most common type.                                                                   |
| Kobo.tgz   | Similar to the old KoboRoot.tgz, applied the same way. Updates /usr/local/Kobo. Never seen in the wild afaik.      |
 
### Shine 5 / Clara BW/Color

| Version    | Release Date   | Type                                                                                                                                                                                                                             | Notes |
|------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|
| 5.0.175773 | May 2024       | [Conversion](https://ereaderfiles.kobo.com/firmwares/kobo12/May2024/tolino-qt5-qt6-update-5.0.175773/KoboRoot.tgz), [Recovery](https://ereaderfiles.kobo.com/firmwares/kobo12/May2024/tolino-qt6-recovery-5.0.175773/update.tar) | |
| 5.0.178115 | May 2024       | [Conversion](https://ereaderfiles.kobo.com/firmwares/kobo/May2024/tolino-qt5-qt6-update-5.0.178115/KoboRoot.tgz), [Normal](https://ereaderfiles.kobo.com/firmwares/kobo/May2024/tolino-qt6-update-5.0.178115/update.tar), [Recovery](https://ereaderfiles.kobo.com/firmwares/kobo/May2024/tolino-qt6-recovery-5.0.178115/update.tar)               | |
| 5.1.184318 | July 2024      | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo12/Jul2024/tolino-qt6-update-5.1.184318/update.tar)                                                                                                                         | |
| 5.2.190625 | August 2024    | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo12/Aug2024/tolino-qt6-update-5.2.190625/update.tar)                                                                                                                         | |
| 5.3.195056 | September 2024 | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo12/Sep2024/tolino-qt6-update-5.3.195056/update.tar)                                                                                                                         | |
| 5.4.197982 | October 2024   | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo12/Oct2024/tolino-qt6-update-5.4.197982/update.tar)                                                                                                                         | |
| 5.6.209315 | February 2025  | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo12/Feb2025/tolino-qt6-update-5.6.209315/update.tar)                                                                                                                         | |
| 5.7.212781 | March 2025  | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo12/Mar2025/tolino-qt6-update-5.7.212781/update.tar)                                                                                                                         | |
| 5.8.216841 | May 2025  | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo12/May2025/tolino-qt6-update-5.8.216841/update.tar)                                                                                                                         | |
| 5.9.220067 | June 2025  | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo12/Jun2025/tolino-qt6-update-5.9.220067/update.tar)                                                                                                                         | |
| 5.10.225420 | July 2025  | [Conversion](https://ereaderfiles.kobo.com/firmwares/kobo12/Jul2025/qt5-qt6-5.10.225420/Koboroot.tgz), [Recovery](https://ereaderfiles.kobo.com/firmwares/kobo12/Jul2025/qt6-recovery-5.10.225420/update.tar)                                                                                                                         | As of this version kobo has started testing the 5.x firmware on EU kobo devices, more info [here](https://www.mobileread.com/forums/showthread.php?t=361035&page=20) and [here](https://help.kobo.com/hc/en-us/articles/32246787707799-Kobo-eReader-Accessibility-Features-Software-Support), this also seems to contain a recovery update, probably to faciliate the downgrade option in accessibility settings. |

### Vision Colour / Libra Colour

| Version    | Release Date   | Type                                                                                                                                                                                                                             | Notes |
|------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| 5.1.184318 | July 2024      | [Conversion](https://ereaderfiles.kobo.com/firmwares/kobo11/Jul2024/tolino-qt5-qt6-update-5.1.184318/KoboRoot.tgz), [Recovery](https://ereaderfiles.kobo.com/firmwares/kobo11/Jul2024/tolino-qt6-recovery-5.1.184318/update.tar) | |
| 5.1.186250 | July 2024      | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo11/Jul2024/tolino-qt6-update-5.1.186250/update.tar)                                                                                                                         | |
| 5.2.190625 | August 2024    | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo11/Aug2024/tolino-qt6-update-5.2.190625/update.tar)                                                                                                                         | |
| 5.3.195056 | September 2024 | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo11/Sep2024/tolino-qt6-update-5.3.195056/update.tar)                                                                                                                         | |
| 5.4.197982 | October 2024   | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo11/Oct2024/tolino-qt6-update-5.4.197982/update.tar)                                                                                                                         | |
| 5.6.209315 | February 2025  | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo11/Feb2025/tolino-qt6-update-5.6.209315/update.tar)                                                                                                                         | |
| 5.7.212781 | March 2025  | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo11/Mar2025/tolino-qt6-update-5.7.212781/update.tar)                                                                                                                         | |
| 5.8.216841 | May 2025  | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo11/May2025/tolino-qt6-update-5.8.216841/update.tar)                                                                                                                         | |
| 5.9.220067 | June 2025  | [Normal](https://ereaderfiles.kobo.com/firmwares/kobo11/Jun2025/tolino-qt6-update-5.9.220067/update.tar)                                                                                                                         | |
| 5.10.225420 | July 2025  | [Conversion](https://ereaderfiles.kobo.com/firmwares/kobo11/Jul2025/qt5-qt6-5.10.225420/KoboRoot.tgz),[Recovery](https://ereaderfiles.kobo.com/firmwares/kobo11/Jul2025/qt6-recovery-5.10.225420/update.tar)                                                                                                                         | As of this version kobo has started testing the 5.x firmware on EU kobo devices, more info [here](https://www.mobileread.com/forums/showthread.php?t=361035&page=20) and [here](https://help.kobo.com/hc/en-us/articles/32246787707799-Kobo-eReader-Accessibility-Features-Software-Support), this also seems to contain a recovery update, probably to faciliate the downgrade option in accessibility settings. |

# Recovery Options

- Fix your fuckups

  ### Recovery Partition

  - Assuming your bootloader and kernel aren't broken you can recover from broken rootfs updates by holding the right button + power until the light shuts off
  - Recovery will flash all the images stored in /recovery rolling you back to your recovery version

  ### Fastboot

  - Can be access by holding power and spamming right button with a cable connected to the computer
  - Very stripped down, not sure how useful, `flash` command ~~might~~ works -- I've managed to flash the serial number and some other things.

# Boot

- Some docs about the boot process

  ### BootRom (BL1)

  - SBC, SLA, DAA are disabled (Secure boot seems to be disabled for the preloader)
  - Can be accessed by shorting the download pads on the board

  ```
  Preloader -     CPU:            MT8512()
  Preloader -     HW version:        0x0
  Preloader -     WDT:            0x10007000
  Preloader -     Uart:            0x11002000
  Preloader -     Brom payload addr:    0x100a00
  Preloader -     DA payload addr:    0x111000
  Preloader -     CQ_DMA addr:        0x10214000
  Preloader -     Var1:            0xa
  Preloader - Disabling Watchdog...
  Preloader - HW code:            0x8512
  Preloader - Target config:        0xe0
  Preloader -     SBC enabled:        False
  Preloader -     SLA enabled:        False
  Preloader -     DAA enabled:        False
  Preloader -     SWJTAG enabled:        False
  Preloader -     EPP_PARAM at 0x600 after EMMC_BOOT/SDMMC_BOOT:    False
  Preloader -     Root cert required:    False
  Preloader -     Mem read auth:        True
  Preloader -     Mem write auth:        True
  Preloader -     Cmd 0xC8 blocked:    True
  Preloader - Get Target info
  Preloader - BROM mode detected.
  Preloader -     HW subcode:        0x8a00
  Preloader -     HW Ver:            0xca02
  Preloader -     SW Ver:            0x100
  Preloader - ME_ID:            FA1F001954B53BEC0EC423FE9D59C26C
  Preloader - SOC_ID:            0000000000000000000000000000000000000000000000000000000000000000
  ```

  - mtkclient has support for the SOC but i haven't been able to use it to extract the preloader
  - preloader can be optained from the update files (bl2.img)
  - you can also dump the preloader on device by using `dd if=/dev/mmcblk0boot0 of=/mnt/onboard/preloader.img`
  - Bootrom is available at `brom_8512.bin`
  - even tho mtkclient and other tools say that SBC is disabled a modified preloader image doesn't boot and device is forced into brom DL mode

  ### Preloader (BL2)

  - Packaged with every update inside the bl2.img
  - Does secure boot checks
  - Includes stripped down fastboot
  - My BinaryNinja db with some names and structs is present in `Preloader.bndb`


# Other links

- [pgaskin kobopatch issue #130](https://github.com/pgaskin/kobopatch-patches/issues/130)
- [NerdyProjects koreader pr #12401](https://github.com/koreader/koreader/pull/12401)
- [beedaddy koreader issue #12047](https://github.com/koreader/koreader/issues/12047)
- [fohvok kfmon issue #9](https://github.com/NiLuJe/kfmon/issues/9)
- [NerdyProjects kfmon pr #11](https://github.com/NiLuJe/kfmon/pull/11)
