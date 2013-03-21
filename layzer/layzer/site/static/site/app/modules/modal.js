;(function (ng) {
    "use strict";

    ng.module('modal', []).directive('modalWindow', ['$compile', function ($compile) {
        var modalScopeAttrs = ['close', 'header', 'submit', 'cancel', 'okText', 'cancelText'];
        var modal = $compile(
            '<div class="modal-backdrop" ng-click="{{modal.cancel}};{{modal.close}}"></div>' +
            '<form class="modal" ng-submit="{{modal.close}}">' +
                '<div class="modal-header">' +
                    '<button type="button" class="close" ng-click="{{modal.cancel}};{{modal.close}}">&times;</button>' +
                    '<h3>{{modal.header}}</h3>' +
                '</div>' +
                '<div class="modal-body">' +
                '</div>' +
                '<div class="modal-footer">' +
                    '<button class="btn btn-large btn-primary" ng-click="{{modal.submit}}">{{modal.okText || \'OK\'}}</button>' +
                    '<button class="btn btn-large" ng-click="{{modal.cancel}}">{{modal.cancelText || \'Cancel\'}}</button>' +
                '</div>' +
            '</form>'
        );

        return function (scope, element, attrs) {
            var modalModel = {};
            ng.forEach(modalScopeAttrs, function(value) {
                modalModel[value] = attrs[value] || '';
            });

            ng.extend(scope, {
                modal: modalModel
            });
            modal(scope, function (modalClone) {
                var body = modalClone.find('.modal-body');
                body.append(element.children());
                element.append(modalClone);
            });
        };
    }]);
}(angular));
