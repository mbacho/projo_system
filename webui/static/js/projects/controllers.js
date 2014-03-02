/**
 * Created by barbossa on 2/10/14.
 */

var projectControllers = angular.module('projectControllers', []);


projectControllers.controller('ProjectCtrl', ['$scope', 'Project',
    function ($scope, Project) {
        $scope.projects = Project.query();
        $scope.displayOrder = 'created';
    }
]);


projectControllers.controller('ProjectNewCtrl', ['$scope',
    function ($scope) {
        $scope.project_name = '';
        $scope.createProject = function(){

        };
    }
]);

function UserForm($scope) {
    var master = {
        name: '',
        domains: [
            {domain: '', subdomain: '', starturl: ''}
        ]
    };

    $scope.cancel = function () {
        $scope.form = angular.copy(master);
    };

    $scope.save = function () {
        master = $scope.form;
        $scope.cancel();
    };

    $scope.addDomain = function () {
        $scope.form.domains.push({domain: '', subdomain: '', starturl: ''});
    };

    $scope.removeDomain = function (domain) {
        $scope.form.domains = _.without($scope.form.domains, domain);
    };

    $scope.isCancelDisabled = function () {
        return angular.equals(master, $scope.form);
    };

    $scope.isSaveDisabled = function () {
        return $scope.myForm.$invalid || angular.equals(master, $scope.form);
    };

    $scope.cancel();
}

