;(function (ng) {
    "use strict";
    ng.module('layzer').factory('feeditemsservice', ['$http', '$q', function ($http, $q) {

        return {
            getForFeed: function getForFeed(feedUrl) {
                return $http.get('/api/v1/feeditem?feed=' + (feedUrl)).then(
                    function (result) {
                        return result.data.objects;
                    }
                );
            }
        }

    }]);
}(angular));
