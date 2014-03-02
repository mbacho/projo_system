/**
 * Created by barbossa on 2/10/14.
 */

var projectServices = angular.module('projectServices', ['ngResource']);

projectServices.factory('Project', ['$resource',
    function ($resource) {
        return $resource('projects/:id', {}, {
            query: {method: 'GET', params: {id: 'projects'}, isArray: false}
        });
    }
]);

