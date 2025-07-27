{
  pkgs,
  ags,
  astal,
  self,
}:
pkgs.stdenv.mkDerivation {
  name = "tapyre";

  src = ../../astal;

  nativeBuildInputs = with pkgs; [
    wrapGAppsHook
    gobject-introspection
    glib
    gjs
    ags.packages.${system}.default
  ];

  buildInputs = [
    astal.packages.${pkgs.system}.astal4
  ];

  installPhase = ''
    mkdir -p $out/bin
    ags bundle ./src/app.ts $out/bin/tapyre
  '';

  preFixup = ''
    gappsWrapperArgs+=(
      --prefix PATH : ${pkgs.lib.makeBinPath [
      self.packages.${pkgs.system}.tapyre-cli
    ]}
    )
  '';
}
