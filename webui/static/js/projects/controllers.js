/**
 * Created by barbossa on 2/10/14.
 */

var projectControllers = angular.module('projectControllers', []);

projectControllers.controller('ProjectCtrl', ['$scope', 'Project',
    function ($scope, Project) {
        $scope.projects = Project.all();
        $scope.displayOrder = 'created';
        $scope.project_name = '';
        $scope.createProject = function () {
            Project.save(
                {name: $scope.project_name, owner: 1},
                function (data) {
                    $scope.projects.push(data);
                },
                function (data) {
                    var msg = '';
                    var keys = _.keys(data.data);
                    for (var i = 0; i < keys.length; i++)
                        msg += (keys[i] + " : " + data.data[keys[i]].join(', ') + '\n')
                    alert(msg);
                });
        };
    }
]);

