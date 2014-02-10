/**
 * Created by barbossa on 2/10/14.
 */

var phonecatControllers = angular.module('phonecatControllers', []);


phonecatControllers.controller('ProjectCtrl', ['$scope', 'Project',
  function($scope, Project) {
    $scope.projects = Project.query();
    $scope.displayOrder = 'created';
  }
]);
