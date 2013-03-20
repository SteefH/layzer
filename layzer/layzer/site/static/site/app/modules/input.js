;(function (ng) {
    "use strict";
    ng.module('input', []).directive('inputOnEscape', function () {
        return {
            link: function (scope, element, attrs) {
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
            }
        }
    });
}(angular));
