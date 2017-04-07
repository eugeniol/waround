angular
    .module('wAround', [])
    .controller('mainController', ($scope, $http) => {
        $http({
            method: 'GET',
            url: '/devices',
        })
            .then(({ data }) => {
                $scope.devices = data
            })
    })