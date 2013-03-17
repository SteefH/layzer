;(function (ng) {
    ng.module('layzer').controller(
        'SubscriptionsCtrl',
        ['$scope', 'subscriptionsservice', function($scope, subscriptions) {
            $scope.subscriptions = subscriptions.query();
        }]
    );
}(angular));
