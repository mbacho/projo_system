/**
 * Created by barbossa on 2/10/14.
 */

var projectControllers = angular.module('projectControllers', []);

projectControllers.controller('ProjectCtrl',
    ['$scope', 'Project',
        function ($scope, Project) {
            $scope.projects = Project.all();
            $scope.displayOrder = 'created';
            $scope.project_name = '';
            $scope.delProject = function (proj) {
                Project.delete({id: proj.id}, function (data) {
                    var al = new Alert();
                    al.showAlert(proj.name + ' deleted', '', 'success');
                    $scope.projects = _.without($scope.projects, proj);
                }, function (data) {
                    var al = new Alert();
                    al.showAlert(data, 'deletion failed', 'warning');
                });
            };
        }
    ]
);

projectControllers.controller('ProjectNewCtrl',
    ['$scope', 'Project',
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
    ]
);

projectControllers.controller('ProjectDetailCtrl',
    ['$scope', 'Project', 'ProjectDomain', '$http',
        function ($scope, Project, ProjectDomain, $http) {
            $scope.project = Project.get(
                {id: $routeParams.proj_id},
                function (data) {
                    var pd = data.projectdomain_project;
                    for (var i = 0; i < pd.length; i++) {
                        pd[i] = ProjectDomain.get({id: pd[i]});
                    }
                }
            );
            $scope.delPD = function (pd) {
                ProjectDomain.delete(
                    {id: pd.id},
                    function () {
                        $scope.project.projectdomain_project = _.without($scope.project.projectdomain_project, pd);
                        var al = new Alert();
                        al.showAlert('deleted', '', 'success');
                    },
                    function () {
                        var al = new Alert();
                        al.showAlert('delete failed', '', 'warning');
                    }
                );
            };
            $scope.cancelPD = function (pd) {
                var al = new Alert();
                al.showAlert('cancelling job', '', 'info');
                $http(
                    {method: 'POST', data: {jobid: pd.jobid}, url: '/api/projectdomains/' + pd.id + '/canceljob/'})
                    .success(function () {
                        al.showAlert('job cancelled', '', 'success');
                    })
                    .error(function () {
                        al.showAlert('job cancel failed', '', 'warning');
                    });
            };
        }
    ]
);

projectControllers.controller('ProjectDomainNewCtrl',
    ['$scope', 'ProjectDomain', 'AcademicDomain',
        function ($scope, ProjectDomain) {
            $scope.form = {
                pd_starturl: '',
                pd_domain: '',
                pd_subdomain: ''
            };
            $scope.creating = false;
            $scope.addPD = function (project_id) {
                $scope.creating = true;
                ProjectDomain.save(
                    {
                        project: project_id,
                        starturl: $scope.form.pd_starturl,
                        domain: parseInt($scope.form.pd_domain),
                        subdomain: $scope.form.pd_subdomain
                    },
                    function (data) {
                        alert('pd created');
                        //window.location.reload();
                        $scope.creating = false;
                    },
                    function (data) {
                        alert('pd creation failed');
                        $scope.creating = false;
                    }
                );
            };
        }
    ]
);
