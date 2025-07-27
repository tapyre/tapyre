{pkgs}:
pkgs.rustPlatform.buildRustPackage {
  name = "tapyre-cli";

  src = ../..;

  cargoLock = {
    lockFile = ../../Cargo.lock;
  };
}
