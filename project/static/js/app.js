

var hidtv = angular.module('hidtv', ['ngFileUpload'])



hidtv.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{ng');
  $interpolateProvider.endSymbol('ng}');
}]);

angular.module('hidtv').controller('uploadController',
  ['$scope', 'Upload', '$timeout',
  function($scope, Upload, $timeout) {

    $scope.upload = function(file) {

      if(file) {
        $scope.progress = "Compressing..."
        Upload.resize(file, 1920, 1080, 0.7).then(function(resizedFile) {
          Upload.upload({
            url: '/upload',
            data: { file: resizedFile, position: $scope.position }
          }).then(function(response) {
            $timeout(function() {
              $scope.result = response.data
            })
          }, function(response) {
            if(response.status > 0) {
              console.log(response.status)
            }
          }, function(event) {
            console.log(Math.min(100, parseInt(100.0 * event.loaded / event.total)));
            $scope.progress = Math.min(100, parseInt(100.0 * event.loaded / event.total))
            if($scope.progress === 100) {
              Turbolinks.visit(location.toString())
            }
          })
        })
      }
    }

  }
])

angular.module('hidtv').controller('lifelogController' ['$scope', 'LifelogService', 
  function($scope, LifelogService) {
    $scope.getSteps = function() {
      LifelogService.getSteps()
      .then(function(response) {
        $scope.steps = response
      })
      .catch(function(response) {

      })
    }
  }
])


// Services
angular.module('hidtv').factory('LifelogService',
  ['$q', '$timeout', '$http',
    function($q, $timeout, $http) {
      return ({
        getSteps: getSteps
      })

      function getSteps() {
        var deferred = $q.defer()

        $http.get('')
      }
    }
  ])