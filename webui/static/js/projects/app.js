/**
 * Created by barbossa on 2/10/14.
 */

var projectApp = angular.module('projectApp',
    [ 'ngRoute', 'projectServices', 'projectControllers']
);

projectApp.config(['$routeProvider', '$locationProvider',
    function ($routeProvider, $locationProvider) {
        $routeProvider.
            when('/', {
                templateUrl: '/static/partials/project/project-list.html',
                controller: 'ProjectCtrl'
            }).
            when('/new_project', {
                templateUrl: '/static/partials/project/project-new.html',
                controller: 'ProjectNewCtrl'
            }).
            when('/project_detail/:proj_id', {
                templateUrl: '/static/partials/project/project-detail.html',
                controller: 'ProjectDetailCtrl'
            }).
            when('/project_detail/:proj_id/add', {
                templateUrl: '/static/partials/project/project-domain-new.html',
                controller: 'ProjectDomainNewCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
        $locationProvider.html5Mode(false).hashPrefix('!')
    }]);
