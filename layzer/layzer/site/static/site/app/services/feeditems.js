;(function (ng) {
    "use strict";
    ng.module('layzer').factory('feeditemsservice', ['$http', '$q', function ($http, $q) {
        var forFeed = {

        };
        return {
            getForFeed: function getForFeed(feedUrl) {
                return $http.get('/api/v1/feeditem?feed=' + (feedUrl)).then(
                    function (result) {
                        forFeed[feedUrl] = {
                            next: result.data.meta.next,
                            objects: result.data.objects
                        };
                        return {
                            items: result.data.objects,
                            hasNext: !!result.data.meta.next
                        };
                    }
                );
            },
            nextForFeed: function nextForFeed(feedUrl) {
                var forThisFeed = forFeed[feedUrl];
                if (!forThisFeed) {
                    return this.getForFeed(feedUrl);
                }
                if (!forThisFeed.promise) {
                    forThisFeed.promise = $q.defer();
                    $http.get(forThisFeed.next).then(function (result) {
                        forThisFeed.next = result.data.meta.next;
                        forThisFeed.objects = forThisFeed.objects.concat(result.data.objects);
                        var promise = forThisFeed.promise;
                        forThisFeed.promise = null;
                        promise.resolve({
                            items: forThisFeed.objects,
                            hasNext: !!result.data.meta.next
                        });
                    });
                }
                return forThisFeed.promise.promise;
            }
        }

    }]);
}(angular));
