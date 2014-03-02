/**
 * Created by barbossa on 2/10/14.
 */

var projectServices = angular.module('projectServices', ['ngResource']);

projectServices.factory('Project', ['$resource',
    function ($resource) {
        return $resource('api/projects/:id/', {}, {
            get: {method: 'GET', params: {id: '@id'}, isArray: false},
            all: {method: 'GET', isArray: true}
        });
    }
]);


projectServices.factory('ProjectDomain', ['$resource',
    function ($resource) {
        return $resource('api/projectdomains/:id/', {}, {
            get: {method: 'GET', params: {id: '@id'}, isArray: false},
            all: {method: 'GET', isArray: true}
        });
    }
]);

