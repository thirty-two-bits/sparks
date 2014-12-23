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
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ui.router',
    'truncate',
]).config(function ($stateProvider, $urlRouterProvider, $locationProvider, SparkApiProvider) {

  SparkApiProvider.setApiBase('http://localhost:5000/api');
  $urlRouterProvider.otherwise("/");
  $locationProvider.html5Mode(true);
  $stateProvider.state('main', {
      url: "/",
      templateUrl: 'views/main.html',
      resolve: {
        articles: function (SparkApi, $stateParams) {
          return SparkApi.articles();
        }
      },
      controller: 'MainCtrl',
  });
});
