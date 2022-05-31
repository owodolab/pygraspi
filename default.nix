{ lib
, buildPythonPackage
, pytestCheckHook
, pytest
, numpy
, networkx
, scikitimage
, sknw
, nbval
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
  ];

  checkInputs = [ pytest ];

  checkPhase = ''
    pytest
  '';
  # checkInputs = [ pytestCheckHook ];

  pythonImportsCheck = ["pygraspi"];


}
