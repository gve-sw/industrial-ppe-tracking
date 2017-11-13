/* Global variables */

var appModule = angular.module('appModule',['ngRoute','ngAnimate'])

/*  Configuration    */

// To avoid conflicts with other template tools such as Jinja2, all between {a a} will be managed by ansible instead of {{ }}
appModule.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);


// Application routing
appModule.config(function($routeProvider, $locationProvider){
    // Maps the URLs to the templates located in the server
    $routeProvider
        .when('/', {templateUrl: 'ng/security_policies'})
        .when('/security_policies', {templateUrl: 'ng/security_policies'})
    $locationProvider.html5Mode(true);
});


/*  Controllers    */



// App controller is in charge of managing all services for the application
appModule.controller('AppController', function($scope, $location, $http, $window, $rootScope){

    $scope.policy = {};
    $scope.policies = []
    $scope.areas = []
    $scope.equipment = []
    $scope.error = ""
    $scope.loading = false;

    $scope.go = function ( path ) {
        $location.path( path );
    };

    $scope.clearError = function(){
        $scope.error = "";
    };

    // Retrieves security policies from the server
    $scope.getPolicies = function(){
        $scope.loading = true;
        $http
            .get('api/security_policy')
            .then(function (response, status, headers, config){
               $scope.policies = response.data
            })
            .catch(function(response, status, headers, config){
                $scope.error = response.data.message
            })
            .finally(function(){
                $scope.loading = false;
            })
    };

    // Creates or update a policy
    $scope.sendPolicy = function(){
        $scope.loading = true;
        $http
            .post('api/security_policy', $scope.policy)
            .then(function (response, status, headers, config){
               $scope.getPolicies();
               $scope.clearPolicy();
            })
            .catch(function(response, status, headers, config){
                $scope.error = response.data.message
            })
            .finally(function(){
                $scope.loading = false;
            })
    };

    // Delete a policy
    $scope.deletePolicy = function(){
        $scope.loading = true;
        $http
            .delete('api/security_policy/' + $scope.policy.id)
            .then(function (response, status, headers, config){
               $scope.getPolicies();
               $scope.clearPolicy();
            })
            .catch(function(response, status, headers, config){
                $scope.error = response.data.message
            })
            .finally(function(){
                $scope.loading = false;
            })
    };

    $scope.editPolicy = function(policy){
        angular.copy(policy, $scope.policy)
    }

    $scope.clearPolicy = function(policy){
       $scope.policy = {}
    }

    // Init methods
    $scope.getPolicies();
});
