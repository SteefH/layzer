;(function (ng) {
    ng.module('layzer').factory('subscriptionsservice', ['$resource', function ($resource) {
        return $resource('/api/v1/subscription/:feed_url', {feed_url: '@feed_url'});
    }]);
}(angular));
