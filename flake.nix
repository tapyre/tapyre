{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    nixpkgs-stable.url = "github:nixos/nixpkgs/nixos-25.05";

    tapyre-cli = {
      url = "github:tapyre/tapyre?dir=tapyre-cli";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    tapyre-astal = {
      url = "github:tapyre/tapyre?dir=tapyre/astal";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    tapyre-cli,
    tapyre-astal,
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

    packages = forAllSystems (pkgs: {
      tapyre-astal = tapyre-astal.packages.${pkgs.system}.default;
      tapyre-cli = tapyre-cli.packages.${pkgs.system}.default;
    });
  };
}
