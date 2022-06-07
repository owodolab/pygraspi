{ lib
, buildPythonPackage
, pytestCheckHook
, pytest
, numpy
, networkx
, scikitimage
, sknw
, nbval
, pymks
}:

buildPythonPackage rec {
  pname = "pygraspi";
  version = "0.1";

  src = lib.cleanSource ./.;

  propagatedBuildInputs = [
    numpy
    networkx
    scikitimage
    sknw
    nbval
    pymks
  ];

  checkInputs = [ pytest ];

  checkPhase = ''
    pytest pygraspi
  '';
  # checkInputs = [ pytestCheckHook ];

  pythonImportsCheck = ["pygraspi"];


}
