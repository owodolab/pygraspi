# Usage:
#
#     $ nix-shell --pure --argstr graspiVersion "???" --argstr tag 20.09
#

{
  tag ? "22.05-pre",
  graspiVersion ? "59f6a8a2e1ca7c8744a4e37701b919131efb2f45",
  pymksVersion ? "5aeb56c9faff8a655136747faa744b81d9549e3d"
}:
let
  pkgs = import (builtins.fetchTarball "https://github.com/NixOS/nixpkgs/archive/${tag}.tar.gz") {};
  pypkgs = pkgs.python3Packages;
  pymkssrc = builtins.fetchTarball "https://github.com/materialsinnovation/pymks/archive/${pymksVersion}.tar.gz";
  pymks = pypkgs.callPackage "${pymkssrc}/default.nix" {
    graspi=graspi;
  };
  extra = with pypkgs; [ black pylint flake8 ipywidgets ];
  graspisrc = builtins.fetchTarball "https://github.com/owodolab/graspi/archive/${graspiVersion}.tar.gz";
  graspi = pypkgs.callPackage "${graspisrc}/default.nix" {};
in
  pkgs.mkShell rec {
    pname = "pygraspi-env";
    buildInputs = with pypkgs; [
      pymks
      graspi
      jupyter
      scikitimage
      pip
    ];

    shellHook = ''
      export OMPI_MCA_plm_rsh_agent=${pkgs.openssh}/bin/ssh

      SOURCE_DATE_EPOCH=$(date +%s)
      export PYTHONUSERBASE=$PWD/.local
      export USER_SITE=`python -c "import site; print(site.USER_SITE)"`
      export PYTHONPATH=$PYTHONPATH:$USER_SITE:$(pwd)
      export PATH=$PATH:$PYTHONUSERBASE/bin

      jupyter nbextension install --py widgetsnbextension --user > /dev/null 2>&1
      jupyter nbextension enable widgetsnbextension --user --py > /dev/null 2>&1
      pip install jupyter_contrib_nbextensions --user > /dev/null 2>&1
      jupyter contrib nbextension install --user > /dev/null 2>&1
      jupyter nbextension enable spellchecker/main > /dev/null 2>&1


  '';
 }
