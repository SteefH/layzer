;(function (ng) {
    "use strict";
    ng.module('layzer').factory('subscriptionsservice', ['$resource', function ($resource) {
        var resource = $resource('/api/v1/subscription/:id', {
            id: '@id'
        }, {
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function (data) {
                    data = ng.fromJson(data);
                    return data.objects;
                }
            }
        });
        return {
            getAll: ng.bind(resource, resource.query)
        };
    }]);
}(angular));
