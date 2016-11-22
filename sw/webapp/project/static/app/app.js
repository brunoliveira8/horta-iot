'use strict';

angular.module('app', [
  'ngCookies',
  'ngResource',
  'ngSanitize',
  'ngRoute',
]).config(function($httpProvider, $resourceProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    $resourceProvider.defaults.stripTrailingSlashes = false;
});