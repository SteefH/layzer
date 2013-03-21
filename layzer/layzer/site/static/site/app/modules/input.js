;(function (ng) {
    "use strict";
    ng.module('input', []).directive('inputOnEscape', function () {
        return function (scope, element, attrs) {
            var expr = attrs.inputOnEscape,
                handler;
            handler = function (e) {
                if (e.keyCode === 27) {
                    scope.$apply(expr);
                }
            };
            element.on('keydown.keys', handler);
            var removeOn = scope.$on('$destroy', function () {
                element.off('keydown.keys', handler);
                removeOn();
            });
        };
    }).directive('autoFocus', ['$timeout', function ($timeout) {

        return{

            link: function (scope, element, attrs) {
                var e = element[0];
                scope.$watch(attrs.autoFocus, function (value) {
                    $timeout(function () {
                        e[value ? 'focus' : 'blur']();
                        if (value) {
                            e.select();
                        }
                    });
                });
            },
            priority: -10000
        };
    }]);
}(angular));
