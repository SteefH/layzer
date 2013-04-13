;(function (ng) {
    ng.module('layzer').controller(
        'FeedItemsCtrl',
        ['$scope', 'feedItems', '$routeParams', 'feeditemsservice',
         function ($scope, feeditems, $routeParams, feeditemsservice) {

            ng.extend($scope, {
                items: feeditems.items,
                hasNext: feeditems.hasNext,
                _shownItem: null,
                isShown: function isShown(item) {
                    return item.id === $scope._shownItem;
                },

                showItem: function showItem(item) {
                    if ($scope.isShown(item)) {
                        $scope._shownItem = null;
                    } else {
                        item.bodyIfShown = item.body;
                        $scope._shownItem = item.id;
                        $scope.markRead(item);
                    }
                },
                loadMore: function loadMore() {
                    if ($scope.hasNext) {
                        feeditemsservice.nextForFeed($routeParams.feed).then(function (items) {
                            $scope.items = items.items;
                            $scope.hasNext = items.hasNext;
                        });
                    }
                },
                markRead: function markRead(item) {
                    feeditemsservice.markRead(item);
                },

                itemClass: function itemClass(item) {
                    var classes = [];
                    if (item.marked_read) {
                        classes.push('read');
                    }
                    return classes.join(' ');
                }
            });
        }]
    );
}(angular));
