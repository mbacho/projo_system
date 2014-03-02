/**
 * Created by barbossa on 2/10/14.
 */

var projectApp = angular.module('projectApp',
    [ 'ngRoute', 'projectServices', 'projectControllers']
);

projectApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/partials/project/project-list.html',
                controller: 'ProjectCtrl'
            }).
            when('/new', {
                templateUrl: '/static/partials/project/project-new.html',
                controller: 'ProjectNewCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
    }]);
