/**
 * Created by barbossa on 2/10/14.
 */

var projectApp = angular.
    module('projectApp',
        [ 'ngRoute', 'projectServices', 'projectControllers', ]
    ).
    config(['$routeProvider', '$locationProvider',
        function ($routeProvider, $locationProvider) {
            $routeProvider.
                when('/', {
                    templateUrl: '/static/partials/project/project-list.html'
                }).
                when('/project_detail/:proj_id', {
                    template: '/static/partials/project/project-detail.html',
                    controller: 'ProjectDetailCtrl'
                }).
                otherwise({
                    redirectTo: '/'
                });
            $locationProvider.html5Mode(false).hashPrefix('!')
        }
    ]);
