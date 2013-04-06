;(function (ng) {

    var slideSpeed = 300,
        fadeSpeed = 300;


    ng.module('layzer', ['ngResource',  'input', 'modal']).config(
        ['$routeProvider',
         function ($routeProvider) {
            $routeProvider.when('/feed/*feed', {
                templateUrl: 'feeditems.html',
                controller: 'FeedItemsCtrl',
                resolve: {
                    feedItems: ['feeditemsservice', '$route', function (items, $route) {
                        return items.getForFeed(decodeURIComponent($route.current.params.feed));
                    }]
                }
            });
        }]
    ).animation('slide-down', function () {
        return {
            setup: function (e) {
                e.hide();
            },
            start: function (element, done) {
                element.slideDown(slideSpeed, function () {done();});
            }
        };
    }).animation('slide-up', function () {
        return {
            setup: function (e) {
                e.show();
            },
            start: function (element, done) {
                element.slideUp(slideSpeed, function () {done();});
            }
        };
    }).animation('fade-in', function () {
        return {
            setup: function (e) {
                e.css({opacity: 0});
            },
            start: function (element, done) {
                element.animate({opacity: 1}, {
                    duration: fadeSpeed,
                    done: function () { done(); }
                });
            }
        };
    }).animation('fade-out', function () {
        return {
            setup: function (e) {
                e.css({opacity: 1});
            },
            start: function (element, done) {
                element.animate({opacity: 0}, {
                    duration: fadeSpeed,
                    done: function () { done(); }
                });
            }
        };
    }).run(['$rootScope', function ($rootScope){
        function getAn(fnIn, fnOut) {
            return {
                enter: fnIn,
                leave: fnOut,
                show: fnIn,
                hide: fnOut
            };
        }
        $rootScope.an = {
            slide: getAn('slide-down', 'slide-up'),
            fade: getAn('fade-in', 'fade-out')
        };
    }]);
}(angular))
