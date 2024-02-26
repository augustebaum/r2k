{pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/643acb4173529a2d2e70a196c677a1afd1f2389f") {}}: let
  python = pkgs.python311;
  r2k = python.pkgs.callPackage ./default.nix {};
in
  pkgs.mkShell {
    packages = [
      r2k

      # For testing
      python.pkgs.ipdb

      # Good to have in shell
      python
      pkgs.poetry
      pkgs.ruff
    ];
  }
