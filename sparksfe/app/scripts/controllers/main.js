'use strict';

/**
 * @ngdoc function
 * @name sparksfeApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sparksfeApp
 */
angular.module('sparksfeApp')
  .controller('MainCtrl', function ($scope, articles) {
    $scope.articles = articles;
  });
