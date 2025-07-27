{
  pkgs,
  astal,
  ags,
  self,
}: {
  tapyre-cli = pkgs.callPackage ./cli.nix {
    inherit pkgs;
  };
  tapyre-astal = pkgs.callPackage ./astal.nix {
    inherit pkgs astal ags self;
  };
}
