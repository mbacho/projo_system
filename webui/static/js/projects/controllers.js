/**
 * Created by barbossa on 2/10/14.
 */

var projectControllers = angular.module('projectControllers', []);

projectControllers.controller('ProjectCtrl', ['$scope', 'Project',
    function ($scope, Project) {
        $scope.projects = Project.all();
        $scope.displayOrder = 'created';
        $scope.project_name = '';
        $scope.delProject = function (proj) {
            Project.delete({id: proj.id}, function (data) {
                var al = new Alert();
                al.showAlert(proj.name+ ' deleted', '', 'success');
                $scope.projects = _.without($scope.projects, proj);
            }, function (data) {
                var al = new Alert();
                al.showAlert(data, 'deletion failed', 'warning');
            });
        };
    }
]);


projectControllers.controller('ProjectNewCtrl', ['$scope', 'Project',
    function ($scope, Project) {
        $scope.project_name = '';
        $scope.current_project = null;
        $scope.createProject = function () {
            Project.save(
                {name: $scope.project_name, owner: 1},
                function (data) {
                    $scope.current_project = data;
                    var al = new Alert();
                    al.showAlert("project created successfully", "", "success");
                },
                function (data) {
                    var msg = '';
                    var keys = _.keys(data.data);
                    for (var i = 0; i < keys.length; i++)
                        msg += (keys[i] + " : " + data.data[keys[i]].join(', ') + '\n')
                    var al = new Alert();
                    al.showAlert(msg, '', 'warning');
                });
        };
    }
]);

projectControllers.controller('ProjectDetailCtrl', ['$scope', 'Project', 'ProjectDomain', '$routeParams',
    function ($scope, Project, ProjectDomain, $routeParams) {
        $scope.projects = Project.get({id: $routeParams.proj_id},
            function (data) {
            },
            function (data) {
                var al = new Alert();
                al.showAlert('project not found', '', 'warning');
            }
        );
    }
]);