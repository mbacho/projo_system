var commonControllers = angular.module('commonControllers', []);

commonControllers.controller('LeftNavCtrl', ['$scope', '$location','Project',
    function ($scope, $location, Project) {
        $scope.projects = Project.all();
        $scope.newproject = '';
        $scope.createProject = function () {
            Project.save(
                {name: $scope.newproject, owner: 1},
                function (data) {
                    var al = new Alert();
                    al.showAlert("project created successfully", "", "success");
                    $scope.projects.push(data);
                    $scope.newproject = '';
                },
                function (data) {
                    var msg = '';
                    var keys = _.keys(data.data);
                    for (var i = 0; i < keys.length; i++)
                        msg += (keys[i] + " : " + data.data[keys[i]].join(', ') + '\n');
                    var al = new Alert();
                    al.showAlert(msg, '', 'warning');
                });
        };
        $scope.openProject = function (proj) {
            $location.path('/project_detail/' + proj.id).replace();
        };
    }
]);
