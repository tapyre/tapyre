{pkgs}:
pkgs.rustPlatform.buildRustPackage {
  name = "tapyre-cli";

  src = ../../tapyre-cli;

  cargoLock = {
    lockFile = ../../tapyre-cli/Cargo.lock;
  };
}
