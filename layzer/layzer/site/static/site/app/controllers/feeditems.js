;(function (ng) {
    ng.module('layzer').controller(
        'FeedItemsCtrl',
        ['$scope', 'feedItems', '$routeParams',
         function ($scope, feeditems, $routeParams) {
            $scope.items = feeditems;
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
        }]
    );
}(angular));
