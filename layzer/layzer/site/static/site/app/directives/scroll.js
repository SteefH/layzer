;(function (ng) {
    ng.module('layzer').directive('lzScrollIntoView', function () {
        return {
            link: function (scope, element, attrs) {
                scope.scrollIntoView = function () {
                    element[0].scrollIntoView(true);
                }
                scope.$watch(attrs.lzScrollIntoView, function (value) {
                    if (value) {
                        element[0].scrollIntoView(true);
                    }
                });
            }
        }
    }).directive('lzScrolledToBottom', function() {
        return function (scope, element, attrs) {
            var e = element[0];
            element.scroll(function () {
                if (e.offsetHeight + e.scrollTop >= e.scrollHeight) {
                    scope.$eval(attrs.lzScrolledToBottom)
                }
            });
        };
    });
}(angular));
