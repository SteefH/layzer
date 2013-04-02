;(function (ng) {
    ng.module('layzer').controller(
        'FeedItemsCtrl',
        ['$scope', 'feedItems', '$routeParams', 'feeditemsservice',
         function ($scope, feeditems, $routeParams, feeditemsservice) {
            $scope.items = feeditems.items;
            $scope.hasNext = feeditems.hasNext;
            $scope._shownItem = {};
            $scope.isShown = function (item) {
                return item.id === $scope._shownItem;
            };
            $scope.showItem = function (item) {
                if ($scope.isShown(item)) {
                    $scope._shownItem = null;
                } else {
                    $scope._shownItem = item.id;
                }
            };
            $scope.loadMore = function () {
                feeditemsservice.nextForFeed($routeParams.feed).then(function (items) {
                    $scope.items = items.items;
                    $scope.hasNext = items.hasNext;
                })
            }
        }]
    );
}(angular));
