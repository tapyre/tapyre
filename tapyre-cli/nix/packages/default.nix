{pkgs}: let
  tapyre-cli = pkgs.callPackage ./tapyre-cli.nix {
    inherit pkgs;
  };
in {
  default = tapyre-cli;
  inherit tapyre-cli;
}
