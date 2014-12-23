'use strict';

/**
 * @ngdoc service
 * @name sparksfeApp.sparkApi
 * @description
 * # sparkApi
 * Provider in the sparksfeApp.
 */
angular.module('sparksfeApp')
  .provider('SparkApi', function () {
    var apiBase, $_http, $_q;

    // Private constructor
    var SparkApi = function () {};


    var config = function (configObj) {
      configObj.url = apiBase + configObj.url;
      return configObj;
    };

    var Response = function (data, meta) {
      this.data = data;
      this.meta = meta;
    };

    var createResponse = function (resp) {
      return new Response(resp.data, resp.meta);
    };

    var handle = function (configObj) {
      var deferred = $_q.defer();
      configObj = config(configObj);

      $_http(configObj).success(function (resp) {
        deferred.resolve(createResponse(resp));
      }).error(function (resp) {
        deferred.reject(createResponse(resp));
      });

      return deferred.promise;
    };

    SparkApi.prototype.articles = function () {
      return handle({
        method: 'GET',
        url: '/articles'
      });
    };

    // Public API for configuration
    this.setApiBase = function (s) {
      apiBase = s;
    };

    // Method for instantiating
    this.$get = function ($http, $q) {
      $_http = $http;
      $_q = $q;
      return new SparkApi(apiBase);
    };
  });
