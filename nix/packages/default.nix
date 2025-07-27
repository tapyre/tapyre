{
  pkgs,
  astal,
  ags,
  self,
}: {
  tapyre-cli = pkgs.callPackage ./tapyre-cli.nix {
    inherit pkgs;
  };
  tapyre-astal = pkgs.callPackage ./tapyre-astal.nix {
    inherit pkgs astal ags self;
  };
}
