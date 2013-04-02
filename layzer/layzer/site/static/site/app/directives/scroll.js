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
    });
}(angular));
