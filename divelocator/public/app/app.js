angular.module('app', ['ngResource', 'ngRoute', 'ngMap']);

angular.module('app').config(function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode({
        enabled: true,
        requireBase: false
    });
    $routeProvider
        .when('/', { templateUrl: '/partials/main', controller: 'mainCtrl'});
});

angular.module('app').controller('mainCtrl', function($scope, $http) {
   $http.get("http://127.0.0.1:3000/wrecks/locs").success(function($res) {
	   $scope.positions = $res.rows;
   });
   $scope.$on('mapInitialized', function(event, map) {
      $scope.map = map;
   });
   
   $scope.centerOnMe= function(){
       navigator.geolocation.getCurrentPosition(function(position) {
          var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
          $scope.map.setCenter(pos);
          $scope.map.setZoom(8);
        });
   };
   $scope.centerOnMe()
   //$scope.googleMapsUrl="http://maps.google.com/maps/api/js?v=3.20&client=AIzaSyDqAj26i0rtDYx7LjYJE-lJeBLtOWRvahs"; // Browser Key
   //$scope.googleMapsUrl="http://maps.google.com/maps/api/js?v=3.20&client=AIzaSyDXtUPfbHiQFVwOU-lKYqth6yCEMqNuGrg"; // Server Key
});