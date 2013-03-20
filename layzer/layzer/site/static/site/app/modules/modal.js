;(function (ng) {
    "use strict";

    ng.module('modal', []).directive('modal', ['$compile', function ($compile) {

        var header = $compile(
            '<div class="modal-header">' +
                '<button type="button" class="close" ng-click="{{modalClose}}">&times;</button>' +
                '<h3>{{modalTitle}}</h3>' +
            '</div>'
        );
        var body = '<div class="modal-body">';
        var footer = $compile(
            '<div class="modal-footer">' +
                '<button class="btn btn-large btn-primary" ng-click="{{modalSubmit}};{{modalClose}}">{{modalOkText}}</button>' +
                '<button class="btn btn-large" ng-click="{{modalCancel}};{{modalClose}}">{{modalCancelText}}</button>' +
            '</div>'
        );
        var link = function (scope, element, attrs) {
            ng.extend(scope, {
                modalClose: attrs.close || '',
                modalTitle: attrs.title || '',
                modalSubmit: attrs.submit || '',
                modalCancel: attrs.cancel || '',
                modalOkText: attrs.okText || 'OK',
                modalCancelText: attrs.cancelText || 'Cancel'
            });
            element.addClass('modal');
            element.children().wrap(body);
            header(scope, function (clone) { element.prepend(clone); });
            footer(scope, function (clone) { element.append(clone); });
        };
        return {
            link: link
        }
    }]);
}(angular));
