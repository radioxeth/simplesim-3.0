{
  inputs = { utils.url = "github:numtide/flake-utils"; };
  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs;
            [
              (pkgs.python3.withPackages (python-pkgs: [
                python-pkgs.python-lsp-server
                python-pkgs.black
                python-pkgs.numpy
                python-pkgs.matplotlib
                python-pkgs.pandas
              ]))

            ];
        };
      });
}
