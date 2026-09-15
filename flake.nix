{
  description = "h0ffmann profile — builds pdf/cv.pdf from README.md with nix-config's labs/publisher";

  inputs.publisher.url = "github:h0ffmann/nix-config/labs/publisher-badges?dir=labs/publisher";

  outputs = { self, publisher }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" ];
      forAll = f: publisher.inputs.nixpkgs.lib.genAttrs systems (s: f s publisher.inputs.nixpkgs.legacyPackages.${s});
    in
    {
      packages = forAll (system: _: {
        default = publisher.lib.${system}.mkPdf {
          name = "cv";
          src = ./.;
          command = "bash cv/build.sh";
        };
      });

      checks = forAll (system: _: {
        cv = self.packages.${system}.default;
      });

      devShells = forAll (system: pkgs: {
        default = pkgs.mkShell {
          name = "cv";
          packages = publisher.lib.${system}.tools;
          shellHook = pkgs.lib.concatStringsSep "\n"
            (pkgs.lib.mapAttrsToList (k: v: "export ${k}=${pkgs.lib.escapeShellArg v}") publisher.lib.${system}.env);
        };
      });
    };
}
