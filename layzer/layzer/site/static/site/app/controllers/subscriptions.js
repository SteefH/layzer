;(function (ng) {
    ng.module('layzer').controller(
        'SubscriptionsCtrl',
        ['$scope', 'subscriptionsservice', function($scope, subscriptions) {
            $scope.subscriptions = subscriptions.getAll();
            $scope.rename = {
                active: false,
                start: function (subscription) {
                    this.subscription = subscription;
                    this.active = true;
                    this.newName = subscription.name
                },
                submit: function () {
                    this.subscription.name = this.newName;
                    subscriptions.edit(this.subscription);
                },
                end: function () {
                    this.active = false;
                }
            };
            $scope.remove = {
                active: false,
                start: function (subscription) {
                    this.subscription = subscription;
                    this.active = true;
                },
                submit: function () {
                    subscriptions.remove(this.subscription).then(function(removed) {
                        var newSubscriptions = [];
                        ng.forEach($scope.subscriptions, function (sub) {
                            if (sub.id !== removed.id) {
                                this.push(sub);
                            }
                        }, newSubscriptions);
                        $scope.subscriptions = newSubscriptions;
                    });
                    this.active = false;
                },
                end: function () {
                    this.active = false;
                }
            };
            $scope.subscribe = {
                start: function () {
                    this.url = '';
                    this.active = true;
                },
                end: function () {
                    this.active = false;
                },
                submit: function () {
                    subscriptions.add(this.url).then(function(sub) {
                        $scope.subscriptions.push(sub);
                    }, function (response) {
                        if (response.status === 409) {
                            $scope.alert.start('Je bent al geabonneerd op deze site');
                        }
                    });
                }
            };
            $scope.alert = {
                start: function (message) {
                    this.message = message;
                    this.active = true;
                },
                end: function () {
                    this.active = false;
                }
            }
        }]
    );
}(angular));
