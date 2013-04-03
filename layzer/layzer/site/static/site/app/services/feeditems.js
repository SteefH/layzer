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
                    forThisFeed.promise = $http.get(
                        forThisFeed.next
                    ).then(function (result) {
                        ng.extend(forThisFeed, {
                            next: result.data.meta.next,
                            objects: forThisFeed.objects.concat(result.data.objects),
                            promise: null
                        });
                        return {
                            items: forThisFeed.objects,
                            hasNext: !!result.data.meta.next
                        };
                    });
                }
                return forThisFeed.promise;
            }
        }

    }]);
}(angular));
