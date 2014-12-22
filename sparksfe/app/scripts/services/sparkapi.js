'use strict';

/**
 * @ngdoc service
 * @name sparksfeApp.sparkApi
 * @description
 * # sparkApi
 * Provider in the sparksfeApp.
 */
angular.module('sparksfeApp')
  .provider('sparkApi', function ($http, $q) {

    // Private variables
    var apiBase = 'Hello';
    // Private constructor
    function SparkApi (apiBase) {
      this.apiBase = apiBase;
    }


    var config = function (configObj) {
      configObj.url = apiBase + configObj.url;
      return configObj;
    };

    var createResponse = function (data, meta, ) {

    }

    var handle = function (configObj) {
      var deferred = $q.defer();
      configObj = config(configObj);
      $http(configObj).success(function (data) {

      }).failure(function () {

      });

      return deferred.promise;
    };

    SparkApi.prototype.articles = function (params) {
      handle({
        url: ''
      })
    };

    // Public API for configuration
    this.setApiBase = function (s) {
      apiBase = s;
    };

    // Method for instantiating
    this.$get = function () {
      return new SparkApi(apiBase);
    };
  });
