;(function (ng) {
    "use strict";

    ng.module('modal', []).directive('modal', ['$compile', function ($compile) {
        var modalScopeAttrs = ['close', 'title', 'submit', 'cancel', 'okText', 'cancelText'];
        var header = $compile(
            '<div class="modal-header">' +
                '<button type="button" class="close" ng-click="{{modal.cancel}};{{modal.close}}">&times;</button>' +
                '<h3>{{modal.title}}</h3>' +
            '</div>'
        );
        var body = '<div class="modal-body">';

        var backdrop = $compile('<div class="modal-backdrop" ng-click="{{modal.cancel}};{{modal.close}}"></div>');
        var modal = $compile('<div class="modal">');
        var footer = $compile(
            '<div class="modal-footer">' +
                '<button class="btn btn-large btn-primary" ng-click="{{modal.submit}};{{modal.close}}">{{modal.okText || \'OK\'}}</button>' +
                '<button class="btn btn-large" ng-click="{{modal.cancel}};{{modal.close}}">{{modal.cancelText || \'Camcel\'}}</button>' +
            '</div>'
        );
        var link = function (scope, element, attrs) {
            var modalModel = {};
            ng.forEach(modalScopeAttrs, function(value) {
                modalModel[value] = attrs[value] || '';
            });

            ng.extend(scope, {
                modal: modalModel
            });
            modal(scope, function (modalClone) {
                element.children().wrap(modalClone);
                header(scope, function (clone) { modalClone.prepend(clone); });
                footer(scope, function (clone) { modalClone.append(clone); });
            });
            element.children().wrap(body);
            element.children().wrap(modal);
            backdrop(scope, function (clone) { element.prepend(clone); });
        };
        return {
            link: link
        }
    }]);
}(angular));
