;(function (ng) {
    "use strict";
    ng.module('layzer').factory('subscriptionsservice', ['$resource', function ($resource) {
        var Subscription = $resource('/api/v1/subscription/:id', {
            id: '@id'
        }, {
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function (data) {
                    data = ng.fromJson(data);
                    return data.objects;
                }
            },
            update: {
                method: 'PUT'
            }
        });
        return {
            getAll: ng.bind(Subscription, Subscription.query),
            add: function (url) {
                var sub = new Subscription({site_url: url});
                sub.$save();
                return sub;
            },
            edit: function (subscription) {
                return subscription.$update();
            }
        };
    }]);
}(angular));
