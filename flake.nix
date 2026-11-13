{
  description = "h0ffmann profile — builds pdf/cv.pdf from README.md with nix-config's labs/publisher";

  inputs.publisher.url = "github:h0ffmann/nix-config?dir=labs/publisher";
  # picasso's gleam-website lab: its pinned nixpkgs gives the md, cover and ste shells.
  inputs.gleam-website.url = "github:h0ffmann/picasso?dir=labs/gleam-website";

  outputs = { self, publisher, gleam-website }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" ];
      forAll = f: publisher.inputs.nixpkgs.lib.genAttrs systems (s: f s publisher.inputs.nixpkgs.legacyPackages.${s});
      # What the short CV needs beside the publisher's toolchain: the site's three typefaces
      # (DESIGN.md), and the commit this flake was built from, which the PDF prints. The
      # commit is empty when the tree has changes that are not committed.
      cvEnv = self: pkgs: {
        CV_FONTS = "${pkgs.google-fonts.override { fonts = [ "BricolageGrotesque" "Newsreader" ]; }}/share/fonts/truetype";
        CV_MONO = "${pkgs.jetbrains-mono}/share/fonts";
        CV_COMMIT = self.rev or "";
      };
    in
    {
      packages = forAll (system: pkgs: {
        default = (publisher.lib.${system}.mkPdf {
          name = "cv";
          src = ./.;
          command = "bash cv/build.sh";
        }).overrideAttrs (_: cvEnv self pkgs);
      });

      checks = forAll (system: _: {
        cv = self.packages.${system}.default;
      });

      devShells = forAll (system: pkgs: {
        # `just ste`: Agda and its standard library, for the ASD-STE100 check of www/ste.
        ste = gleam-website.inputs.nixpkgs.legacyPackages.${system}.mkShell {
          packages = [ (gleam-website.inputs.nixpkgs.legacyPackages.${system}.agda.withPackages (p: [ p.standard-library ])) ];
        };
        # `just md-quality`, `just reuse`: the analysers of the Markdown files and of the
        # licences, from the same pinned nixpkgs.
        md = gleam-website.inputs.nixpkgs.legacyPackages.${system}.mkShell {
          packages = with gleam-website.inputs.nixpkgs.legacyPackages.${system};
            [ markdownlint-cli2 vale lychee reuse git python3 ];
        };
        # `just cover <login>`: the Rust of cover/ and the node that runs vendor/archify. Chrome
        # and gh come from the host.
        cover = gleam-website.inputs.nixpkgs.legacyPackages.${system}.mkShell {
          packages = with gleam-website.inputs.nixpkgs.legacyPackages.${system}; [ cargo rustc nodejs ];
        };
        default = pkgs.mkShell {
          name = "cv";
          packages = publisher.lib.${system}.tools;
          shellHook = pkgs.lib.concatStringsSep "\n"
            (pkgs.lib.mapAttrsToList (k: v: "export ${k}=${pkgs.lib.escapeShellArg v}") (publisher.lib.${system}.env // cvEnv self pkgs));
        };
      });
    };
}
