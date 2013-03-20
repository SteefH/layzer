;(function (ng) {
    "use strict";
    var module = ng.module('effects', []),
        directive = ng.bind(module, module.directive);

    var createEffectDirective = function (options) {
        var inFunc = options.inFunc,
            outFunc = options.outFunc,
            initiallyHidden = options.initiallyHidden,
            ucName = ng.uppercase(options.name.substr(0, 1)) + options.name.substr(1),
            directiveName = 'effects' + ucName,
            speedName = 'effects' + ucName + 'Speed';

        directive(directiveName, ['$timeout', function ($timeout) {
            var result = { }, link;

            link = function (scope, element, attributes) {
                var expr = attributes[directiveName],
                    speed = 'fast';
                try {
                    speed = ng.fromJson(attributes[speedName]);
                } catch (e) {
                    // nothing
                }
                scope.$watch(expr, function (value) {
                    $timeout(function () {
                        element.stop(true);
                        element[value ? inFunc : outFunc](speed);
                    });
                });
                element[scope.$eval(expr) ? 'show' : 'hide']();
            };
            if (initiallyHidden) {
                result.compile = function (element) {
                    element.hide();
                    return link;
                };
            } else {
                result.link = link;
            }
            return result;
        }]);
    };

    createEffectDirective({
        name: 'fade', inFunc: 'fadeIn', outFunc: 'fadeOut',
        initiallyHidden: true
    });
    createEffectDirective({
        name: 'slide', inFunc: 'slideDown', outFunc: 'slideUp',
        initiallyHidden: true
    });

}(angular));
