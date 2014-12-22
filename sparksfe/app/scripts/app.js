'use strict';

/**
 * @ngdoc overview
 * @name sparksfeApp
 * @description
 * # sparksfeApp
 *
 * Main module of the application.
 */
angular.module('sparksfeApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ui.router',
]).config(function ($stateProvider, $urlRouterProvider, sparkApiProvider) {

  sparkApiProvider.setApiBase('http://localhost:9000');
  $urlRouterProvider.otherwise("/");

  $stateProvider.state('main', {
      url: "/",
      templateUrl: 'views/main.html',
      controller: 'MainCtrl'
  });
});
