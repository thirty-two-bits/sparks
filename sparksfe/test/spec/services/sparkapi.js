'use strict';

describe('Service: sparkApi', function () {

  // load the service's module
  beforeEach(module('sparksfeApp'));

  // instantiate service
  var sparkApi;
  beforeEach(inject(function (_sparkApi_) {
    sparkApi = _sparkApi_;
  }));

  it('should do something', function () {
    expect(!!sparkApi).toBe(true);
  });

});
