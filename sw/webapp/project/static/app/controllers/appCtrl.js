'use strict';
angular.module('app')
  .controller('appCtrl', function ($scope, $http, $interval) {

    $http.get("/ultima_medida/")
    .then(function(response) {
        $scope.ultima_medida = response.data;
    });

    $http.get("/media_medidas/")
    .then(function(response) {
        $scope.media_medidas = response.data;
    });

    var interval = $interval(function() {
            $http.get("/ultima_medida/")
                .then(function(response) {
                    $scope.ultima_medida = response.data;
            });

            $http.get("/media_medidas/")
            .then(function(response) {
                $scope.media_medidas = response.data;
            });

          }, 1000);

});