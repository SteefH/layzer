;(function (ng) {
    ng.module('layzer').controller(
        'SubscriptionsCtrl',
        ['$scope', 'subscriptionsservice', function($scope, subscriptions) {
            $scope.subscriptions = subscriptions.getAll();
        }]
    ).controller(
        'AddSubscriptionCtrl',
        ['$scope', 'subscriptionsservice', function ($scope, Subscription) {
            $scope.add = Subscription.add;
        }]
    );
}(angular));
