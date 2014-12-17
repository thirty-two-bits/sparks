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
    var Api = $resource('https://mysterious-springs-6760.herokuapp.com/api/articles/');


    var getParams = function (asString) {
        asString = asString || false;
        var pairs = (asString ? [] : {});
        for (var key in this.$params) {
            if (this.$params.hasOwnProperty(key)) {
                var item = this.$params[key],
                    name = encodeURIComponent(key);
                if (typeof item === "object") {
                    for (var subkey in item) {
                        if (!angular.isUndefined(item[subkey]) && item[subkey] !== "") {
                            var pname = name + "_" + encodeURIComponent(subkey);
                            if (asString) {
                                pairs.push(pname + "=" + item[subkey]);
                            } else {
                                pairs[pname] = item[subkey];
                            }
                        }
                    }
                } else if (!angular.isFunction(item) && !angular.isUndefined(item) && item !== "") {
                    if (asString) {
                        pairs.push(name + "=" + encodeURIComponent(item));
                    } else {
                        pairs[name] = encodeURIComponent(item);
                    }
                }
            }
        }
        return pairs;
    };


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
            Api.query(getParams.call(params), function(data) {
                console.log(data);
                $timeout(function() {
                    // update table params
                    // set new data
                    $defer.resolve(data);
                }, 500);
            });
        }
    });
  });
