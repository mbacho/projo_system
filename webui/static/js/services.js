/**
 * Created by barbossa on 2/10/14.
 */

var webometricsServices = angular.module('webometricsServices', ['ngResource']);

webometricsServices.factory('Project', ['$resource',
    function ($resource) {
        return $resource('projects/:id', {}, {
            query: {method: 'GET', params: {id: 'projects'}, isArray: false}
        });
    }
]);
