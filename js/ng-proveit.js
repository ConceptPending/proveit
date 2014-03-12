var app = angular.module('proveit', []);

app.controller("proveitCtrl", function($scope, $http) {
	$scope.roothash = '';
	$scope.totalbalance = 0;
	$scope.rawholdings = '';
	$scope.hashtreedump = '';
	$scope.hashVerified = '';
	$scope.UpdateHashVerifier = function() {
		try {
			jsondump = $.parseJSON($scope.hashtreedump);
			$scope.nodeinfo = jsondump[0];
			$scope.roothash = jsondump[1];
			hashtree = jsondump[2];
			node = new Node($scope.nodeinfo[0], $scope.nodeinfo[1])
			$scope.hashVerified = ValidateNode(node, jsondump[1], hashtree);
		} catch(err) {
			$scope.hashVerified = 'Malformed';
		}
	}
});
