# KoboTolinoFindings

# Updates

- Updates have changed quite a bit since 4.x firmware
- ## Structure

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
  ### /usr/local/Kobo only updates
  ```
  Kobo.tgz
  |- libnickel.so
  |- # etc whatever you want unpacked in /usr/local/Kobo
  ```
  - You can use this type of update to enable devmode on the firmware by overriding `/usr/local/Kobo/branch` with a non-release branch eg. devmode (libnickel.so only checks for `release/` in this file to decide if it should run in release mode)
  