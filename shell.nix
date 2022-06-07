# Usage:
#
#     $ nix-shell --pure --argstr graspiVersion "???" --argstr tag 20.09
#

{
  tag ? "22.05",
  graspiVersion ? "59f6a8a2e1ca7c8744a4e37701b919131efb2f45",
  pymksVersion ? "5aeb56c9faff8a655136747faa744b81d9549e3d"
}:
let
  pkgs = import (builtins.fetchTarball "https://github.com/NixOS/nixpkgs/archive/${tag}.tar.gz") {};
  pypkgs = pkgs.python3Packages;
  pymkssrc = builtins.fetchTarball "https://github.com/materialsinnovation/pymks/archive/${pymksVersion}.tar.gz";
  pymks = pypkgs.callPackage "${pymkssrc}/default.nix" {
    graspi=graspi;
    sfepy=null;
  };
  extra = with pypkgs; [ black pylint flake8 ];
  graspisrc = builtins.fetchTarball "https://github.com/owodolab/graspi/archive/${graspiVersion}.tar.gz";
  graspi = pypkgs.callPackage "${graspisrc}/default.nix" {};
  pygraspi = pypkgs.callPackage ./default.nix { sknw=sknw; pymks=pymks; };
  sknw = pypkgs.buildPythonPackage rec {
    pname = "sknw";
    version = "0.14";

    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "sha256-kFwOVaRdlruSL+Eg2sxRbyljL12UyYJzUZq5CC/Cw9k=";
    };

    propagatedBuildInputs = with pypkgs; [ numba networkx ];

  };
  nixes_src = builtins.fetchTarball "https://github.com/wd15/nixes/archive/9a757526887dfd56c6665290b902f93c422fd6b1.zip";
  jupyter_extra = pypkgs.callPackage "${nixes_src}/jupyter/default.nix" {
    jupyterlab=(if pkgs.stdenv.isDarwin then pypkgs.jupyter else pypkgs.jupyterlab);
  };
in
 (pygraspi.overridePythonAttrs (old: rec {

    propagatedBuildInputs = old.propagatedBuildInputs;

    nativeBuildInputs = propagatedBuildInputs ++ [
      pygraspi
    ] ++ extra ++ [ jupyter_extra ];

    shellHook = ''
      export OMPI_MCA_plm_rsh_agent=${pkgs.openssh}/bin/ssh

      SOURCE_DATE_EPOCH=$(date +%s)
      export PYTHONUSERBASE=$PWD/.local
      export USER_SITE=`python -c "import site; print(site.USER_SITE)"`
      export PYTHONPATH=$PYTHONPATH:$USER_SITE:$(pwd)
      export PATH=$PATH:$PYTHONUSERBASE/bin
      export NIX_SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

  '';
  }))
