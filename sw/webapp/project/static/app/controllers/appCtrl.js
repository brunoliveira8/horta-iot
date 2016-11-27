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

            $http.get("/status_atuador/")
            .then(function(response) {
                $scope.atuador = response.data;
                if ($scope.atuador.status == true){
                    angular.element('#atuador').removeClass('label-danger');
                    angular.element('#atuador').addClass('label-success');
                    angular.element('#atuador').text('Ligada');
                }
                else {
                    angular.element('#atuador').removeClass('label-success');
                    angular.element('#atuador').addClass('label-danger');
                    angular.element('#atuador').text('Desligada');

                }
            });

          }, 1000);

});