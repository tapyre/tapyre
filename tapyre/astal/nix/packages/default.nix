{
  pkgs,
  astal,
  ags,
  tapyre-cli,
}: let
  tapyre = pkgs.callPackage ./tapyre.nix {
    inherit pkgs astal ags tapyre-cli;
  };
in {
  default = tapyre;
  inherit tapyre;
}
