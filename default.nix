{ lib
, buildPythonPackage
, pytestCheckHook
, pytest
, numpy
, networkx
, scikitimage
, skan
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
    skan
    sknw
  ];

  checkInputs = [ pytest ];

  checkPhase = ''
    pytest
  '';
  # checkInputs = [ pytestCheckHook ];


  pythonImportsCheck = ["pygraspi"];


}
