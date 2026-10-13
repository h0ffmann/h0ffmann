{
  description = "h0ffmann profile — builds pdf/cv.pdf from README.md with nix-config's labs/publisher";

  inputs.publisher.url = "github:h0ffmann/nix-config?dir=labs/publisher";
  # The toolchain of site/ (Gleam, Node, esbuild): picasso's gleam-website lab.
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
        # `just site`: the website of site/.
        site = gleam-website.devShells.${system}.default;
        # `just md-quality`, `just reuse`: the analysers of the Markdown files and of the
        # licences, from the same pinned nixpkgs as the site's toolchain.
        md = gleam-website.inputs.nixpkgs.legacyPackages.${system}.mkShell {
          packages = with gleam-website.inputs.nixpkgs.legacyPackages.${system};
            [ markdownlint-cli2 vale lychee reuse git python3 ];
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
