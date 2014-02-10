/**
 * Created by barbossa on 2/10/14.
 */

var webometricsApp = angular.module('webometricsApp',
    [ 'ngRoute', 'webometricsServices', 'webometricsFilters', 'webometricsControllers']
);

webometricsApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/home', {
                templateUrl: '/partials/home.html',
                controller: 'ProjectCtrl'
            }).
            when('/project/new', {
                templateUrl: '/partials/project-new.html',
                controller: 'ProjectNewCtrl'
            }).
            otherwise({
                redirectTo: '/home'
            });
    }]);

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

    $scope.removeDomain = function (contact) {
        var domains = $scope.form.domains;
        for (var i = 0, ii = domains.length; i < ii; i++) {
            if (domain === domains[i]) {
                domains.splice(i, 1);
            }
        }
    };

    $scope.isCancelDisabled = function () {
        return angular.equals(master, $scope.form);
    };

    $scope.isSaveDisabled = function () {
        return $scope.myForm.$invalid || angular.equals(master, $scope.form);
    };

    $scope.cancel();
}

