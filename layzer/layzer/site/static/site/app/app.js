;(function (ng) {
    ng.module('layzer', ['ngResource', 'effects', 'input', 'modal']).config(
        ['$routeProvider',
         function ($routeProvider) {
            $routeProvider.when('/feed/:feed', {
                templateUrl: 'feeditems.html',
                controller: 'FeedItemsCtrl',
                resolve: {
                    feedItems: ['feeditemsservice', '$route', function (items, $route) {
                        return items.getForFeed($route.current.params.feed);
                    }]
                }
            });
        }]
    );
}(angular))
