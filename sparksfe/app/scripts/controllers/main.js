'use strict';

/**
 * @ngdoc function
 * @name sparksfeApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sparksfeApp
 */
angular.module('sparksfeApp')
  .controller('MainCtrl', function ($scope, $timeout, $resource, ngTableParams) {
    var Api = $resource('http://127.0.0.1:5000/api/articles');

    $scope.tableParams = new ngTableParams({
        page: 1,            // show first page
        count: 10,          // count per page
        sorting: {
            current_facebook_shares: 'asc'     // initial sorting
        }
    }, {
        total: 0,           // length of data
        getData: function($defer, params) {
            // ajax request to api
            Api.get(params.url(), function(data) {
                $timeout(function() {
                    // update table params
                    params.total(data.total);
                    // set new data
                    $defer.resolve(data.result);
                }, 500);
            });
        }
    });
  });
