{pkgs}:
pkgs.rustPlatform.buildRustPackage {
  name = "tapyre-cli";

  src = ../../cli;

  cargoLock = {
    lockFile = ../../cli/Cargo.lock;
  };
}
