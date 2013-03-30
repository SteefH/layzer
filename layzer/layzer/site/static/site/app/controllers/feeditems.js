;(function (ng) {
    ng.module('layzer').controller(
        'FeedItemsCtrl',
        ['$scope', 'feedItems', '$routeParams',
         function ($scope, feeditems, $routeParams) {
            $scope.items = feeditems;
            if (0 && $routeParams.feed) {
                $scope.items = feeditemsservice.getForFeed($routeParams.feed);
            }
        }]
    );
}(angular));
