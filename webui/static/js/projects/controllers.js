/**
 * Created by barbossa on 2/10/14.
 */

var projectControllers = angular.module('projectControllers', []);

projectControllers.controller('ProjectDetailCtrl',
    ['$scope', 'Project', 'ProjectDomain', '$routeParams', '$http', '$location',
        function ($scope, Project, ProjectDomain, $routeParams, $http, $location) {
            $scope.project = Project.get(
                {id: $routeParams.proj_id}
            );
            //$scope.project_domains = ProjectDomain.getProject($routeParams.proj_id);
            $scope.delProject = function () {
                $proj = $scope.proj;
                Project.delete({id: proj.id}, function (data) {
                    var al = new Alert();
                    al.showAlert(proj.name + ' deleted', '', 'success');
                    $scope.projects = _.without($scope.projects, proj);
                }, function (data) {
                    var al = new Alert();
                    al.showAlert(data, 'deletion failed', 'warning');
                });
            };
            $scope.addPD = function () {
                $location.path('/project_detail/' + $scope.project.id + '/add').replace();
            };
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
    ['$scope', 'ProjectDomain', 'AcademicDomain', '$routeParams', '$location',
        function ($scope, ProjectDomain, AcademicDomain, $routeParams, $location) {
            $scope.project_id = $routeParams.proj_id;
            $scope.academicdomains = AcademicDomain.all();
            $scope.form = {
                pd_starturl: '',
                pd_domain: '',
                pd_subdomain: ''
            };
            $scope.cancelAdd = function(){
                history.back();
            };
            $scope.addPD = function () {
                ProjectDomain.save(
                    {
                        project: $scope.project_id,
                        starturl: $scope.form.pd_starturl,
                        domain: parseInt($scope.form.pd_domain),
                        subdomain: $scope.form.pd_subdomain
                    },
                    function (data) {
                        $location.path('/project_detail/' + $scope.project_id).replace();
                    },
                    function (data) {
                        var al = new Alert();
                        al.showAlert('pd creation failed', '', 'danger');
                    }
                );
            };
        }
    ]
);
