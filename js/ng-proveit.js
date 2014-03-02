function Node(value, hashdigest) {
	this.value = Decimal(value);
	this.hashdigest = hashdigest;
}

var NodeCombiner = function(left, right) {
	value = left.value.add(right.value);
	hashdigest = CryptoJS.SHA256(value.toString() + left.hashdigest + right.hashdigest).toString();
	return new Node(value, hashdigest);
}

var ValidateNode = function(node, roothash, pairlist) {
	for (x in pairlist) {
		if (pairlist[x][2]) {
			node = NodeCombiner(node, Node(pairlist[x][0], pairlist[x][1]));
		} else {
			node = NodeCombiner(Node(pairlist[x][0], pairlist[x][1]), node);
		}
	}
	return roothash == node.hashdigest;
}

var app = angular.module('proveit', []);

app.controller("proveitCtrl", function($scope, $http) {
	$scope.roothash = '';
	$scope.totalbalance = 0;
	$scope.rawholdings = '';
	$scope.hashtreedump = '';
});
