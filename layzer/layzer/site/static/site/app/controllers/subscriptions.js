;(function (ng) {
    ng.module('layzer').controller(
        'SubscriptionsCtrl',
        ['$scope', 'subscriptionsservice', function($scope, subscriptions) {
            $scope.subscriptions = subscriptions.query();
        }]
    ).controller(
        'AddSubscriptionCtrl',
        ['$scope', 'subscriptionsservice', function ($scope, Subscription) {
            $scope.add = function (siteUrl) {
                var subscription = new Subscription({
                    site_url: siteUrl
                });
                subscription.$save();
            };
        }]
    );
}(angular));
