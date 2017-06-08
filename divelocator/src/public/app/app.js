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

   $scope.activeWreck = null;

   $scope.Slider1DefValue = "0;20";
   $scope.Slider1Options = {
     from:0,
     to:100,
     step:5,
     dimension: ' m',
     threshold: 5,
     callback: function(value, released) {
       console.log(value + " " + released);
     }

   };

   $scope.getWreck = function(event,wid) {
	   $http.get("http://127.0.0.1:3000/wrecks/"+wid).success(function($res) {
		   $scope.activeWreck = $res;
	   });
   };

   $scope.centerOnUK = function() {
	   var pos = new google.maps.LatLng("54.217623","-4.535172");
       $scope.map.setCenter(pos);
       $scope.map.setZoom(5);
   };
   $scope.centerOnIRE = function() {
	   var pos = new google.maps.LatLng("53.570235","-7.711594");
       $scope.map.setCenter(pos);
       $scope.map.setZoom(6);
   };
   $scope.centerOnSCO = function() {
	   var pos = new google.maps.LatLng("57.193342","-4.459641");
       $scope.map.setCenter(pos);
       $scope.map.setZoom(6);
   };
   $scope.centerOnENG = function() {
	   var pos = new google.maps.LatLng("52.476803","-1.015238");
       $scope.map.setCenter(pos);
       $scope.map.setZoom(5);
   };
   $scope.centerOnIOM = function() {
	   var pos = new google.maps.LatLng("54.218886","-4.529501");
       $scope.map.setCenter(pos);
       $scope.map.setZoom(9);
   };
   $scope.centerOnMe= function(){
       navigator.geolocation.getCurrentPosition(function(position) {
          var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
          $scope.map.setCenter(pos);
          $scope.map.setZoom(8);
        });
   };
   $scope.centerOnMe();
});
