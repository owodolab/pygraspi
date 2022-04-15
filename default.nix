{ lib
, buildPythonPackage
, pytestCheckHook
, pytest
, numpy
, networkx
, scikitimage
, sknw
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
  ];

  checkInputs = [ pytest ];

  checkPhase = ''
    pytest
  '';
  # checkInputs = [ pytestCheckHook ];

  pythonImportsCheck = ["pygraspi"];


}
