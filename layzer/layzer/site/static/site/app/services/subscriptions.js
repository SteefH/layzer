;(function (ng) {
    "use strict";
    ng.module('layzer').factory('subscriptionsservice', ['$resource', '$q', function ($resource, $q) {
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

        var withPromise = function (fn) {
            return function () {
                var args = Array.prototype.slice.call(arguments, 0),
                    deferred = $q.defer();
                args.push(
                    ng.bind(deferred, deferred.resolve),
                    ng.bind(deferred, deferred.reject)
                );
                fn.apply(this, args);
                return deferred.promise;
            }
        };

        var callWithPromise = function (fn) {
            return withPromise(fn).apply(this, Array.prototype.slice.call(arguments, 1));
        }

        return {
            getAll: ng.bind(Subscription, Subscription.query),
            add: function (url) {
                var sub = new Subscription({site_url: url});
                return callWithPromise(ng.bind(sub, sub.$save));
            },
            edit: function (subscription) {
                return callWithPromise(ng.bind(subscription, subscription.$update));
            },
            remove: function (subscription) {
                return callWithPromise(ng.bind(subscription, subscription.$delete));
            }
        };
    }]);
}(angular));
