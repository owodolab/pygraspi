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
, graph-tool
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
    graph-tool
  ];

  checkInputs = [ pytest ];

  checkPhase = ''
    pytest pygraspi
  '';
  # checkInputs = [ pytestCheckHook ];

  pythonImportsCheck = ["pygraspi"];


}
