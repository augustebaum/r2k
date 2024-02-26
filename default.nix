{
  lib,
  python,
  buildPythonApplication,
  poetry-core,
  pythonRelaxDepsHook,
  arrow,
  beautifulsoup4,
  click,
  feedparser,
  orjson,
  pick,
  pydantic,
  python-dateutil,
  pyyaml,
  readability-lxml,
  requests,
  pytestCheckHook,
  ...
}: let
  version = "0.7.4";
in
  buildPythonApplication rec {
    pname = "r2k";
    inherit version;
    format = "pyproject";

    src = ./.;

    nativeBuildInputs = [
      poetry-core
      pythonRelaxDepsHook
    ];

    pythonRelaxDeps = [
      "arrow"
      "beautifulsoup4"
      "click"
      "click"
      "orjson"
      "pydantic"
      "pyyaml"
      "requests"
    ];

    propagatedBuildInputs = [
      arrow
      beautifulsoup4
      click
      feedparser
      orjson
      pick
      pydantic
      python-dateutil
      pyyaml
      requests
    ];

    passthru = {
      inherit python;
      optional-dependencies = {
        readability = [readability-lxml];
      };
    };

    nativeCheckInputs =
      [pytestCheckHook]
      ++ lib.flatten (builtins.attrValues passthru.optional-dependencies);

    meta = {
      mainProgram = "r2k";
    };
  }
