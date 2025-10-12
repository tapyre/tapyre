{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
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
          buildInputs = with pkgs; [
            uv
            python3
            ollama
            pkg-config
            cmake
            cairo
            gtk3
            gobject-introspection
            wrapGAppsHook
            gtk-layer-shell
          ];

          NIX_LD_LIBRARY_PATH = with pkgs;
            lib.makeLibraryPath [
            ];

          shellHook = ''
            export LD_LIBRARY_PATH="$NIX_LD_LIBRARY_PATH"
          '';
        };
      }
    );
  };
}
