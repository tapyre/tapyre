{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    nixpkgs-stable.url = "github:nixos/nixpkgs/nixos-25.05";

    astal = {
      url = "github:aylur/astal";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    ags = {
      url = "github:aylur/ags";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.astal.follows = "astal";
    };

    tapyre-cli = {
      url = "github:tapyre/tapyre?dir=tapyre-cli";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    ags,
    astal,
    tapyre-cli,
    ...
  } @ inputs: let
    systems = [
      "x86_64-linux"
    ];

    forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f pkgsFor.${system});

    pkgsFor = nixpkgs.lib.genAttrs systems (
      system:
        import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        }
    );
  in {
    formatter = forAllSystems (pkgs: pkgs.alejandra);

    devShells = forAllSystems (
      pkgs: {
        default = pkgs.mkShell {
          buildInputs = [
            ags.packages.${pkgs.system}.default
            pkgs.sass
          ];
        };
      }
    );

    packages = forAllSystems (
      pkgs: {
        default = pkgs.stdenv.mkDerivation {
          name = "tapyre";

          src = ./.;

          nativeBuildInputs = with pkgs; [
            wrapGAppsHook
            gobject-introspection
            glib
            gjs
            ags.packages.${system}.default
          ];

          buildInputs = with pkgs; [
            astal.packages.${system}.astal4
          ];

          installPhase = ''
            mkdir -p $out/bin
            ags bundle ./src/app.ts $out/bin/tapyre
          '';

          preFixup = ''
            gappsWrapperArgs+=(
              --prefix PATH : ${pkgs.lib.makeBinPath [
              tapyre-cli.packages.${pkgs.system}.default
            ]}
            )
          '';
        };
      }
    );
  };
}
